'''
Created on 2022-09-07

@author: wf
'''
class Context:
    """ 
    legacy context handler, encapsulates context
    """
    
    def __init__(self,context_dict:dict):
        """
        constructor
        
        Args:
            context_dict(dict): a context dict in legacy format
        """
        self.context_dict=context_dict
        self.page_options=PageOptions(context_dict.get("page_options",{}))
        
    def as_javascript(self):
        """
        generate my initial JavaScript
        """
        title=self.page_options.get_title()
        debug=str(self.page_options.get_debug()).lower()
        page_ready=str(self.page_options.get_page_ready()).lower()
        result_ready=str(self.page_options.get_result_ready()).lower()
        reload_interval_ms=self.page_options.get_reload_interval_ms()
        javascript=f"""let justpy_core=new JustpyCore(
      this, // window
      '{title}', // title
      {page_ready}, // page_ready
      {result_ready}, // result_ready     
      {reload_interval_ms}, // reload_interval
      {debug}   // debug
    );"""
        return javascript
        
class PageOptions:
    """
    legacy page_options handler, encapsulating page_options
    """
    
    def __init__(self,page_options_dict:dict):
        self.page_options_dict=page_options_dict 
        self.events=page_options_dict["events"]
        
    def get_title(self):
        return self.page_options_dict.get("title","JustPy")

    def get_debug(self):
        return self.page_options_dict.get("debug",False)
    
    def get_page_ready(self):
        return "page_ready" in self.events
    
    def get_result_ready(self):
        return "result_ready" in self.events
    
    def get_reload_interval_ms(self)->float:
        reload_interval=self.page_options_dict.get("reload_interval",0)
        if reload_interval:
            ms=round(reload_interval*1000)
        else:
            ms=0
        return ms