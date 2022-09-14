'''
Created on 2022-09-14

@author: wf
'''
import asyncio
import justpy as jp
import pandas as pd
import traceback
from jpcore.demostarter import Demostarter

class DemoBrowser():
    """
    Browser for demos
    """
    def handleException(self,ex):
        '''
        handle the given exception
        
        Args:
            ex(Exception): the exception to handle
        '''
        errorMsg=str(ex)
        trace=""
        if self.debug:
            trace=traceback.format_exc()
        if self.debug:
            print(errorMsg)
            print(trace)
        errorMsgHtml=f"{errorMsg}<pre>{trace}</pre>"
        self.errors.inner_html=errorMsgHtml
        
    async def onSizeColumnsToFit(self,_msg:dict):   
        try:
            await asyncio.sleep(0.3)
            if self.ag_grid:
                await self.ag_grid.run_api('sizeColumnsToFit()', self.wp)
        except Exception as ex:
            self.handleException(ex)
        
    async def web_page(self):
        """
        browser for justpy demos
        """
        self.wp=jp.QuasarPage()
        self.errors=jp.Div(a=self.wp)
        ds=Demostarter()
        video_size=192
        lod=ds.as_list_of_dicts(video_size=video_size)
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
        self.ag_grid=df.jp.ag_grid(a=self.wp,style=style,options=grid_options )
        self.ag_grid.html_columns = [1,2]
        self.wp.on("page_ready", self.onSizeColumnsToFit)
        return self.wp

demo_browser=DemoBrowser()
jp.justpy(demo_browser.web_page)

