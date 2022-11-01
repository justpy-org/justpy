"""
Created on 2022-10-21

@author: wangw37
"""
import justpy as jp
import pandas as pd

class TestIssue578():
    """ 
    test for Issue 578
    
    see https://github.com/justpy-org/justpy/issues/578
    """
    def __init__(self,data_frames:list):
        """
        constructor
        """
        if len(data_frames)<1:
            raise Exception("There needs to be at least one data frame")
        self.data_frames=data_frames
        self.data_frame_index=0
        
    def next_index(self):
        """
        calculate the next index
        """
        return (self.data_frame_index+1) % len(self.data_frames)
    
    def next_button_text(self):
        """
        calculate the button text for selecting the next index
        """
        n_index=self.next_index()
        return f"show dataframe {n_index}"
        
    def content(self):
        """
        the browser main web page
        """
        self.wp =jp.WebPage()
        self.button = jp.Button(a=self.wp, text=self.next_button_text(), classes='mt-1 w-fit px-4 py-2 rounded-md border border-gray-300 shadow-sm bg-green-200 text-red-700')
        self.div = jp.Div(a=self.wp)
        self.ag_grid=jp.AgGrid(a=self.div)
        self.load_dataframe()
        self.button.on('click', self.button_click)
        return self.wp
    
    def load_dataframe(self):
        """
        load the dataframe for the current index
        """
        self.ag_grid.load_pandas_frame(self.data_frames[self.data_frame_index])
    
    async def button_click(self, _msg):
        """
        react on the button click
        """
        self.data_frame_index=self.next_index()
        self.load_dataframe()
        self.button.text=self.next_button_text()

def grid_test_issue578():
    """
    setup the TestIssue class and 
    """
    data_frame = pd.DataFrame(data= {'col1': [1, 2], 'col2': [11, 22]})
    data_frame1 = pd.DataFrame(data= {'col1': [10, 20], 'col2': [11, 22], 'col3': [111, 222]})
    testIssue578=TestIssue578(data_frames=[data_frame,data_frame1])
    return testIssue578.content()

from examples.basedemo import Demo
Demo("Issue 578 new_aggrid", grid_test_issue578)
