'''
Created on 2022-09-14

@author: wf
'''
import asyncio
import justpy as jp
import pandas as pd
import traceback
from jpcore.demostarter import Demostarter
from jpcore.justpy_app import JustpyDemoApp
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
from justpy import parse_html, QBtn

class BaseWebPage():
    """
    Base Webpage
    """
    def __init__(self):
        """
        constructor
        """
        self.debug=True
        
    def showError(self,msg_html:str):
        """
        show the given error
        
        Args:
            msg_html(str): the html code to show as an error
        """
        self.errors.inner_html=msg_html
        
    def get_html_error(self,ex)->str:
        """
        get the html error message for the given exception
        """
        error_msg=str(ex)
        trace=""
        if self.debug:
            trace=traceback.format_exc()
        if self.debug:
            print(error_msg)
            print(trace)
        error_msg_html=f"❌{error_msg}<pre>{trace}</pre>"
        return error_msg_html
      
    def handleException(self,ex):
        '''
        handle the given exception
        
        Args:
            ex(Exception): the exception to handle
        '''
        error_msg_html=self.get_html_error(ex)
        self.showError(error_msg_html)
        
    def setup(self):
        """
        prepare basic page infrastructure
        """
        self.wp=jp.QuasarPage()
        self.wp.head_html = '<link rel="stylesheet" href="/templates/css/pygments.css">'
        # RGB 49 65 153
        color="bg-indigo-800"
        #  <q-btn glossy label="Tutorial" classes="q-mr-sm" name="tutorial-btn"></q-btn>
        self.bp = parse_html(
        f"""
<div class="q-pa-md">
  <q-layout view="HHH lpr Fff" container  style="height: 95vh" class="shadow-2 rounded-borders">
    <q-header reveal class="{color}">
        <q-toolbar name="toolbar">
            <q-btn flat round dense icon="menu"/>
            <q-toolbar-title>Justpy examples</q-toolbar-title>
            <q-space />
        </q-toolbar>
    </q-header>
    <q-page-container style="overflow: hidden;">
        <q-page padding name="main_page" style="overflow: hidden;">
            <div class="row">
              <div class="col-sm-12 name="error-display">
              </div>
            </div  
        </q-page>
    </q-page-container>    
    <q-footer class="{color} text-white">
        <div class="text-white q-pa-xs" style="height: 30px;" name="footer"></div>
    </q-footer>
</div>
""",
        a=self.wp,
    )
        self.main_page = self.bp.name_dict["main_page"]
        self.toolbar=self.bp.name_dict["toolbar"]
        #self.tutorial_btn = self.bp.name_dict["tutorial-btn"]
        #self.tutorial_btn.on("click",self.on_tutorial_btn_click)
        # put into html
        self.errors=self.bp.name_dict["error-display"]

class DemoDisplay(BaseWebPage):
    """
    display for a single demo
    """
    def __init__(self,demo:JustpyDemoApp):
        """
        constructor
        
        Args:
            demo:JustpyDemoApp: the demo to be displayed
        """
        BaseWebPage.__init__(self)
        self.demo=demo
        self.lexer=get_lexer_by_name("python")
        self.formatter=HtmlFormatter()
        self.syntax_highlighted_code=highlight(self.demo.source,self.lexer, self.formatter)    
        
    def web_page(self):
        """
        return my WebPage
        """
        self.setup()
        self.sourceFrame=jp.QDiv(a=self.main_page,classes="row")
        self.source_code_div=jp.QDiv(a=self.sourceFrame,classes="col-sm-6")
        self.source_code_div.inner_html=self.syntax_highlighted_code
        self.statusDiv=jp.QDiv(a=self.main_page)
        self.statusDiv.inner_html=self.demo.status
        return self.wp

class DemoBrowser(BaseWebPage):
    """
    Browser for demos
    """
    def __init__(self):
        BaseWebPage.__init__(self)
        self.demo_starter=Demostarter()
        jp.app.add_jproute("/demo/{demo_name}",self.show_demo)
        
    async def onSizeColumnsToFit(self,_msg:dict):   
        """
        handle event for sizing the ag_grid columns to fit
        """
        try:
            await asyncio.sleep(0.3)
            if self.ag_grid:
                await self.ag_grid.run_api('sizeColumnsToFit()', self.wp)
        except Exception as ex:
            self.handleException(ex)
        
    def web_page(self):
        """
        browser for justpy demos
        """
        self.setup()
        self.mount_all_btn=QBtn(label="Mount all",a=self.toolbar,classes="q-mr-sm",click=self.on_mount_all_btn_click)
        
        video_size=512
        lod=self.demo_starter.as_list_of_dicts(video_size=video_size)
        df=pd.DataFrame(lod)
        style='height: 90vh; width: 99%; margin: 0.25rem; padding: 0.25rem;'
        grid_options = """{
          'rowHeight': %s,
        defaultColDef: {
            filter: true,
            sortable: true,
            resizable: true,
            cellStyle: {textAlign: 'left'},
            headerClass: 'font-bold'
        }
    }""" % video_size
        self.ag_grid=df.jp.ag_grid(a=self.main_page,style=style,options=grid_options )
        self.ag_grid.html_columns = [1,2,3,4]
        self.ag_grid.on('rowSelected', self.row_selected)
        self.ag_grid.options.columnDefs[0].checkboxSelection = True
        self.wp.on("page_ready", self.onSizeColumnsToFit)
        return self.wp
    
    async def row_selected(self,msg):
        """
        a grid row has been selected
        """
        if msg.selected:
            try:
                row_data = msg.data
                index = row_data["#"]
                demo=self.demo_starter.demos[index-1]
                self.mount(demo,index)
            except BaseException as ex:
                demo.status=self.get_html_error(ex)
            pass
        
    def mount(self,demo,index):
        """
        mount the given demo at the given index
        
        Args:
            demo(JustpyDemoApp): the demo to mount
            index(int): the index of the demo
        """
        try:
            total=len(self.demo_starter.demos)
            print (f"mounting {index}/{total}:{demo}")
            demo.mount(jp.app)
            demo.try_it_url=f"/{demo.name}"
            demo.status="✅"
        except BaseException as ex:
            demo.status=self.get_html_error(ex)
              
    async def on_mount_all_btn_click(self,_msg):
        """
        mount all button has been clicked
        """
        total=len(self.demo_starter.demos)
        print(f"mount all has been clicked ... trying to mount {total} demos ")
        for i,demo in enumerate(self.demo_starter.demos):
            self.mount(demo,i+1)
        await self.wp.update()
            
    def show_demo(self,request):
        """
        show a demo by name
        """
        if "demo_name" in request.path_params:
            demo_name=request.path_params["demo_name"]
            if demo_name in self.demo_starter.demos_by_name:
                demo=self.demo_starter.demos_by_name[demo_name]
                demo_display=DemoDisplay(demo)
                return demo_display.web_page()    
            else:
                self.showError(f"example {demo_name} not found")
        self.showError("no example demo name specified")

demo_browser=DemoBrowser()
jp.justpy(demo_browser.web_page)


