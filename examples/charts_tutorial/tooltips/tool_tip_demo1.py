# Justpy Tutorial demo tool_tip_demo1 from docs/charts_tutorial/tooltips.md
import justpy as jp

# https://www.highcharts.com/demo/line-basic
chart_def = """
{
 chart: {
        type: 'spline'
    },
    title: {
        text: ''
    },
    subtitle: {
        text: 'JustPy Tooltip Demo'
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
    }]
}
"""


def tool_tip_demo1():
    wp = jp.WebPage()
    jp.Div(text='Charts with default Highcharts tooltip', classes='m-2 p-2 text-xl bg-blue-500 text-white',a =wp)
    d = jp.Div(classes='flex flex-wrap ', a=wp)
    my_charts = []
    for i in range(3):
        my_charts.append(jp.HighCharts(a=d, classes='m-2 p-2 border', options=chart_def))
    my_charts[0].options.tooltip.shared = False
    my_charts[1].options.tooltip.shared = True
    my_charts[2].options.tooltip.split = True
    my_charts[0].options.title.text = 'Simple Tooltip'
    my_charts[1].options.title.text = 'Shared Tooltip'
    my_charts[2].options.title.text = 'Split Tooltip'
    return wp


# initialize the demo
from  examples.basedemo import Demo
Demo ("tool_tip_demo1",tool_tip_demo1)
