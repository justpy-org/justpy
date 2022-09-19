# Justpy Tutorial demo grid_test16 from docs/grids_tutorial/pandas.md
import justpy as jp
import pandas as pd

wm_df = pd.read_csv('https://elimintz.github.io/women_majors.csv').round(2)

def grid_test16():
    wp = jp.WebPage()
    grid = jp.AgGrid(a=wp)
    grid.load_pandas_frame(wm_df)
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("grid_test16",grid_test16)
