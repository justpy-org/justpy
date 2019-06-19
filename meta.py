import justpy as jp
from itsdangerous import Signer
import uuid
import markdown
from mdx_gfm import GithubFlavoredMarkdownExtension
# https://stackoverflow.com/questions/24027589/how-to-convert-raw-javascript-object-to-python-dictionary

import demjson
import json #_jsonnet
import ast


s1 = """
{title: {
        text: 'Solar Employment Growth by Sector, 2010-2016'
    },
    subtitle: {
        text: 'stam'
    }}
"""
s2 ="{'title': {'text': 'Solar Employment Growth by Sector, 2010-2016'}, 'subtitle': {'text': 'stam'}}"
s3="""
{

    title: {
        text: 'Solar Employment Growth by Sector, 2010-2016'
    },

    subtitle: {
        text: 'Source: thesolarfoundation.com'
    },

    yAxis: {
        title: {
            text: 'Number of Employees'
        }
    },
    legend: {
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'middle'
    },

    plotOptions: {
        series: {
            label: {
                connectorAllowed: false
            },
            pointStart: 2010
        }
    },

    series: [{
        name: 'Installation',
        data: [43934, 52503, 57177, 69658, 97031, 119931, 137133, 154175]
    }, {
        name: 'Manufacturing',
        data: [24916, 24064, 29742, 29851, 32490, 30282, 38121, 40434]
    }, {
        name: 'Sales & Distribution',
        data: [11744, 17722, 16005, 19771, 20185, 24377, 32147, 39387]
    }, {
        name: 'Project Development',
        data: [null, null, 7988, 12169, 15112, 22452, 34400, 34227]
    }, {
        name: 'Other',
        data: [12908, 5948, 8105, 11248, 8989, 11816, 18274, 18111]
    }],

    responsive: {
        rules: [{
            condition: {
                maxWidth: 500
            },
            chartOptions: {
                legend: {
                    layout: 'horizontal',
                    align: 'center',
                    verticalAlign: 'bottom'
                }
            }
        }]
    }

}
"""
# print(demjson.decode(s1))
# print(demjson.decode(s2))
# s4 = (demjson.decode(s3))
# print(s4)
# print()
# help(demjson)
# print(json.dumps(s4))

# pt = parse_test("a = {text: 'hello', subtext: 'bye'}")


#----------------------------------

def change_editor(self, msg):
    print('in change')
    print(self.value)
    self.value += 'hello'

def click(self, msg):
    self.text = 'I was clicked'

def ed_test(request):
    wp = jp.WebPage()
    # a = jp.Hello(a=wp, click=click)
    # jp.Hello(a=wp)
    # jp.Hello(a=wp)
    # jp.Hello(a=wp)
    e = jp.EditorJP(a=wp, value='initial')
    # e = jp.TextArea(a=wp)
    e.on('change', change_editor)
    # e.on('input', change_editor)
    # jp.Hello(a=wp)
    in1 = jp.Input(placeholder='type here', a=wp)

    # jp.Hello(a=wp)
    # jp.Hello(a=wp)
    # jp.Hello(a=wp)
    return wp

# jp.justpy(ed_test)


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Point:
   # x, y, color eventually marker

    def __init__(self,  **kwargs):


        for k, v in kwargs.items():
            self.__setattr__(k,v)








def test_plot():
    ts = pd.Series(np.random.randn(1000), index = pd.date_range('1/1/2000', periods=1000))
    ts = ts.cumsum()
    ts.plot()
    plt.show()

# test_plot()

a = ['columnrange',
     'cylinder',
     'dependencywheel',
     'errorbar',
     'funnel',
     'funnel3d',
     'gauge',
     'heatmap',
     'histogram',
     'item',
     'line',
     'networkgraph',
     'organization',
     'packedbubble',
     'pareto',
     'pie',
     'polygon',
     'pyramid',
     'pyramid3d',
     'sankey',
     'scatter',
     'scatter3d',
     'series',
     'solidgauge',
     'spline',
     'streamgraph',
     'sunburst',
     'tilemap',
     'timeline',
     'treemap',
     'variablepie',
     'variwide',
     'vector',
     'venn',
     'waterfall',
     'windbarb',
     'wordcloud',
     'xrange']

a = """
{ legend: {
        align: 'right',
        verticalAlign: 'top',
        layout: 'vertical',
        x: 0,
        y: 100
    }}

"""
import json, demjson
print(a)
print(demjson.decode(a))
