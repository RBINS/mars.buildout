from DateTime import DateTime
from Products.CMFCore.permissions import AccessInactivePortalContent
from Products.CMFCore.utils import _checkPermission
from Products.CMFCore.utils import _getAuthenticatedUser
from Products.CMFPlone.CatalogTool import CatalogTool

orig_search = CatalogTool.search

def search(self, *args, **kw):
    """ Wrap search() the same way that searchResults() is """
    query = {}
    
    if args:
        query = args[0]
    elif 'query_request' in kw:
        query = kw.get['query_request']
    
    kw['query_request'] = query.copy()
    
    user = _getAuthenticatedUser(self)
    query['allowedRolesAndUsers'] = self._listAllowedRolesAndUsers(user)
    
    if not _checkPermission(AccessInactivePortalContent, self):
        query['effectiveRange'] = DateTime()
    
    kw['query_request'] = query
    
    return orig_search(self, **kw)

CatalogTool.search = search
