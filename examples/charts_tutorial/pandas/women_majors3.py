# Justpy Tutorial demo women_majors3 from docs/charts_tutorial/pandas.md
import justpy as jp
import pandas as pd
import itertools


wm = pd.read_csv("https://elimintz.github.io/women_majors.csv").round(2)
wm_under_20 = list(
    wm.loc[0, wm.loc[0] < 20].index
)  # Create list of majors which start under 20%


def make_pairs_list(x_data, y_data):
    return list(map(list, itertools.zip_longest(x_data, y_data)))


def women_majors3():
    wp = jp.WebPage(highcharts_theme="grid")
    wm_chart = jp.HighCharts(a=wp, classes="m-2 p-2 w-3/4")
    o = wm_chart.options  # Will save us some typing and make code cleaner
    o.title.text = "The gender gap is transitory - even for extreme cases"
    o.title.align = "left"
    o.xAxis.title.text = "Year"
    o.xAxis.gridLineWidth = 1
    o.yAxis.title.text = "% Women in Major"
    o.yAxis.labels.format = "{value}%"
    o.legend.layout = "proximate"
    o.legend.align = "right"
    o.series = []
    x_data = wm.iloc[:, 0].tolist()
    for major in wm_under_20:
        s = jp.Dict()
        y_data = wm[major].tolist()
        s.data = make_pairs_list(x_data, y_data)
        s.name = major
        s.type = "spline"
        o.series.append(s)
        s.marker.enabled = False
    return wp


# initialize the demo
from examples.basedemo import Demo

Demo("women_majors3", women_majors3)
