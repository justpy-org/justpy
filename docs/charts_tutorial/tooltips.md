# Tooltips

## Basic Use

The tooltip is the popup that is shown when you hover over a point on the chart. It provides one of the advantages of using interactive charts as it makes the chart more informative.

Highcharts allows defining a tooltip using a very versatile formatting function (in JavaScript). JustPy allows writing tooltip formatters for Highcharts charts in Python just like any other event handler. Let's look at a concrete example.

```python
import justpy as jp

my_chart_def = """
{
    chart: {
        type: 'column'
    },
    title: {
        text: 'Tourists in Middle Earth'
        },
    xAxis: {
        categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    },
    series: [{
        name: "Tourists in '000",
        data: [29.9, 71.5, 106.4, 129.2, 144.0, 176.0, 135.6, 148.5, 216.4, 194.1, 95.6, 54.4]
    }]
}
"""

async def tooltip_formatter1(self, msg):
    return await self.tooltip_update('<div>My tooltip!</div>', msg.websocket)

def chart_test1():
    wp = jp.WebPage()
    # First chart
    wp.css = '.h-chart {height: 300px;}'
    chart1 = jp.HighCharts(a=wp, classes='m-2 p-2 border w-1/2', options=my_chart_def)
    chart1.options.subtitle.text = 'Default Tooltip'
    # Second chart
    chart2 = jp.HighCharts(a=wp, classes='m-2 p-2 border w-1/2', options=my_chart_def)
    chart2.options.subtitle.text = 'Custom Tooltip'
    chart2.on('tooltip', tooltip_formatter1)
    return wp

jp.justpy(chart_test1)
```

In this example we put two charts on the page. They are identical except for their subtitle and the fact that that the second one has a custom tooltip formatter. 

The tooltip formatting function (the handler for the tooltip event) is called `tooltip_formatter1` and has one line in it:

```python
return await self.tooltip_update('<div>My tooltip!</div>', msg.websocket)
```

This line returns the result of running the method `tooltip_update` of the HighCharts component. The method has two arguments (in addition to self). The first is an HTML string which determines the content of the tooltip and the second is the websocket over which this HTML needs to be transmitted. The websocket of the page on which the event occurred can be found in `msg.websocket` and this is the websocket we use (`msg` is the second argument of the event handler).

!!! note
    Since the method `tooltip_update` is a coroutine, it needs be awaited and the tooltip event handler needs to be defined with the keyword async.

## Tooltip Debouncing

If you quickly mouseover several points on charts with user defined formatters, you will see the "Loading…" inscription instead of the information you expect. Only when no new tooltip event occurs for 100ms (0.1 second), JustPy notifies its backend that a tooltip event has happened. This prevents the server from being inundated with irrelevant tooltip requests as the user moves the mouse over the chart.

The debouncing delay can be changed by setting the attribute `tooltip_debounce` which is by default 100ms. The following command changes the debounce period to 500ms:

```python
chart2.tooltip_debounce = 500  # Assign value of debounce period in ms
```
 

## Using Point Data to Format Tooltip

So far, the tooltip we return for all points is the same. That is not very interesting. We would like the tooltip to be much more descriptive.

The second argument to the tooltip formatter (`msg` in our case) has values specific to tooltip events to assist us with this. In addition to the usual fields it contains the fields:
- `msg.x` - The x coordinate of the point
- `msg.category` - If the x value is not a number, for example 'Jan' or 'Feb', it will show up here
- `msg.y` - The y coordinate of the point
- `msg.color` - The color of the point
- `msg.series_name` - The name of the series the point is in
- `msg.series_index` - The index of the series the point is in
- `msg.point_index` - The index of the point in its series

Let's use some of the fields above to create a more informative tooltip. Please replace `tooltip_formatter1` with this new version and run the program:

```python
async def tooltip_formatter2(self, msg):
    tooltip_html = f"""
    <div style="color: {msg.color};">{msg.series_name}</div>
    <div>{msg.category}</div>
    <div>x: {msg.x}, y: {msg.y}</div>
    """
    return await self.tooltip_update(tooltip_html, msg.websocket)
```

We use the Python f-string template like features to create a tooltip that includes information about each point. Notice how `msg.color` is used to give the series name the color of the point. In charts with multiple series, this becomes very useful.

There is another way to create the HTML string used to update the tooltip. Try using the following `tooltip_formatter2` instead of the one above:
```python
async def tooltip_formatter3(self, msg):
    d1 = jp.Div(text=msg.series_name, style=f'color: {msg.color};')
    d2 = jp.Div(text=msg.category)
    d3 = jp.Div(text=f'x: {msg.x}, y: {msg.y}')
    tooltip_html = d1.to_html() + d2.to_html() + d3.to_html()
    return await self.tooltip_update(tooltip_html, msg.websocket)
```

This time we create JustPy components and then use the `to_html()` method to convert them to HTML. Both methods work well and you should use the one you are most comfortable with.


## Tooltip Positioning

You may have noticed in the example above, that the tooltip covers part of the column instead of showing up above it. When we create custom tooltips, we need to help Highcharts position them correctly. We do this using the `tooltip_x` and `tooltip_y` attributes of the JustPy HighCharts class. These attributes determine the offset in pixels for the tooltip relative to where Higcharts estimates it needs to show it. In practice, you will need to experiment with different values to get the positioning you want.

Here is the same example as above but with the tooltip position changed:

```python
import justpy as jp

my_chart_def = """
{
    chart: {
        type: 'column'
    },
    title: {
        text: 'Tourists in Middle Earth'
        },
    xAxis: {
        categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    },
    series: [{
        name: "Tourists in '000",
        data: [29.9, 71.5, 106.4, 129.2, 144.0, 176.0, 135.6, 148.5, 216.4, 194.1, 95.6, 54.4]
    }
    ]
}
"""

async def tooltip_formatter4(self, msg):
    tooltip_html = f"""
    <div style="color: {msg.color};">{msg.series_name}</div>
    <div>{msg.category}</div>
    <div>x: {msg.x} y: {msg.y}</div>
    """
    return await self.tooltip_update(tooltip_html, msg.websocket)

def chart_test2():
    wp = jp.WebPage()
    # First chart
    chart1 = jp.HighCharts(a=wp, classes='m-2 p-2 border w-1/2', options=my_chart_def)
    chart1.options.subtitle.text = 'Default Tooltip'

    # Second chart
    chart2 = jp.HighCharts(a=wp, classes='m-2 p-2 border w-1/2', options=my_chart_def)
    chart2.options.subtitle.text = 'Custom Tooltip'
    chart2.on('tooltip', tooltip_formatter4)
    chart2.tooltip_y = 80
    chart2.tooltip_x = -55
    return wp

jp.justpy(chart_test2)
```

We added the lines:
```python
    chart2.tooltip_y = 80
    chart2.tooltip_x = -55
```
to get the desired positioning. 

## Fixed Tooltip

A tooltip can be fixed to one position. This is done by setting the chart attribute `tooltip_fixed` to `True`. When the tooltip is fixed, `tooltip_x` and `tooltip_y` designate the absolute position in the chart to place the tooltip. 

Here is the example above but this time with a fixed tooltip:

```python
import justpy as jp

my_chart_def = """
{
    chart: {
        type: 'column'
    },
    title: {
        text: 'Tourists in Middle Earth'
        },
    xAxis: {
        categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    },
    series: [{
        name: "Tourists in '000",
        data: [29.9, 71.5, 106.4, 129.2, 144.0, 176.0, 135.6, 148.5, 216.4, 194.1, 95.6, 54.4]
    }
    ]
}
"""

async def tooltip_formatter5(self, msg):
    tooltip_html = f"""
    <div style="color: {msg.color};">{msg.series_name}</div>
    <div>{msg.category}</div>
    <div>x: {msg.x} y: {msg.y}</div>
    """
    return await self.tooltip_update(tooltip_html, msg.websocket)

def chart_test3():
    wp = jp.WebPage()
    # First chart
    chart1 = jp.HighCharts(a=wp, classes='m-2 p-2 border w-1/2', options=my_chart_def)
    chart1.options.subtitle.text = 'Default Tooltip'

    # Second chart
    chart2 = jp.HighCharts(a=wp, classes='m-2 p-2 border w-1/2', options=my_chart_def)
    chart2.options.subtitle.text = 'Custom Tooltip'
    chart2.on('tooltip', tooltip_formatter5)
    chart2.tooltip_fixed = True
    chart2.tooltip_y = 100
    chart2.tooltip_x = 100
    return wp

jp.justpy(chart_test3)
```

The lines that make the difference are:
```python
    chart2.tooltip_fixed = True
    chart2.tooltip_y = 100
    chart2.tooltip_x = 100
```

## Shared and Split Tooltips

### Default Tooltips

Highcharts supports shared and split tooltips in addition to the regular tooltip. To see the difference between the three, run the example below which includes the same chart three times, each time with a different kind of tooltip. This is how the Highcharts default tooltip looks like.

```python
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

jp.justpy(tool_tip_demo1)
```

### Custom Tooltips

In the example below we add three additional charts with custom tooltips to the page. In total, there are now six charts on the page. The first three use the default Highcharts tooltip and the second three use custom tooltips. The first custom tooltip is of type single, the second is of type shared and the third is a split tooltip.

For single and shared tooltip handlers the first argument of the  `tooltip_update` is an HTML string. For split tooltip the first argument is a list of HTML strings. The first string is for the x value and the following strings on the list are the HTML strings per series.

In the case of shared and split tooltips, the `msg` argument of the tooltip formatter includes a list of the properties of all the points with the corresponding x value. It is accessed as `msg.points`. As you will see in the example below, we iterate over this list in the tooltip handlers to generate the required output.


```python
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


def tool_tip_demo2():
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

    jp.Div(text='Charts with user defined tooltip formatter functions',
           classes='m-2 p-2 text-xl bg-blue-500 text-white', a=wp)
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
    tooltip_html = f"""
    <div class="text-red-500">
    <div><span style="color: {msg.color}">&#x25CF;&nbsp;</span>{msg.series_name}</div>
    <div>Year: {msg.x}</div>
    <div>Number of employees: {"{:,}".format(msg.y)}</div>
    </div>
    """
    return await self.tooltip_update(tooltip_html, msg.websocket)


async def shared_tooltip_formatter(self, msg):
    tooltip_div = jp.Div(classes="text-white bg-blue-400")
    jp.Span(text=f'Year: {msg.x}', classes='text-lg', a=tooltip_div)
    for point in msg.points:
        point_div = jp.Div(a=tooltip_div)
        jp.Span(text=f'&#x25CF; {point.series_name}', classes='bg-white', style=f'color: {point.color}', a=point_div)
        jp.Span(text=f'Number of employees: {"{:,}".format(point.y)}', a=point_div)
    return await self.tooltip_update(tooltip_div.to_html(), msg.websocket)


async def split_tooltip_formatter(self, msg):
    tooltip_array = [f'The x value is {msg.x}']
    for point in msg.points:
        point_div = jp.Div()
        jp.Span(text='&#x25CF;', classes='bg-white', style=f'color: {point.color}', a=point_div)
        jp.Span(text=f'{point.series_name}', a=point_div)
        jp.Span(text=f'Year: {point.x}', a=point_div)
        jp.Span(text=f'Number of employees: {"{:,}".format(point.y)}', a=point_div)
        tooltip_array.append(point_div.to_html())
    return await self.tooltip_update(tooltip_array, msg.websocket)


jp.justpy(tool_tip_demo2)
```

The `split_tooltip_formatter` function is a little more complex as can be seen above. A split tooltip means that each series has its own separate popup box and therefore the HTML for each series needs to be returned. The `tooltip_update` method therefore takes as its first argument a list of strings instead of a string as in the other cases. The first string in the list represents the HTML for the x axis value. 
