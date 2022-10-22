"""
Created on 2022-10-19

see https://github.com/justpy-org/justpy/issues/571

@author: getzze
"""
#!/usr/bin/env python3
import justpy as jp
import numpy as np

button_classes = "w-32 mr-2 mb-2 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full"
 
columnDefs= [
        {'headerName': 'Name', 'field': 'name'},
        {'headerName': 'Age', 'field': 'age'},
]

# The tabular data to work on (represented by a list of dicts)
lod = [
        {'name': 'Alice', 'age': 18},
        {'name': 'Bob', 'age': 21},
        {'name': 'Carol', 'age': 42},
]

def grid_test_issue571():
    """
    test issue 571
    """
    wp = jp.WebPage()
    grid = jp.AgGrid(a=wp, classes='max-h-60')
    grid.load_lod(lod=lod,columnDefs=columnDefs)

    async def update_via_rowdata(self, _msg):
        """
        update the grid content via direct rowdata access
        """
        grid.options["rowData"][1]["age"]+= 1
         
    async def update_via_load_lod(self, _msg):
        """
        update the grid content via load_lod function
        """
        lod[0]["age"] += 1
        grid.load_lod(lod=lod,columnDefs=columnDefs)
        
    async def update_with_nan(self, _msg):
        """
        update the grid content with a not a number value
        """
        lod[2]["age"] = np.nan
        grid.load_lod(lod=lod,columnDefs=columnDefs)
 
    jp.Button(text='Update via options rowData', click=update_via_rowdata, a=wp, classes=button_classes)
    jp.Button(text='Update via load_lod', click=update_via_load_lod, a=wp, classes=button_classes)
    jp.Button(text='Update with a np.nan', click=update_with_nan, a=wp, classes=button_classes)   
    return wp

from examples.basedemo import Demo
Demo("Issue 500 aggrid uuid value", grid_test_issue571)
