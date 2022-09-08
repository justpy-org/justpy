"""
Created on 2022-09-07

@author: wf
"""
import textwrap
from typing import List

from starlette.requests import Request


class Context:
    """
    legacy context handler, encapsulates context
    """

    def __init__(self, context_dict: dict):
        """
        constructor

        Args:
            context_dict(dict): a context dict in legacy format
        """
        self.context_dict = context_dict
        self.page_options = PageOptions(context_dict.get("page_options", {}))
        self.use_websockets_js=self.context_dict.get("use_websockets","true")
        self.page_id_js=context_dict["page_id"]
        self.title_js=self.get_js_option("title", "JustPy")
        self.redirect_js=self.get_js_option("redirect","")
        self.display_url_js=self.get_js_option("display_url","")
        justpy_dict_js=str(self.context_dict.get("justpy_dict","[]"))
        self.justpy_dict_js=justpy_dict_js.replace('</' + 'script>', '</" + "script>')

    def get_url_for(self, name: str, path: str = None):
        """
        get url for the given route name
        Args:
            name: name of the route
            path: path params
        """
        url = None
        request = self.context_dict.get("request")
        if request is not None and isinstance(request, Request):
            if path is None:
                path = ""
            url = request.url_for(name, path=path)
        return url
    def get_js_option(self,key,default_value):
        """
        get the page_option with the given key as javascript using the
        default value in case the value is not set or none
        """
        js_option=self.page_options.page_options_dict.get(key,default_value)
        if js_option is None:
            js_option=default_value
        return js_option
        
    def as_html_lines(self,indent:str="  "):
        """
        generate the html lines for justpy to work 
        """
        html=self.as_script_src("justpy_core")
        html+=f"""{indent}<script>
{indent}  var page_id = {self.page_id_js};
{indent}  var use_websockets = {self.use_websockets_js};
{indent}  var justpyComponents = {self.justpy_dict_js};
"""
        html+=self.as_javascript_constructor(indent+"  ")
        html+=f"\n{indent}</script>\n{self.as_script_srcs(indent)}"
        html+=f"{indent}<script>\n{self.as_javascript_setup(indent)}\n{indent}</script>\n"
        return html
    
    def as_script_src(self,file_name:str,indent:str="  "):
        src= f"{indent}<script src='/templates/js/{file_name}.js'></script>\n"
        return src
    
    def as_script_srcs(self,indent:str="  "):
        """
        generate a list of javascript files to be imported
        """
        srcs = ""
        for file_name in [
            "event_handler",
            "html_component",
            "quasar_component",
            "chartjp",
            "aggrid",
            "iframejp",
            "deckgl",
            "altairjp",
            "plotlyjp",
            "bokehjp",
            "katexjp",
            "editorjp",
        ]:
            srcs +=self.as_script_src(file_name,indent)
        return srcs
    
    def as_javascript_setup(self,indent):
        """
        generate the java script setup code
        """
        js=f"{indent}  justpy_core.setup();"
        return js

    def as_javascript_constructor(self,indent:str="    "):
        """
        generate my initial JavaScript
        """
        debug = str(self.page_options.get_debug()).lower()
        page_ready = str(self.page_options.get_page_ready()).lower()
        result_ready = str(self.page_options.get_result_ready()).lower()
        reload_interval_ms = self.page_options.get_reload_interval_ms()
        static_resources_url = self.get_url_for("static")
        if static_resources_url is None:
            static_resources_url = "/"
        javascript = f"""let justpy_core=new JustpyCore(
            this, // window
            {self.page_id_js}, // page_id
            '{self.title_js}', // title
            '{self.use_websockets_js}', // use_websockets
            '{self.redirect_js}', // redirect
            '{self.display_url_js}', // display_url
            {page_ready}, // page_ready
            {result_ready}, // result_ready     
            {reload_interval_ms}, // reload_interval
            {self.page_options.events},  // events
            '{static_resources_url}',  // static_resources_url
            {debug}   // debug
        );"""
        javascript = textwrap.indent(javascript, indent)
        return javascript


class PageOptions:
    """
    legacy page_options handler, encapsulating page_options
    """

    def __init__(self, page_options_dict: dict):
        self.page_options_dict = page_options_dict
        self.events: List[str] = page_options_dict.get("events", [])

    def get_debug(self):
        """
        Get debug status of the PageOptions
        """
        return self.page_options_dict.get("debug", False)

    def get_page_ready(self):
        return "page_ready" in self.events

    def get_result_ready(self):
        return "result_ready" in self.events

    def get_reload_interval_ms(self) -> float:
        reload_interval = self.page_options_dict.get("reload_interval", 0)
        if reload_interval:
            ms = round(reload_interval * 1000)
        else:
            ms = 0
        return ms
