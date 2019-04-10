"""
Script to be launched on development instance
once Data.fs has been recovered from production
"""
import logging

from plone import api
from transaction import commit
from zope.component.hooks import setSite

logger = logging.getLogger('prod-to-dev')
site = app.Plone
setSite(site)

with api.env.adopt_user(username="admin"):
    # delete ldap plugin
    if 'ldap-plugin' in site.acl_users:
        site.acl_users.manage_delObjects(['ldap-plugin'])
        commit()

    site.portal_purgepolicy.maxNumberOfVersionsToKeep = 0

commit()
