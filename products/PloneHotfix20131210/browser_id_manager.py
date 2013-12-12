from Products.Sessions.BrowserIdManager import BrowserIdManager

del BrowserIdManager.encodeUrl.im_func.__doc__
