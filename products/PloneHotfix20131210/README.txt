Plone hotfix, 2013-12-10
========================

This hotfix fixes multiple minor vulnerabilities in Plone. This hotfix fixes
issues in all versions of Plone.

The hotfix is officially supported by the Plone security team on the
following versions of Plone in accordance with the Plone
`version support policy`_: 4.3.2, 4.3.1, 4.3, 4.2.6, 4.1.6, 4.0.9 and 3.3.6.

The fixes included here will be incorporated into subsequent releases of Plone,
so Plone 4.3.3 and greater should not require this hotfix.


Installation
============

Installation instructions can be found at
https://plone.org/security/20131210


Q&A
===

Q: How can I confirm that the hotfix is installed correctly and my site is protected?
  A: On startup, the hotfix will log a number of messages to the Zope event log
  that look like this::

    2013-12-10 15:00:00 INFO Products.PloneHotfix20130611 Applied catalog patch

  The exact list of patches attempted depends on the version of Plone.
  If a patch is attempted but fails, it will be logged as a warning that says
  "Could not apply". This may indicate that you have a non-standard Plone
  installation.

Q: I am using an unsupported version of Plone and this hotfix breaks my
instance, what should I do? 
  A: If at all possible, upgrade to a supported
  version of Plone. Otherwise, comment out individual fixes from __init__.py
  until the error ceases. Please let security@plone.org know of any problems, as
  they may be specific advice available for problems.

Q: How can I report problems installing the patch?
  A: Contact the Plone security team at security@plone.org, or visit the
  #plone channel on freenode IRC.

Q: How can I report other potential security vulnerabilities?
  A: Please email the security team at security@plone.org rather than discussing
  potential security issues publicly.

.. _`version support policy`: http://plone.org/support/version-support-policy
