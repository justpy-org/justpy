# Updating Charts

In some applications, we would like charts to update as the underlying data changes. The following program updates the two series on a chart every second and then updates all the browser tabs the page is open in. The program is similar to the [clock](/tutorial/pushing_data?/#clock) example in the general tutorial.

```python
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

jp.justpy(chart_test, startup=chart_init)
```

We use `chart_dict` to define the chart including two series of 50 random integers. One series is of type scatter and the other is of type column.

The same global WebPage instance is returned following all requests and therefore we set `delete_flag` to `False`. 

The function `chart_updater` removes the first value in the two series and adds a random value at their end. Then, the page is updated and the procedure repeats itself after a 1 second non-blocking delay.
 
Notice that in the definition of the series in `chart_dict` we set the `animation` to `False`. Experiment by setting this to `True` to see the difference.
