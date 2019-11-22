# Tooltips
The tooltip is the popup that is shown when you hover over a point on the chart. One of the advantages of interactive charts is the tooltip. It allows making charts more informative. Highcharts allows defining a tooltip using a very versatile formatting function (in JavaScript). JustPy allows writing tooltip formatters for Highcharts charts in Python just as it allows writing other event handlers in Python. Let's look at a concrete example.

Please run the program below:
```python
import justpy as jp
import asyncio

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


def tool_tip_demo():
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

    jp.Div(text='Charts with user defined tooltip formatter functions', classes='m-2 p-2 text-xl bg-blue-500 text-white', a=wp)
    d = jp.Div(classes='flex flex-wrap', a=wp)
    my_charts = []
    for i in range(3):
        my_charts.append(jp.HighCharts(a=d, classes='m-2 p-2 border', options=chart_def))
    my_charts[0].options.tooltip.shared = False
    my_charts[1].options.tooltip.shared = True
    my_charts[2].options.tooltip.split = True
    my_charts[0].options.title.text = 'Simple Tooltip - Formatter Example'
    my_charts[1].options.title.text = 'Shared Tooltip - Formatter Example'
    my_charts[2].options.title.text = 'Split Tooltip - Formatter Example'

    my_charts[0].on('tooltip', simple_tooltip_formatter)
    my_charts[1].on('tooltip', shared_tooltip_formatter)
    my_charts[2].on('tooltip', split_tooltip_formatter)
    return wp


async def simple_tooltip_formatter(self, msg):
    print(msg)
    # await asyncio.sleep(0.2) # Uncomment to simulate 200ms communication delay
    s1 = f'<span class="bg-white" style="color: {msg.color}">&#x25CF;</span>'
    div1 = f'<div>My formatter:</div>'
    div2 = f'<div>{s1}{msg.series_name}</div>'
    div3 = f'<div>Year: {msg.x}</div>'
    div4 = f'<div>Number of employees: {"{:,}".format(msg.y)}</div>'
    tooltip_div = f'<div class="text-red-500 text-lg"> {div1}{div2}{div3}{div4}</div>'
    return await self.tooltip_update(tooltip_div, msg.websocket)


async def shared_tooltip_formatter(self, msg):
    print(msg)
    # await asyncio.sleep(0.2)  # Uncomment to simulate 200ms communication delay
    tooltip_div = jp.Div(classes="text-white bg-blue-800 text-xs", temp=True)
    for point in msg.points:
        point_div = jp.Div(a=tooltip_div, temp=True)
        jp.Span(text='&#x25CF;', classes='bg-white', style=f'color: {point.color}', a=point_div, temp=True)
        jp.Span(text=f'{point.series_name}', a=point_div, temp=True)
        jp.Span(text=f'Year: {point.x}', a=point_div, temp=True)
        jp.Span(text=f'Number of employees: {"{:,}".format(point.y)}', a=point_div, temp=True)
    return await self.tooltip_update(tooltip_div.to_html(), msg.websocket)


async def split_tooltip_formatter(self, msg):
    print(msg)
    # await asyncio.sleep(0.2)  # Uncomment to simulate 200ms communication delay
    tooltip_array = [f'The x value is {msg.x}']
    for point in msg.points:
        point_div = jp.Div(temp=True)
        jp.Span(text='&#x25CF;', classes='bg-white', style=f'color: {point.color}', a=point_div, temp=True)
        jp.Span(text=f'{point.series_name}', a=point_div, temp=True)
        jp.Span(text=f'Year: {point.x}', a=point_div, temp=True)
        jp.Span(text=f'Number of employees: {"{:,}".format(point.y)}', a=point_div, temp=True)
        tooltip_array.append(point_div.to_html())
    return await self.tooltip_update(tooltip_array, msg.websocket)

jp.justpy(tool_tip_demo)
```

This example uses the basic Highcharts line demo chart. In the browser tab you will see 6 charts. The top three charts use the standard Highcharts tooltip formatter. The bottom three charts use tooltip formatters written in Python. Mouseover all charts to see the difference between the different kinds of tooltips. The simple tooltip shows information only for the one point the mouse is over. The shared tooltip provides information of all the points with the same x axis value in one popup box while the split tooltip shows several popup boxes, one for each series value as well as for the x value itself. 

Assigning a tooltip formatter to a chart in JustPy is done in the same way as assigning any event handler. For example in the program above the line:
```python
my_charts[0].on('tooltip', simple_tooltip_formatter)
```

assigns the function simple_tooltip_formatter as the event handler of the tooltip event of the chart that is the first element of the list my_charts. Now, whenever this chart is required to show a tooltip, it will request from the server an HTML string to render in the tooltip popup box or boxes.
You will notice that if you quickly mouseover several points on the charts with user defined formatters (the lower three charts), you will see the "Loading…" inscription instead of the values. Only when no new tooltip event occurs for 100ms (0.1 second) JustPy retrieves tooltip values from the server. This prevents the server from being inundated with irrelevant tooltip requests as the user moves the mouse over the chart, at the cost of all tooltips showing with an extra delay.  
Let's look first at the function simple_tooltip_formatter. For the simple tooltip event, JustPy adds four entries to the msg dictionary that is the second argument to the tooltip event handler. The keys are 'x', 'y', 'color' and 'series_name, for example:
'x': 2016, 'y': 137133, 'color': '#7cb5ec', 'series_name': 'Installation'
We use these to create a string representing HTML that will be used to format the tooltip box. In this way, we can create a tooltip with point specific information. 
The tooltip is finally updated using the coroutine method of HighCharts named tooltip_update. It receives two arguments. The first is the HTML string and the second is the websocket instance used to communicate with the specific browser tab in which the tooltip event occurred. It is provided to all events as a field of msg.  The tooltip_update method returns True so the rest of the page does not get updated. Make sure that the tooltip event handler returns a value other than None so that JustPy does not update the whole page also. 
Moving to shared_tootlip_formatter, the main difference is that now msg includes a list of the points corresponding to the x value. Unsurprisingly, this list is called msg.points. To create the HTML update string, we now iterate over this list and build a more complex string. A different technique is used here to construct the HTML string. Instead of using string functions, we use JustPy components and then use the to_html method to convert the resulting structure to an HTML string. When using this technique, don't forget to set the temp attribute of all the component instances to False so that JustPy knows that they will not be interacted with in the future and do not need to be saved.
The split_tooltip_formatter is a little more complex. A split tooltip means that each series has its own separate popup box and therefore the HTML for each series needs to be returned. The tooltip_update method therefore takes as its first argument a list of strings instead of a string as in the other cases. The first string in the list represents the HTML for the x axis value. 
