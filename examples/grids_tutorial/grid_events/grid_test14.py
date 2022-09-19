# Justpy Tutorial demo grid_test14 from docs/grids_tutorial/grid_events.md
import justpy as jp
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/fivethirtyeight/data/master/alcohol-consumption/drinks.csv', encoding="ISO-8859-1")

def grid_change(self, msg):
    msg.page.df = jp.read_csv_from_string(msg.data)
    c = msg.page.df.jp.plot(0, [1,2,3,4], kind='column', classes='m-2 p-2 w-2/3 border', title='Alcohol Consumption per Country')
    msg.page.c.options = c.options

def grid_test14():
    wp = jp.WebPage()
    wp.df = df
    wp.c = df.jp.plot(0, [1,2,3,4], kind='column', a=wp, classes='m-2 p-2 border', title='Alcohol Consumption per Country')
    grid = df.jp.ag_grid(a=wp)
    for event_name in ['sortChanged', 'filterChanged', 'columnMoved', 'rowDragEnd']:
        grid.on(event_name, grid_change)
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("grid_test14",grid_test14)
