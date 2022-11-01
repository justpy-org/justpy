"""
Created on 2022-10-19

see https://github.com/justpy-org/justpy/issues/571

@author: getzze
"""
#!/usr/bin/env python3
import justpy as jp
import numpy as np
import copy

class TestIssue571():
    """
    Test handling not a number values in aggrid
    see https://github.com/justpy-org/justpy/issues/571
    
    """
    def __init__(self):
        """
        constructor
        """
        self.button_classes = "w-32 mr-2 mb-2 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full"
 
        self.columnDefs= [
                {'headerName': 'Name', 'field': 'name'},
                {'headerName': 'Age', 'field': 'age'},
        ]
        
        # The tabular data to work on (represented by a list of dicts)
        self.original_lod = [
                {'name': 'Alice', 'age': 18},
                {'name': 'Bob', 'age': 21},
                {'name': 'Carol', 'age': 42},
        ]
        
    def addButton(self,text,click):
        return jp.Button(text=text, click=click, a=self.wp, classes=self.button_classes)
    
    def grid_test_issue571(self):
        """
        test issue 571
        """
        self.wp = jp.WebPage()
        self.grid = jp.AgGrid(a=self.wp, classes='max-h-60')
        self.addButton(text='Update via options rowData', click=self.update_via_rowdata)
        self.addButton(text='Update via load_lod', click=self.update_via_load_lod)
        self.addButton(text='Update with a np.nan', click=self.update_with_nan)   
        self.reloadButton=self.addButton(text="restore original table data", click=self.restore_table)
        self.reload()
        return self.wp
    
    def reload(self, _msg={}):
        """
        update the grid content via direct rowdata access
        """
        self.lod=copy.deepcopy(self.original_lod)
        self.grid.load_lod(lod=self.lod,columnDefs=self.columnDefs)
        
    async def restore_table(self, _msg):
        self.reload(_msg)
        self.reloadButton.text="restore original table data"
        await self.wp.update()

    async def update_via_rowdata(self, _msg):
        """
        update the grid content via direct rowdata access
        """
        self.grid.options["rowData"][1]["age"]+= 1
         
    async def update_via_load_lod(self, _msg):
        """
        update the grid content via load_lod function
        """
        self.lod[0]["age"] += 1
        self.grid.load_lod(lod=self.lod,columnDefs=self.columnDefs)
        
    async def update_with_nan(self, _msg):
        """
        update the grid content with a not a number value
        """
        self.reloadButton.text="click me to fix table"
        await self.wp.update()
        self.lod[2]["age"] = np.nan
        self.grid.load_lod(lod=self.lod,columnDefs=self.columnDefs)
        

def test_issue571():
    testIssue571=TestIssue571()
    return testIssue571.grid_test_issue571()
    

from examples.basedemo import Demo
Demo("Issue 500 aggrid uuid value", test_issue571)
