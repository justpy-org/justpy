# Justpy Tutorial demo chart_test from docs/charts_tutorial/updating_charts.md
import justpy as jp
import asyncio
from random import randrange


chart_dict = {
    'title': {'text': 'Updating Chart'},
    'series': [
            {'name': 'Random Column', 'type': 'column', 'animation': False, 'data': [randrange(100) for i in range(50)]},
            {'name': 'Random Scatter', 'type': 'scatter', 'animation': False, 'data': [randrange(100) for i in range(50)]}
               ],
    }

wp = jp.WebPage(delete_flag=False)
chart = jp.HighCharts(a=wp, options=chart_dict, classes='m-1 p-2 border w-10/12')


async def chart_updater():
    while True:
        await asyncio.sleep(1)
        for i in range(0,2):
            chart.options.series[i].data.pop(0)
            chart.options.series[i].data.append(randrange(100))
        jp.run_task(wp.update())


async def chart_init():
    jp.run_task(chart_updater())

async def chart_test():
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("chart_test",chart_test, startup=chart_init)
