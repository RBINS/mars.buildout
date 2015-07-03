Plone hotfix, 2015-12-08
========================

This hotfix fixes an unauthorized disclosure of registered user information in Plone.

This hotfix should be applied to the following versions of Plone:

* Plone 5.0 and any version prior
* Plone 4.3.7 and any version prior
* Any older version of Plone starting from 2.1, 2.5, 3.0, 3.1, 3.2, 3.3, 4.0, 4.1, and 4.2

The hotfix is officially supported by the Plone security team on the
following versions of Plone in accordance with the Plone
`version support policy`_: 4.0.10, 4.1.6, 4.2.7, 4.3.7 and 5.0.
However it has also received some testing on older versions of Plone.
The fixes included here will be incorporated into subsequent releases of Plone,
so Plone 4.3.8, 5.0.1 and greater should not require this hotfix.


Installation
============

Installation instructions can be found at
https://plone.org/products/plone-hotfix/releases/20151208


Q&A
===

Q: How can I confirm that the hotfix is installed correctly and my site is protected?
  A: On startup, the hotfix will log a number of messages to the Zope event log
  that look like this::

    2015-12-08 03:20:08 INFO Products.PloneHotfix20151208 Applied searchFulltextForMembers patch

  If a patch is attempted but fails, it will be logged as a warning that says
  "Could not apply". This may indicate that you have a non-standard Plone
  installation.

Q: How can I report problems installing the patch?
  A: Contact the Plone security team at security@plone.org, or visit the
  #plone channel on freenode IRC.

Q: How can I report other potential security vulnerabilities?
  A: Please email the security team at security@plone.org rather than discussing
  potential security issues publicly.

.. _`version support policy`: http://plone.org/support/version-support-policy
