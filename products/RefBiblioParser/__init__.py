from  RefParser import  RefParser, manage_addRefParser
from  RefRenderer import  REFRenderer, manage_addREFRenderer

def initialize(context):
    context.registerClass(RefParser,
                          constructors = (manage_addRefParser,),
                          )
                          
    context.registerClass(REFRenderer,
                          constructors = (manage_addREFRenderer,),
                          ) 
