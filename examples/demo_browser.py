'''
Created on 2022-09-14

@author: wf
'''
import argparse
import asyncio
import gc
import justpy as jp
import os
import pandas as pd
import psutil
import socket
import traceback
from jpcore.demostarter import Demostarter
from jpcore.tutorial import TutorialManager,Example
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
        
    async def onPageReady(self,_msg:dict):   
        """
        react on page_ready event
        """
        process = psutil.Process(os.getpid())
        gc.collect()
        mem_message=(f'memory: {process.memory_info().rss:,} bytes')
        self.title_status.inner_html=mem_message
        
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
  <q-layout view="HHH lpr Fff" container  style="height: 99vh" class="shadow-2 rounded-borders">
    <q-header reveal class="{color}">
        <q-toolbar name="toolbar">
            <q-btn flat round dense icon="menu"/>
            <q-toolbar-title>Justpy examples</q-toolbar-title>
            <span class="label bg-primary text-white" name="title-status"></span>
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
        self.footer = self.bp.name_dict["footer"]
        self.toolbar=self.bp.name_dict["toolbar"]
        self.title_status=self.bp.name_dict["title-status"]
        #self.tutorial_btn = self.bp.name_dict["tutorial-btn"]
        #self.tutorial_btn.on("click",self.on_tutorial_btn_click)
        # put into html
        self.errors=self.bp.name_dict["error-display"]
        self.wp.on("page_ready", self.onPageReady)

class DemoDisplay(BaseWebPage):
    """
    display for a single demo
    """
    def __init__(self,demo:JustpyDemoApp,example:Example=None):
        """
        constructor
        
        Args:
            demo:JustpyDemoApp: the demo to be displayed
            example:Example: the tutorial example this might relate to
        """
        BaseWebPage.__init__(self)
        self.demo=demo
        self.example=example
        self.lexer=get_lexer_by_name("python")
        self.formatter=HtmlFormatter()
        self.syntax_highlighted_code=highlight(self.demo.source,self.lexer, self.formatter)    
        
    def web_page(self):
        """
        return my WebPage
        """
        self.setup()
        self.container = jp.QDiv(a=self.main_page)
        self.demo_description = jp.QDiv(a=self.container, classes="row")
        self.demo_desc = jp.QDiv(a=self.demo_description, classes="centered")
        self.demo_desc.inner_html=self.demo.source_link+"&nbsp;"
        if self.example:
            jp.Br(a=self.demo_description)
            self.example_link = jp.A(a=self.demo_description,text=self.example.header,href=self.example.github_url)
        self.sourceFrame=jp.QDiv(a=self.container, classes="row")
        # display code
        self.source_code_div=jp.QDiv(a=self.sourceFrame, classes="col-6")
        self.source_code_div.inner_html=self.syntax_highlighted_code
        # display preview
        self.preview_div = jp.QDiv(a=self.sourceFrame, classes="col-6")
        self.toggle_btn = jp.QBtnToggle(
                a=self.preview_div,
                classes="row q-ma-md",
                toggle_color='blue',
                push=True,
                glossy=True,
                input=self.toggle_preview,
                value='video',
        )
        self.toggle_btn.options.append({'label': "Video demo", 'value': "video"})
        self.toggle_btn.options.append({'label': "Live demo", 'value': "live"})
        self.preview_container = jp.QDiv(a=self.preview_div, classes="row")
        self._showVideoDemo()
        # demo status
        self._showDemoStatus()
        return self.wp

    def toggle_preview(self, _msg):
        """
        toggle between demo video and iframe preview
        """
        if self.toggle_btn.value == "live":
            self._showLiveDemo()
        else:
            self._showVideoDemo()

    def _showDemoStatus(self):
        """
        shows the status of the live demo
        """
        jp.QDiv(a=self.footer, text=f"Status{self.demo.status}")

    def _showVideoDemo(self):
        """
        Display a video demonstrating the demo
        """
        self.preview_container.delete_components()
        self.preview_video = jp.QImg(
                a=self.preview_container,
                src=self.demo.video_url,
                alt=self.demo.description,
                classes="row",
                style="max-width: 800px"
        )

    def _showLiveDemo(self):
        """
        Display an iframe showing the demo
        """
        self.preview_container.delete_components()
        jp.Iframe(
                a=self.preview_container,
                src=f"/{self.demo.wpfunc.__name__}",
                classes="col-grow",
                style="overflow:hidden; height:100vh; width:100%;"
        )


class DemoBrowser(BaseWebPage):
    """
    Browser for demos
    """
    def __init__(self):
        """
        constructor
        """
        BaseWebPage.__init__(self)
        self.demo_starter=Demostarter()
        self.tutorial_manager=TutorialManager()
        jp.app.add_jproute("/demo/{demo_name}",self.show_demo)
        self.mounted={}
        
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
            
    async def onPageReady(self,_msg:dict):   
        """
        react on page_ready event
        """
        await self.onSizeColumnsToFit(_msg)
        await super().onPageReady(_msg)
        self.footer.text=f"{len(self.mounted)} apps mounted"
        
    def web_page(self):
        """
        browser for justpy demos
        """
        self.setup()
        self.mount_all_btn=QBtn(label="Mount all",a=self.toolbar,classes="q-mr-sm",click=self.on_mount_all_btn_click)
        
        video_size=512
        lod=self.demo_starter.as_list_of_dicts(video_size=video_size)
        for record in lod:
            index=record["#"]
            demo=self.demo_starter.demos[index-1]
            example=self.tutorial_manager.examples_by_name.get(demo.name,None)
            tutorial_link=""
            if example is not None:
                tutorial_link=f"""<a href={example.github_url} target="_blank">{example.header}</a>"""
            record["tutorial"]=tutorial_link
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
        self.ag_grid.html_columns = [1,2,3,4,5,6]
        self.ag_grid.on('rowSelected', self.row_selected)
        self.ag_grid.options.columnDefs[0].checkboxSelection = True
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
            demo.try_it_url=f"/{demo.wpfunc.__name__}"
            demo.status="✅"
            self.mounted[demo.name]=demo
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
                example=self.tutorial_manager.examples_by_name.get(demo_name,None)
                demo_display=DemoDisplay(demo,example)
                return demo_display.web_page()    
            else:
                self.showError(f"example {demo_name} not found")
        self.showError("no example demo name specified")

parser = argparse.ArgumentParser(description="Justpy Examples browser")
parser.add_argument("--host", default=socket.getfqdn())
parser.add_argument("--port", type=int, default=8000)
args = parser.parse_args()
demo_browser=DemoBrowser()
jp.justpy(demo_browser.web_page,host=args.host, port=args.port)


