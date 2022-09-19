# Justpy Tutorial demo grid_test17 from docs/grids_tutorial/pandas.md
import justpy as jp
import pandas as pd

wm_df = pd.read_csv('https://elimintz.github.io/women_majors.csv').round(2)

def grid_test17():
    wp = jp.WebPage()
    wm_df.jp.ag_grid(a=wp)
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("grid_test17",grid_test17)
