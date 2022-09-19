# Justpy Tutorial demo grid_test11 from docs/grids_tutorial/grid_events.md
import justpy as jp
import pandas as pd

wm_df = pd.read_csv('https://elimintz.github.io/women_majors.csv').round(2)

def row_selected2(self, msg):
    print(msg)
    if msg.selected:
        self.row_data_div.text = msg.data
        self.row_selected2 = msg.rowIndex
    elif self.row_selected2 == msg.rowIndex:
        self.row_data_div.text = ''

def grid_test11():
    wp = jp.WebPage()
    row_data_div = jp.Div(a=wp)
    grid = wm_df.jp.ag_grid(a=wp)
    grid.row_data_div = row_data_div
    grid.on('rowSelected', row_selected2)
    grid.options.columnDefs[0].checkboxSelection = True
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("grid_test11",grid_test11)
