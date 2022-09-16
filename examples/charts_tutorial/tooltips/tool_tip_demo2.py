# Justpy Tutorial demo tool_tip_demo2 from docs/charts_tutorial/tooltips.md
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


# initialize the demo
from  examples.basedemo import Demo
Demo ("tool_tip_demo2",tool_tip_demo2)
