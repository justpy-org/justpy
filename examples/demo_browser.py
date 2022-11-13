'''
Created on 2022-09-14

@author: wf
'''
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
import asyncio
import gc
import justpy as jp
import os
import sys
import psutil
import traceback
from jpcore.demostarter import Demostarter
from jpcore.tutorial import TutorialManager,Example
from jpcore.demoapp import JustpyDemoApp
from jpcore.justpy_app import JustpyServer
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
from justpy import parse_html, QBtn
from pydevd_file_utils import setup_client_server_paths

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
        
    def setup(self,extra_html=""):
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
    %s
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
""" %   extra_html,
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
        example_source=self.demo.example_source
        self.container = jp.QDiv(a=self.main_page)
        self.demo_description = jp.QDiv(a=self.container, classes="row")
        self.example_source_link = jp.Div(a=self.demo_description)
        self.example_source_link.inner_html=example_source.img_link
        self.demo_desc = jp.QDiv(a=self.demo_description, classes="centered")
        self.demo_desc.inner_html=self.demo.source_link 
        if self.example:
            # special handling for tutorial code
            pass
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
    def __init__(self,base_path:str=None,debug:bool=False):
        """
        constructor
        
        Args:
            base_path(str): the path to search examples in
            debug(bool): if True switchon debugging
        """
        BaseWebPage.__init__(self)
        self.demo_starter=Demostarter(base_path=base_path,debug=debug)
        self.tutorial_manager=TutorialManager()
        jp.app.add_jproute("/demo/{demo_name}",self.show_demo)
        self.mounted={}
        self.page_load_count=0
        self.endMount = 10
        self.startMount = 0

        
    def optionalDebug(self,args):   
        '''
        start the remote debugger if the arguments specify so
        
        Args:
            args(): The command line arguments
        '''
        if args.debugServer:
            import pydevd
            print (args.debugPathMapping,flush=True)
            if args.debugPathMapping:
                if len(args.debugPathMapping)==2:
                    remotePath=args.debugPathMapping[0] # path on the remote debugger side
                    localPath=args.debugPathMapping[1]  # path on the local machine where the code runs
                    MY_PATHS_FROM_ECLIPSE_TO_PYTHON = [
                        (remotePath, localPath),
                    ]
                    setup_client_server_paths(MY_PATHS_FROM_ECLIPSE_TO_PYTHON)
                    #os.environ["PATHS_FROM_ECLIPSE_TO_PYTHON"]='[["%s", "%s"]]' % (remotePath,localPath)
                    #print("trying to debug with PATHS_FROM_ECLIPSE_TO_PYTHON=%s" % os.environ["PATHS_FROM_ECLIPSE_TO_PYTHON"]);
         
            pydevd.settrace(args.debugServer, port=args.debugPort,stdoutToServer=True, stderrToServer=True)
            print("command line args are: %s" % str(sys.argv))
        
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
        try:
            await self.onSizeColumnsToFit(_msg)
            await super().onPageReady(_msg)
            if self.page_load_count==0:
                for i,demo_name in enumerate(
                        ["stock_test2",
                         "plot_test4",
                         "plotly_test",
                         "women_majors3",
                         "blackjack",
                         "dogs"]
                    ):
                    demo=self.demo_starter.demos_by_name[demo_name]
                    await self.add_demo(demo,i+1)
                pass
            else:
                for i,demo in enumerate(self.mounted.values()):
                    await self.add_demo_tolist(demo)
                    
            self.page_load_count+=1
            self.footer.text=f"{len(self.mounted)} apps mounted {self.page_load_count} page loads"
        except Exception as ex:
            self.handleException(ex)
            
    async def add_demo(self,demo:JustpyDemoApp,index:int):
        """
        mount and add demo to list
        """
        try:
            self.mount(demo,index)
        except BaseException as ex:
            demo.status=self.get_html_error(ex)
        await self.add_demo_tolist(demo,self.video_size)
    
    async def add_demo_tolist(self,demo:JustpyDemoApp,video_size:int=512):
        """
        add a demo (potentially with video) to the thumbnail list
        
        Args:
            demo(JustpyDemoApp): the demo app to add
            video_size(int): the size of the video (default: 512)
        """
        if isinstance(demo, str):
            print(f"{demo} is a string not a JustpyDemoApp")
            return
        video_link=demo.video_link(video_size=video_size)
        list_item_html = f"""<q-item clickable v-ripple>
                            <q-item-section avatar>{demo.example_source.img_link}</q-item-section>
                            <q-item-section>
                                {video_link}
                            </q-item-section>
                            <q-item-section avatar> 
                              <q-btn class="gt-xs text-grey-8" size="12px" flat dense round icon="delete" name="delete"/>
                            </q-item-section>
                            <q-separator spaced ></q-separator>
                        </q-item>"""
        list_item = parse_html(list_item_html)
        delete_button=list_item.name_dict["delete"]
        delete_button.video_list=self.video_list
        delete_button.list_item=list_item
        list_item.name = demo.name
        list_item.video_url = demo.video_url
        self.video_list.add_component(list_item,0)
        
        def delete_list_item(btn, _msg):
            """
            delete a list item
            """
            btn.video_list.remove(btn.list_item)
            pass
        list_item.name_dict["delete"].on("click", delete_list_item)
        
    def web_page(self):
        """
        browser for justpy demos
        """
        extra_html="""  <q-drawer name="drawer" width=784 breakpoint=700 show-if-above elevated content-class="bg-white text-blue">
            <q-scroll-area class="fit">
                <div class="q-pa-sm">
                    <q-list name="thumbnail_list">
                    </q-list>
                </div>
            </q-scroll-area>
    </q-drawer>"""
        self.setup(extra_html)
        try:

            self.video_list=self.bp.name_dict["thumbnail_list"]
            self.mount_all_btn=QBtn(label="Mount all",a=self.toolbar,classes="q-mr-sm",click=self.on_mount_all_btn_click)
            self.slider = jp.QRange(a=self.toolbar, classes='m-8 p-2', style='width: 400px', input=self.change_range, label=True,
                                     label_always=True,value=[1, 10], min=1, max=len(self.demo_starter.demos), snap=True, markers=True)
            self.mount_range_btn = QBtn(label=f'Mount range', a=self.toolbar, classes="q-mr-sm",click=self.on_mount_range_btn_click)
            self.progress = jp.QBanner(a=self.toolbar, classes="bg-purple-8 text-white",style='width: 200px', text ='Progress of mounting will show up here', show= False)
            self.video_size=512
            icon_size=32
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
        }""" % icon_size
            self.ag_grid=jp.AgGrid(a=self.main_page,style=style,options=grid_options )
            self.reload_grid()
        except Exception as ex:
            self.handleException(ex)
        return self.wp
    
    def get_lod(self):
        self.lod=self.demo_starter.as_list_of_dicts()
        for record in self.lod:
            index=record["#"]
            demo=self.demo_starter.demos[index-1]
            example=self.tutorial_manager.examples_by_name.get(demo.name,None)
            if example is not None:
                demo.example_source=example.example_source
                record["→"]=example.example_source.img_link

    def reload_grid(self):
        self.get_lod()
        self.columnDefs= []
        if len(self.lod)>0:
            first=self.lod[0]
            for key in first.keys():
                self.columnDefs.append({
                    'headerName': key, 
                    'field': key}
                )
        #self.columnDefs= [
        #        {'headerName': 'Name', 'field': 'name'},
        #        {'headerName': 'Age', 'field': 'age'},
        #]
        self.columnDefs[0]["checkboxSelection"] = True
        self.ag_grid.load_lod(lod=self.lod, columnDefs=self.columnDefs)
        self.ag_grid.html_columns = [1,2,3,4,5]
        self.ag_grid.on('rowSelected', self.row_selected)
  
    async def row_selected(self,msg):
        """
        a grid row has been selected
        """
        if msg.selected:
            try:
                row_data = msg.data
                index = row_data["#"]
                demo=self.demo_starter.demos[index-1]
                await self.add_demo(demo,index)
                self.reload_grid()
            except Exception as ex:
                self.handleException(ex)
        
    def mount(self,demo,index:int,force:bool=False):
        """
        mount the given demo 
        
        Args:
            demo(JustpyDemoApp): the demo to mount
            index(int): the index to mount the demo at
            force(bool): if True force the mount even if there is an issue for this demo
        """
        if(force or demo.issue is None or demo.fixed is not None):
            try:
                total=len(self.demo_starter.demos)
                print (f"mounting {index}/{total}:{demo}")
                demo.mount(jp.app)
                demo.try_it_url=f"/{demo.wpfunc.__name__}"
                demo.status="✅"
                self.mounted[demo.name]=demo
                self.progress.text = f"mounting {index}/{total}"
            except BaseException as ex:
                demo.status=self.get_html_error(ex)
        else:
            demo.status=(f"can't mount due to unfixed issue {demo.issue}")
            
    async def on_mount_all_btn_click(self,_msg):
        """
        mount all button has been clicked
        """
        self.mount_all_btn.loading = True
        self.slider.show = False
        self.mount_range_btn.show = False
        self.progress.show = True
        total=len(self.demo_starter.demos)
        print(f"mount all has been clicked ... trying to mount {total} demos ")
        for i,demo in enumerate(self.demo_starter.demos):
            self.mount(demo,i+1)
            await self.wp.update()
        self.reload_grid()
        self.mount_all_btn.show = False
        self.footer.text = f"{len(self.mounted)} apps mounted {self.page_load_count} page loads"
        self.progress.text += " complete"
        await self.wp.update()
        await asyncio.sleep(4)


    async def on_mount_range_btn_click(self,_msg):
        """
        mount all button has been clicked
        """
        self.mount_range_btn.loading = True
        self.slider.show = False
        self.mount_all_btn.show = False
        self.progress.show = True
        total = self.endMount-self.startMount +1
        print(f"mount range has been clicked ... trying to mount {total}  demos between {self.startMount} and {self.endMount}")
        for i,demo in enumerate(self.demo_starter.demos[self.startMount-1 : self.endMount-1], self.startMount):
            self.mount(demo, i)
            await self.wp.update()
        self.reload_grid()
        self.mount_range_btn.loading = False
        self.mount_all_btn.show = True
        self.slider.show = True
        self.progress.text += " complete"
        self.footer.text = f"{len(self.mounted)} apps mounted {self.page_load_count} page loads"
        await self.wp.update()
        await asyncio.sleep(4)
        self.progress.show = False


    def change_range(self, _msg):
        self.endMount = max(_msg.value.values())
        self.startMount = min(_msg.value.values())
        print(f'{self.startMount} - {self.endMount}')



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
        

def main(argv=None):  # IGNORE:C0111
    """main program."""

    if argv is None:
        argv = sys.argv
    try:
        program_name = os.path.basename(sys.argv[0])
        parser = ArgumentParser(
            description="Justpy Examples browser",
            formatter_class=RawDescriptionHelpFormatter,
        )
        parser.add_argument(
            "-d", "--debug", dest="debug", action="store_true", help="show debug info"
        )
        parser.add_argument(
            "--heroku", action="store_true", help="in heroku environment pick up port from env variable and set host to 0.0.0.0"
        )
        parser.add_argument(
            "-p",
            "--path",
            default=os.getcwd(),
            help="path to the examples (default: %(default)s)",
        )
        parser.add_argument('--debugServer',
                                     help="remote debug Server")
        parser.add_argument('--debugPort',type=int,
                                     help="remote debug Port",default=5678)
        parser.add_argument('--debugPathMapping',nargs='+',help="remote debug Server path mapping - needs two arguments 1st: remotePath 2nd: local Path")
   
        parser.add_argument("--host", default=JustpyServer.getDefaultHost())
        parser.add_argument("--port", type=int, default=8000)
        args = parser.parse_args(argv[1:])
        demo_browser=DemoBrowser(base_path=args.path,debug=args.debug)
        if args.heroku:
            args.port=os.environ["PORT"]
            args.host="0.0.0.0"
        demo_browser.optionalDebug(args)
        jp.justpy(demo_browser.web_page,host=args.host, port=args.port,PLOTLY=True,KATEX=True,VEGA=True)
    except Exception as e:
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        if args.debug:
            print(traceback.format_exc())
        return 2    

if __name__ == "__main__":
    sys.exit(main())

