"""
Created on 2022-09-16

@author: bapowell
"""
import justpy as jp
import pandas as pd
import uuid

df = pd.DataFrame({
    "col1": range(3),
    "col2": ['Abc', 'Def', 'Ghi'],
    "col3": [pd.Timestamp(year=2016, month=4, day=d+1) for d in range(3)],
    "col4": [uuid.uuid4() for _ in range(3)]
})

async def row_selected(self, msg):
    print(msg)
    if msg.selected:
        self.row_data_div.text = msg.data
        self.row_selected = msg.rowIndex
    elif self.row_selected == msg.rowIndex:
        self.row_data_div.text = ''

def manipulate_row_data(irow, icol, col_key, val):
    if isinstance(val, uuid.UUID):
        new_val = str(val)
    elif isinstance(val, pd.Timestamp):
        new_val = val.timestamp()  # convert to POSIX epoch seconds (float)
    else:
        new_val = val
    # print(irow, icol, col_key, new_val)
    return new_val

def grid_test_issue500():
    wp = jp.WebPage()
    row_data_div = jp.Div(a=wp, text="Replace me by selecting a row")
    grid = df.jp.ag_grid(a=wp, row_data_converter=manipulate_row_data)
    grid.row_data_div = row_data_div
    grid.on("rowSelected", row_selected)
    grid.options.columnDefs[0].checkboxSelection = True
    return wp


from examples.basedemo import Demo

Demo("Issue 500 aggrid uuid value", grid_test_issue500)
