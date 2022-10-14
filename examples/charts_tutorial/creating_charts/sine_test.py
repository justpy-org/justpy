# Justpy Tutorial demo sine_test from docs/charts_tutorial/creating_charts.md
import justpy as jp
import numpy as np


def sine_test():
    wp = jp.WebPage()
    chart = jp.HighCharts(a=wp, classes="border m-2 p-2 w-3/4")
    o = chart.options
    o.title.text = "Sines Galore"
    x = np.linspace(-np.pi, np.pi, 201)
    for frequency in range(1,11):
        y = np.sin(frequency * x)
        s = jp.Dict()
        s.name = f"F{frequency}"
        s.data = list(zip(x, y))
        o.series.append(s)
    return wp


# initialize the demo
from examples.basedemo import Demo
Demo("sine_test", sine_test)
