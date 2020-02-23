from justpy import *


s1 = """
{
    chart: {
        plotBackgroundColor: null,
        plotBorderWidth: 0,
        plotShadow: false
    },
    title: {
        text: 'Browser<br>shares<br>2017',
        align: 'center',
        verticalAlign: 'middle',
        y: 40
    },
    tooltip: {
        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
    },
    plotOptions: {
        pie: {
            dataLabels: {
                enabled: true,
                distance: -50,
                style: {
                    fontWeight: 'bold',
                    color: 'white'
                }
            },
            startAngle: -90,
            endAngle: 90,
            center: ['50%', '75%'],
            size: '110%'
        }
    },
    series: [{
        type: 'pie',
        name: 'Browser share',
        innerSize: '50%',
        data: [
            ['Chrome', 5.89],
            ['Firefox', 13.29],
            ['Internet Explorer', 13],
            ['Edge', 3.78],
            ['Safari', 3.42],
            {
                name: 'Other',
                y: 7.61,
                dataLabels: {
                    enabled: false
                }
            }
        ]
    }]
}

"""

def pie_chart(request):
    wp = WebPage()
    Hello(a=wp)
    d = Div(classes='flex flex-wrap', a=wp)
    charts = [s1] #, s4, var_pie]
    for chart in charts:
        my_chart = HighCharts(a=d)
        my_chart.load_json(chart)
        my_chart.on('tooltip', simple_tooltip)
    return wp

async def simple_tooltip(self, msg):
    print(msg)
    return await self.tooltip_update('hello', get_websocket(msg))
    # await asyncio.sleep(0.2) # Uncomment to simulate 200ms communication delay
    s1 = f'<span class="bg-white" style="color: {msg.color}">&#x25CF;</span>'
    div1 = f'<div>My formatter:</div>'
    div2 = f'<div>{s1}{msg.series_name}</div>'
    div3 = f'<div>Year: {msg.x}</div>'
    div4 = f'<div>Number of employees: {"{:,}".format(msg.y)}</div>'
    tooltip_div = f'<div class="text-white bg-blue-800 text-lg"> {div1}{div2}{div3}{div4}</div>'
    # await websocket.send_json({'type': 'tooltip_update', 'data': tooltip_div, 'id': msg.id})
    return await self.tooltip_update(tooltip_div, get_websocket(msg))


justpy(pie_chart)
