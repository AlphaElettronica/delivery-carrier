# Copyright 2018 Tecnativa - Pedro M. Baeza
# Copyright 2021 Tecnativa - Carlos Roca
# Copyright 2024 Jacques-Etienne Baudoux (BCIM) <je@bcim.be>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    available_carrier_ids = fields.Many2many(
        comodel_name="delivery.carrier",
        compute="_compute_available_carrier_ids",
    )

    @api.onchange("partner_id", "partner_shipping_id")
    def _onchange_partner_id(self):
        res = None
        if hasattr(super(), "_onchange_partner_id"):
            res = super()._onchange_partner_id()
        set_default_carrier = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("delivery_auto_refresh.set_default_carrier")
        )
        if set_default_carrier:
            for order in self:
                action = order.action_open_delivery_wizard()
                carrier_id = self.env["delivery.carrier"].browse(
                    action["context"]["default_carrier_id"]
                )
                # If the carrier isn't allowed for the current shipping address, we wont
                # default to it. In that case we'd try to fallback to the former carrier.
                order.carrier_id = fields.first(
                    (carrier_id | order.carrier_id).filtered(
                        lambda x: x in order.available_carrier_ids._origin
                    )
                )
        return res

    @api.depends("partner_shipping_id")
    def _compute_available_carrier_ids(self):
        """We want to apply the same carriers filter in the header as in the wizard"""
        for sale in self:
            wizard = self.env["choose.delivery.carrier"].new({"order_id": sale.id})
            sale.available_carrier_ids = wizard.available_carrier_ids._origin

    def _get_param_auto_add_delivery_line(self):
        # When we have the context 'website_id' it means that we are doing the order from
        # e-commerce. So we don't want to add the delivery line automatically.
        if self.env.context.get("website_id"):
            return False
        return (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("delivery_auto_refresh.auto_add_delivery_line")
        )

    def _update_delivery_line(self, delivery_line, price_unit):
        """Update the existing delivery line"""
        values = self._prepare_delivery_line_vals(self.carrier_id, price_unit)
        new_vals = {}
        for f, val in values.items():
            field_def = delivery_line._fields.get(f)
            if isinstance(field_def, (fields.One2many, fields.Many2many)):
                # Tax is set with a SET command
                clear = update = False
                for cmd in val:
                    if cmd[0] == fields.Command.SET:
                        if delivery_line[f].ids != cmd[2]:
                            update = True
                    else:
                        clear = True
                if clear:
                    new_vals[f] = [fields.Command.CLEAR] + val
                elif update:
                    new_vals[f] = val
            elif isinstance(field_def, fields.Many2one):
                if delivery_line[f].id != val:
                    new_vals[f] = val
            elif f == "sequence":
                # sequence is last sequence + 1. As the delivery line already
                # exists, substract 1
                if delivery_line[f] != val - 1:
                    new_vals[f] = val
            elif delivery_line[f] != val:
                new_vals[f] = val
        if new_vals:
            delivery_line.write(new_vals)

    def _auto_refresh_delivery(self):
        self.ensure_one()
        if self.env.context.get("auto_refresh_delivery"):
            return
        if not self._get_param_auto_add_delivery_line():
            return
        if self.state not in ("draft", "sent"):
            return

        self = self.with_context(auto_refresh_delivery=True)

        if not self.carrier_id:
            self._set_delivery_carrier()

        if not self.carrier_id or self.is_all_service:
            self._remove_delivery_line()
        else:
            price_unit = self.carrier_id.rate_shipment(self)["price"]
            delivery_lines = self.order_line.filtered("is_delivery")
            if not delivery_lines:
                self._create_delivery_line(self.carrier_id, price_unit)
            elif len(delivery_lines) > 1:
                delivery_discount = delivery_lines[-1:].discount
                self._remove_delivery_line()
                sol = self._create_delivery_line(self.carrier_id, price_unit)
                if delivery_discount and sol:
                    sol.discount = delivery_discount
            else:
                self._update_delivery_line(delivery_lines[0], price_unit)
        if self.recompute_delivery_price:
            self.recompute_delivery_price = False

    @api.model_create_multi
    def create(self, vals_list):
        # Prevent to refresh delivery in the call to super
        orders = (
            super(SaleOrder, self.with_context(auto_refresh_delivery=True))
            .create(vals_list)
            .with_context(auto_refresh_delivery=False)
        )
        for order in orders:
            order._auto_refresh_delivery()
        return orders

    def write(self, vals):
        # Prevent to refresh delivery in the call to super
        res = super(SaleOrder, self.with_context(auto_refresh_delivery=True)).write(
            vals
        )
        for order in self:
            order._auto_refresh_delivery()
        return res

    def set_delivery_line(self, carrier, amount):
        if self._get_param_auto_add_delivery_line() and self.state in ("draft", "sent"):
            self.carrier_id = carrier.id
        else:
            return super().set_delivery_line(carrier, amount)

    def _is_delivery_line_voidable(self):
        """If the picking is returned before being invoiced, like when the picking
        is delivered but immediately return because the customer refused the order,
        so no delivery charges should be applied."""
        # There are invoiceable lines so there's no full return or the lines
        # were not set to refund.
        qty_delivered = sum(
            self.order_line.filtered(
                lambda x: not x.is_delivery and x.product_id.type != "service"
            ).mapped("qty_delivered")
        )
        # There must be validated pickings
        pickings = self.picking_ids.filtered(lambda x: x.state == "done")
        # If there aren't delivery lines or the order is a quotation there's
        # nothing to be done either. If there are more than one delivery lines
        # we won't be doing anything as well.
        if (
            self.state not in ("done", "sale")
            or self.invoice_ids
            or not self.order_line.filtered("is_delivery")
            or len(self.order_line.filtered("is_delivery")) > 1
            or qty_delivered
            or not pickings
        ):
            return False
        return True


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _get_protected_fields(self):
        # Avoid locked orders validation error when voiding the delivery line
        fields = super()._get_protected_fields()
        if self.env.context.get("delivery_auto_refresh_override_locked"):
            return [x for x in fields if x not in ["product_uom_qty", "price_unit"]]
        return fields
