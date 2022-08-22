'''
Created on 2022-08-22

@author: wf
'''
import justpy as jp
import pandas as pd

df_object = {'row1': [], 'row2': [], 'row3': [], 'row4': [], 'row5': []}
df_object['row1'] = [pd.Timestamp(year=2016, month=4, day=8)]*5
df_object['row2'] = ['100']*5
df_object['row3'] = [100.345]*5
df_object['row4'] = [3]*5
df_object['row5'] = [100]*5

df = pd.DataFrame(df_object)

def row_selected(self, msg):
    print(msg)
    if msg.selected:
        self.row_data_div.text = msg.data
        self.row_selected = msg.rowIndex
    elif self.row_selected == msg.rowIndex:
        self.row_data_div.text = ''

def grid_test():
    wp = jp.WebPage()
    row_data_div = jp.Div(a=wp)
    grid = df.jp.ag_grid(a=wp)
    grid.row_data_div = row_data_div
    grid.on('rowSelected', row_selected)
    grid.options.columnDefs[0].checkboxSelection = True
    return wp

jp.justpy(grid_test)
from  examples.basedemo import Demo
Demo('Issue 270 aggrid timestamp value',grid_test)
