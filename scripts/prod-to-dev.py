"""
Script to be launched on development instance
once Data.fs has been recovered from production
"""
from plone import api
from zope.component.hooks import setSite
from transaction import commit
import logging
# from ecreall.helpers.upgrade.interfaces import IUpgradeTool

logger = logging.getLogger('prod-to-dev')
site = app.Plone
setSite(site)

with api.env.adopt_user(username="admin"):
    # delete ldap plugin
    if 'ldap-plugin' in site.acl_users:
        site.acl_users.manage_delObjects(['ldap-plugin'])
        commit()

    site.portal_purgepolicy.maxNumberOfVersionsToKeep = 0
    # delete all file and image objects
    # tool = IUpgradeTool(site.portal_setup)
    #
    # def delete_object(obj, path):
    #     api.content.delete(obj=obj, check_linkintegrity=False)
    #
    #
    # tool.migrateContent(('Image', 'File'), delete_object,
    #                     commit=True, nofail=False)
    #
    # tool.reindexContents(tool.portal.portal_types.keys(),
    #                      commit=True, nofail=False)

commit()
