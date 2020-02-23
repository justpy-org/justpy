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
        allowPointSelect: true,
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

    jp.Div(text='Charts with user defined tooltip formatter functions', classes='m-2 p-2 text-xl bg-blue-500 text-white',a =wp)
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
    tooltip_div = f'<div class="text-red-500 text-xl"> {div1}{div2}{div3}{div4}</div>'
    return await self.tooltip_update(tooltip_div, jp.get_websocket(msg))


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
    return await self.tooltip_update(tooltip_div.to_html(), jp.get_websocket(msg))


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
    return await self.tooltip_update(tooltip_array, jp.get_websocket(msg))

jp.justpy(tool_tip_demo)
