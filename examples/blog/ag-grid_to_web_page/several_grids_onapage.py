# Justpy Tutorial demo several_grids_onapage 
# Several Grids on a Page       
#      
# generated by write_as_demo  at 2022-11-15T06:57:30.466895+00:00 
# 
# see https://justpy.io/blog/ag-grid_to_web_page#several-grids-on-a-page
import justpy as jp
import pandas as pd

wm = pd.read_csv('https://elimintz.github.io/women_majors.csv').round(2)
wm_under_20 = wm[wm.loc[0, wm.loc[0] < 20].index]
wm_under_20.insert(0, 'Year', wm['Year'])

def several_grids_onapage():
    """
    show several grids on a page
    """
    wp = jp.WebPage()
    wm.jp.ag_grid(a=wp)
    wm_under_20.jp.ag_grid(a=wp)
    return wp

# initialize the demo
from examples.basedemo import Demo
Demo("several_grids_onapage", several_grids_onapage)
