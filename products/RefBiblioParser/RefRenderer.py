############################################################################
#                                                                          #
#             copyright (c) 2004 ITB, Humboldt-University Berlin           #
#             written by: Raphael Ritz, r.ritz@biologie.hu-berlin.de       #
#                                                                          #
############################################################################

"""REFRenderer class"""

# Python stuff
import os

# Zope stuff
from Globals import InitializeClass
from App.Dialogs import MessageDialog

# CMF stuff
from Products.CMFCore.utils import getToolByName

# Bibliography stuff
from Products.CMFBibliographyAT.BibliographyRenderer \
     import IBibliographyRenderer, BibliographyRenderer


class REFRenderer(BibliographyRenderer):
    """
    specific REF renderer
    """

    __implements__ = (IBibliographyRenderer ,)

    meta_type = "REF Renderer"

    format = {'name':'Ref',
              'extension':'REF'}

    def __init__(self,
                 id = 'ref',
                 title = "Ref renderer - renderer for local RBINS bliographic datamodel"):
        """
        initializes id and title
        """
        self.id = id
        self.title = title

    def render(self, object):
        """
        renders a bibliography object(folder, list, ...) in Ref format
        """
        bib_tool = getToolByName(object, 'portal_bibliography')
        ref_types = bib_tool.getReferenceTypes()
        if object.portal_type in ref_types:
            return self.renderEntry(object)
        if object.isPrincipiaFolderish:
            entries = object.contentValues(ref_types)
            rendered = [self.renderEntry(entry) \
                        for entry in entries]
            return ''.join(rendered)
        return ''
        

    def renderEntry(self, entry):
        """
        renders a BibliographyEntry object in Ref format
        """
        
        ref = {}
        ref['A'] = "%A " + entry.Authors(sep="\n%A ",
                                         lastsep="\n%A ",
                                         abbrev=0,
                                         lastnamefirst=1)

        value = self.AuthorURLs(entry)
        if value:
          ref['O'] = "\n%O " + '\n%O '.join(''.join(value).split('\n'))
        
        value = entry.getPublication_year().strip()
        if value:
          if value!='':
            ref['D'] = "\n%D" + value.strip()
          elif 'in press' in entry.getAbstract():
            ref['D'] = "in press"
          else:
            ref['D'] = "n.d."

        try:
          value = entry.getType()
        except:
          value =""
        if value:
          ref['R'] = "\n%R " + value.strip()

        try:
          value = entry.Title()
        except:
          value =""
        if value:
          if not ref.has_key('R') :
           for key in ['acte', 'thesis', 'eindwerk', 'thèse', 'proceedings', 'akte']:
            if key in value:
              value.split(':')
              ref['T'] = "\n%T " + value[0].strip()
              ref['R'] = "\n%R " + value[1].strip()
              break
          if not ref.has_key('T') :
            ref['T'] = "\n%T " + value.strip()

        if not ref.has_key('R') :
         try:
           value = entry.getNote()
         except:
           value =""
         if value:
          for key in ['acte', 'thesis', 'eindwerk', 'thèse', 'proceedings', 'akte']:
           if key in value:
            for svalue in value.split('\n'):
             for key2 in ['acte', 'thesis', 'eindwerk', 'thèse', 'proceedings', 'akte']:
              if key2 in svalue:
               ref['R'] = "/n%R " + svalue.strip()
               break

        try:
          value = entry.getBooktitle()
        except:
          value =""
        if value:
          if not ref.has_key('R') :
           for key in ['acte', 'thesis', 'eindwerk', 'thèse', 'proceedings', 'akte']:
            if key in value:
              value.split(':')
              ref['B'] = "\n%B " + value[0].strip()
              ref['R'] = "\n%R " + value[1].strip()
              break
          if not ref.has_key('B') :
            ref['B'] = "\n%B " + value.strip()

        try:
          value = entry.getJournal()
        except:
          value =""
        if value:
          ref['J'] = "\n%J " + value.strip()

        try:
          value = entry.getPublisher()
        except:
          value =""
        if value:
          ref['I'] = "\n%I " + value.strip()

        try:
          value = entry.getCity()
        except:
          value =""
        if value:
          ref['C'] = "\n%C " + value.strip()

        try:
          value = entry.getVolume()
        except:
          value =""
        if value:
          ref['V'] = "\n%V " + value.strip()

        try:
          value = entry.getNumber()
        except:
          value =""
        if value:
          ref['N'] = "\n%N " + value.strip()

        try:
          value = entry.getPages()
        except:
          value =""
        if value:
          ref['P'] = "\n%P " + value.strip()

        try:
          value = entry.getAbstract()
        except:
          value =""
        if value:
          if not ref.has_key('O') :
            ref['O'] = "\n%O " + '\n%O '.join(''.join(value).split('\n'))
          else:
            ref['O'] += "\n%O " + '\n%O '.join(''.join(value).split('\n'))

        try:
          value = entry.getNote()
        except:
          value=""
        if value:
          svalue = value.split('\n')
          value=""
          for key in svalue:
            for key2 in ['acte', 'thesis', 'eindwerk', 'thèse', 'proceedings', 'akte', 'in press', 'automatic ref import']:
              if key2 in key:
                key = ''
                break
            if key != '':
              value += key.strip() + '\n'
          ref['X'] = "/n%X " + value.strip()

        try:
          value = entry.getURL()
        except:
          value =""
        if value:
          if not ref.has_key('O') :
            ref['O'] = "\n%O " + '\n%O '.join(''.join(value).split('\n'))
          else:
            ref['O'] += "\n%O " + '\n%O '.join(''.join(value).split('\n'))

        try:
          value = entry.getSubject()
        except:
          value =""
        if value:
          ref['K'] = "\n%K " + '\n%K '.join(''.join(value).split('\n'))

        refer=''
        for key in ['A', 'D', 'T', 'R', 'I', 'K', 'J', 'V', 'P', 'B', 'C', 'E', 'X', 'O', 'N', 'M', 'Z', ]:
          refer += ref.get(key, '')
        return refer + '\n\n'

    def AuthorURLs(self, entry):
        """a string with all the known author's URLs;
        helper method for bibtex output"""
        a_list = entry.getAuthorList()
        a_URLs = ''
        for a in a_list:
            url = a.get('homepage', ' ')
            if url != ' ':
              a_URLs += "%s and " % url
        if a_URLs != '':
          a_URLs = a_URLs[:-5]
        return a_URLs[:-5]


# Class instanciation
InitializeClass(REFRenderer)

def manage_addREFRenderer(self, REQUEST=None):
    """ """
    try:
        self._setObject('REF', REFRenderer())
    except:
        return MessageDialog(
            title='Bibliography tool warning message',
            message='The renderer you attempted to add already exists.',
            action='manage_main')
    return self.manage_main(self, REQUEST)
