import justpy as jp
import pandas as pd

wm = pd.read_csv('https://elimintz.github.io/women_majors.csv').round(2)
wm_under_20 = wm[wm.loc[0, wm.loc[0] < 20].index]
wm_under_20.insert(0, 'Year', wm['Year'])

# Tailwind classes to format header div
title_classes = 'text-2xl text-white bg-blue-500 text-center mb-2 p-2'

# Change grid default style to change height
grid_style = 'height: 85vh; width: 99%; margin: 0.25rem; padding: 0.25rem;'

@jp.SetRoute('/wm')
def serve_wm():
    wp = jp.WebPage()
    jp.Div(text='All Majors', classes=title_classes, a=wp)
    wm.jp.ag_grid(a=wp, style=grid_style)
    return wp

@jp.SetRoute('/wm_20')
def serve_wm():
    wp = jp.WebPage()
    jp.Div(text='Only Majors with Women Starting Under 20%', classes=title_classes, a=wp)
    wm_under_20.jp.ag_grid(a=wp, style=grid_style)
    return wp

jp.justpy()