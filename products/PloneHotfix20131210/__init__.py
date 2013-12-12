import logging


logger = logging.getLogger('Products.PloneHotfix20131210')


hotfixes = [
    'browser_id_manager',
    'catalog',
    'factory',
    'image',
    ]


PLONE_ONLY = ['catalog', 'factory']

try:
    import Products.CMFPlone
except ImportError:
    # No Plone. Remove all but the Zope patches.
    for f in PLONE_ONLY:
        if f in hotfixes:
            hotfixes.remove(f)


# Apply the fixes
for hotfix in hotfixes:
    try:
        __import__('Products.PloneHotfix20131210.%s' % hotfix)
        logger.info('Applied %s patch' % hotfix)
    except:
        logger.warn('Could not apply %s' % hotfix)
logger.info('Hotfix installed')
