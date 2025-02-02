===============================
PostLogistics Labels WebService
===============================

.. 
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! This file is generated by oca-gen-addon-readme !!
   !! changes will be overwritten.                   !!
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! source digest: sha256:5234dd08026ec3787d48cbe33c5b438f1a4adbd0276d8da4e5917c4d0d2686f3
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

.. |badge1| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :target: https://odoo-community.org/page/development-status
    :alt: Beta
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |badge3| image:: https://img.shields.io/badge/github-OCA%2Fdelivery--carrier-lightgray.png?logo=github
    :target: https://github.com/OCA/delivery-carrier/tree/12.0/delivery_carrier_label_postlogistics
    :alt: OCA/delivery-carrier
.. |badge4| image:: https://img.shields.io/badge/weblate-Translate%20me-F47D42.png
    :target: https://translation.odoo-community.org/projects/delivery-carrier-12-0/delivery-carrier-12-0-delivery_carrier_label_postlogistics
    :alt: Translate me on Weblate
.. |badge5| image:: https://img.shields.io/badge/runboat-Try%20me-875A7B.png
    :target: https://runboat.odoo-community.org/builds?repo=OCA/delivery-carrier&target_branch=12.0
    :alt: Try me on Runboat

|badge1| |badge2| |badge3| |badge4| |badge5|

This module uses `PostLogistics BarCodes WebService`_ to generate labels
for your Delivery Orders.

It adds a `Create label` button on Delivery Orders.
A generated label will be an attachement of your Delivery Order.

To see it, please install documents module.

You can create multiple delivery method to match your diffent package types.

.. _PostLogistics BarCodes WebService: https://www.post.ch/en/business/a-z-of-subjects/dropping-off-mail-items/business-sending-letters/sending-consignments-web-service-barcode

**Table of contents**

.. contents::
   :local:

Installation
============

As a requirement you need to install `suds-jurko` library. It will fail with the
latest and outdated version of `suds`.
https://pypi.python.org/pypi/suds-jurko/0.6


Furthermore, if you want to use the integration server of Postlogistics
you will have to patch this library with the following patch:

https://fedorahosted.org/suds/attachment/ticket/239/suds_recursion.patch

A copy of this patch is available in `patches` folder of this module.

Configuration
=============

.. important::
   A "Swiss Post Business customer" account is required to use this module.

   See `Log in`_


To configure:

* Go to `Configurations -> Settings -> Postlogistics`
* Set your login informations
* launch the Update PostLogistics Services

This will load available services and generate carrier options.

Now you can create a carrier method for PostLogistics WebService:

* First choose a Service group and save
* Add a Mandatory Carrier option using a Basic Service
* Save Carrier Method (this will update filters to show you only
  compatible services)
* Then add other `Optional as default` and `Optional` carrier option
  from listed
* Add additional Service and Delivery instructions

.. _Log in: https://account.post.ch/selfadmin/?login&lang=en

Technical references
~~~~~~~~~~~~~~~~~~~~

`"Barcode" web service documentation`_

.. _"Barcode" web service documentation: https://www.post.ch/en/business/a-z-of-subjects/dropping-off-mail-items/business-sending-letters/barcode-support

Known issues / Roadmap
======================

* Integration of price webservice :
  https://www.post.ch/en/customer-center/all-online-services/preise-berechnen/info

* Not sure if the recursive patch of suds is still needed as there's no need
  to use the integration WS anymore. However we still want to patch open to
  get meaningful error messages.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/delivery-carrier/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us to smash it by providing a detailed and welcomed
`feedback <https://github.com/OCA/delivery-carrier/issues/new?body=module:%20delivery_carrier_label_postlogistics%0Aversion:%2012.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Authors
~~~~~~~

* Camptocamp

Contributors
~~~~~~~~~~~~

* Yannick Vaucher <yannick.vaucher@camptocamp.com>
* Guewen Baconnier <guewen.baconnier@camptocamp.com>
* Akim Juillerat <akim.juillerat@camptocamp.com>
* Julien Coux <julien.coux@camptocamp.com>

Maintainers
~~~~~~~~~~~

This module is maintained by the OCA.

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

This module is part of the `OCA/delivery-carrier <https://github.com/OCA/delivery-carrier/tree/12.0/delivery_carrier_label_postlogistics>`_ project on GitHub.

You are welcome to contribute. To learn how please visit https://odoo-community.org/page/Contribute.
