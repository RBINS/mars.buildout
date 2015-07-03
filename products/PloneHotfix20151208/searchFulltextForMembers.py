try:
    from Products.CMFPlone import patches  # noqa
except ImportError:
    pass

from Products.PlonePAS.tools.memberdata import MemberDataTool
if hasattr(MemberDataTool.searchFulltextForMembers.im_func, '__doc__'):
    del MemberDataTool.searchFulltextForMembers.im_func.__doc__
