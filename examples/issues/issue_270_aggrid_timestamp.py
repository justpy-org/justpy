"""
Created on 2022-08-22

@author: wf
"""
import justpy as jp
import pandas as pd

df_object = {"row1": [], "row2": [], "row3": [], "row4": [], "row5": []}
df_object["row1"] = [pd.Timestamp(year=2016, month=4, day=8)] * 5
df_object["row2"] = ["100"] * 5
df_object["row3"] = [100.345] * 5
df_object["row4"] = [3] * 5
df_object["row5"] = [100] * 5

df = pd.DataFrame(df_object)
msg_div = None


async def row_selected(self, msg):
    print(msg)
    if msg.selected:
        self.a.components[0].text = msg.data
        self.row_selected = msg.rowIndex
    elif self.row_selected == msg.rowIndex:
        self.row_data_div.text = ""


async def btn_click(self, msg):
    print("Button clicked")
    self.a.components[0].text = "Clicked!!!"


def grid_test_issue270():
    wp = jp.WebPage()
    row_data_div = jp.Div(a=wp, text="Replace me by selecting a row")
    grid = df.jp.ag_grid(a=wp)
    grid.on("rowSelected", row_selected)
    grid.options.columnDefs[0].checkboxSelection = True
    btn = jp.Button(text="Click", a=wp, click=btn_click)
    return wp


from examples.basedemo import Demo

Demo("Issue 270 aggrid timestamp value", grid_test_issue270)
