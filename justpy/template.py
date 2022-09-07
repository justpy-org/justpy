'''
Created on 2022-09-07

@author: wf
'''
class Context:
    """ 
    legacy context handler, encapsulates context
    """
    
    def __init__(self,context_dict:dict):
        self.context_dict=context_dict
        self.page_options=PageOptions(context_dict.get("page_options",{}))
        
    def as_javascript(self):
        """
        generate my initial JavaScript
        """
        title=self.page_options.getTitle()
        debug=str(self.page_options.getDebug()).lower()
        javascript=f"""let justpy_core=new JustpyCore(
      this, // window
      '{title}', // title
      {debug}   // debug
    );"""
        return javascript
        
class PageOptions:
    """
    legacy page_options handler, encapsulating page_options
    """
    
    def __init__(self,page_options_dict:dict):
        self.page_options_dict=page_options_dict 
        
    def getTitle(self):
        return self.page_options_dict.get("title","JustPy")

    def getDebug(self):
        return self.page_options_dict.get("debug",False)