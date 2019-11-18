from justpy import *
# import demjson
# from types import SimpleNamespace
import numpy as np
import datetime

s3 = """
{
 chart: {
        
        type: 'spline'
        
    },
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
s4 = """
{
    chart: {
        type: 'spline',
        scrollablePlotArea: {
            minWidth: 600,
            scrollPositionX: 1
        }
    },
    title: {
        text: 'Wind speed during two days',
        align: 'left'
    },
    subtitle: {
        text: '13th & 14th of February, 2018 at two locations in Vik i Sogn, Norway',
        align: 'left'
    },
    xAxis: {
        type: 'datetime',
        labels: {
            overflow: 'justify'
        }
    },
    yAxis: {
        title: {
            text: 'Wind speed (m/s)'
        },
        minorGridLineWidth: 0,
        gridLineWidth: 0,
        alternateGridColor: null,
        plotBands: [{ // Light air
            from: 0.3,
            to: 1.5,
            color: 'rgba(68, 170, 213, 0.1)',
            label: {
                text: 'Light air',
                style: {
                    color: '#606060'
                }
            }
        }, { // Light breeze
            from: 1.5,
            to: 3.3,
            color: 'rgba(0, 0, 0, 0)',
            label: {
                text: 'Light breeze',
                style: {
                    color: '#606060'
                }
            }
        }, { // Gentle breeze
            from: 3.3,
            to: 5.5,
            color: 'rgba(68, 170, 213, 0.1)',
            label: {
                text: 'Gentle breeze',
                style: {
                    color: '#606060'
                }
            }
        }, { // Moderate breeze
            from: 5.5,
            to: 8,
            color: 'rgba(0, 0, 0, 0)',
            label: {
                text: 'Moderate breeze',
                style: {
                    color: '#606060'
                }
            }
        }, { // Fresh breeze
            from: 8,
            to: 11,
            color: 'rgba(68, 170, 213, 0.1)',
            label: {
                text: 'Fresh breeze',
                style: {
                    color: '#606060'
                }
            }
        }, { // Strong breeze
            from: 11,
            to: 14,
            color: 'rgba(0, 0, 0, 0)',
            label: {
                text: 'Strong breeze',
                style: {
                    color: '#606060'
                }
            }
        }, { // High wind
            from: 14,
            to: 15,
            color: 'rgba(68, 170, 213, 0.1)',
            label: {
                text: 'High wind',
                style: {
                    color: '#606060'
                }
            }
        }]
    },
    tooltip: {
        valueSuffix: ' m/s'
    },
    plotOptions: {
        spline: {
            lineWidth: 4,
            states: {
                hover: {
                    lineWidth: 5
                }
            },
            marker: {
                enabled: false
            },
            pointInterval: 3600000, // one hour
            //pointStart: Date.UTC(2018, 1, 13, 0, 0, 0)
        }
    },
    series: [{
        name: 'Hestavollane',
        data: [
            3.7, 3.3, 3.9, 5.1, 3.5, 3.8, 4.0, 5.0, 6.1, 3.7, 3.3, 6.4,
            6.9, 6.0, 6.8, 4.4, 4.0, 3.8, 5.0, 4.9, 9.2, 9.6, 9.5, 6.3,
            9.5, 10.8, 14.0, 11.5, 10.0, 10.2, 10.3, 9.4, 8.9, 10.6, 10.5, 11.1,
            10.4, 10.7, 11.3, 10.2, 9.6, 10.2, 11.1, 10.8, 13.0, 12.5, 12.5, 11.3,
            10.1
        ]

    }, {
        name: 'Vik',
        data: [
            0.2, 0.1, 0.1, 0.1, 0.3, 0.2, 0.3, 0.1, 0.7, 0.3, 0.2, 0.2,
            0.3, 0.1, 0.3, 0.4, 0.3, 0.2, 0.3, 0.2, 0.4, 0.0, 0.9, 0.3,
            0.7, 1.1, 1.8, 1.2, 1.4, 1.2, 0.9, 0.8, 0.9, 0.2, 0.4, 1.2,
            0.3, 2.3, 1.0, 0.7, 1.0, 0.8, 2.0, 1.2, 1.4, 3.7, 2.1, 2.0,
            1.5
        ]
    }],
    navigation: {
        menuItemStyle: {
            fontSize: '10px'
        }
    }
}
"""
var_pie = """
{
    chart: {
        type: 'variablepie'
    },
    title: {
        text: 'Countries compared by population density and total area.'
    },
    tooltip: {
        headerFormat: '',
        pointFormat: '<span style="color:{point.color}">\\u25CF</span> <b> {point.name}</b><br/>Area (square km): <b>{point.y}</b><br/>Population density (people per square km): <b>{point.z}</b><br/>'
    },
    series: [{
        minPointSize: 10,
        innerSize: '20%',
        zMin: 0,
        name: 'countries',
        data: [{
            name: 'Spain',
            y: 505370,
            z: 92.9
        }, {
            name: 'France',
            y: 551500,
            z: 118.7
        }, {
            name: 'Poland',
            y: 312685,
            z: 124.6
        }, {
            name: 'Czech Republic',
            y: 78867,
            z: 137.5
        }, {
            name: 'Italy',
            y: 301340,
            z: 201.8
        }, {
            name: 'Switzerland',
            y: 41277,
            z: 214.5
        }, {
            name: 'Germany',
            y: 357022,
            z: 235.6
        }]
    }]
}
"""
s5 = """
{
    chart: {
    width: 1000
    },
    title: {
        text: 'Monthly temperatures in a random cold place'
    },
    subtitle: {
        text: 'All series should be blue below zero'
    },
    xAxis: {
        type: 'datetime'
    },
    plotOptions: {
        series: {
            className: 'main-color',
            negativeColor: true
        }
    },
    series: [{
        name: 'Spline',
        type: 'spline',
        data: [-6.4, -5.2, -3.0, 0.2, 2.3, 5.5, 8.4, 8.3, 5.1, 0.9, -1.1, -4.0],
        pointStart: 1262304000000,
        pointInterval: 2592000000‬
    }, {
        name: 'Area',
        type: 'area',
        data: [-6.4, -5.2, -3.0, 0.2, 2.3, 5.5, 8.4, 8.3, 5.1, 0.9, -1.1, -4.0],
        pointStart: 1293840000000,
        pointInterval: 2592000000‬
    }, {
        name: 'Column',
        type: 'column',
        data: [-6.4, -5.2, -3.0, 0.2, 2.3, 5.5, 8.4, 8.3, 5.1, 0.9, -1.1, -4.0],
        pointStart: 1325376000000,
        pointInterval: 2592000000‬
    }]
}
"""

def chart_click(self, msg):
    print('in chart', msg)
    self.options.title.text += 'clicked'
    return
    chart_types = ['area', 'arearange', 'areaspline', 'bar', 'bellcurve', 'column', ]
    self.chart.options.title.text = HighCharts.chart_types[self.index]
    self.chart.options.chart.type = HighCharts.chart_types[self.index]
    self.index += 1

async def my_tooltip(self, msg):
    print(msg)
    # await asyncio.sleep(0.2)
    websocket = get_websocket(msg)
    s1 = f'<span style="color: {msg.color}">&#x25CF;</span>'
    div1 = f'<div>{s1} My formatter:</div>'
    div2 = f'<div>{msg.series_name}</div>'
    div3 = f'<div>Year: {msg.x}</div>'
    div4 = f'<div>Number of employees: {"{:,}".format(msg.y)}</div>'
    tooltip_div = f'<div class="text-white bg-blue-800 text-lg"> {div1}{div2}{div3}{div4}</div>'
    await websocket.send_json({'type': 'tooltip_update', 'data': tooltip_div, 'id': msg.id})
    return True

async def my_shared_tooltip(self, msg):
    print(msg.points)

    return_string = ''
    print('x', msg.x)
    for point in msg.points:
        # return_string += f'<div style="font-size:10px">{point["series_name"]}   {point["x"]} {point["y"]}</div>'
        #<span style="color:' + this.point.color + '">\u25CF</span>
        #<span style="color:' + this.point.color + '">&#x25CF;</span>
        # s1 = f'<span style="color: {point.color}">&#x25CF;</span>'
        s1 = f'<span style="color: {point.color}">&#129409;</span>'
        return_string += f'<div style="font-size:12px"> {s1} {point.series_name}   {point.x} {point.y}</div>'
    # await asyncio.sleep(0.2)
    websocket = get_websocket(msg)
    # await websocket.send_json({'type': 'tooltip_update', 'data': f'<span style="font-size:20px">Daniel {msg.series_name} {msg.x} {msg.y}</span>', 'id': msg.id})
    print(return_string)
    await websocket.send_json({'type': 'tooltip_update', 'data': return_string, 'id': msg.id})
    return True

async def my_split_tooltip(self, msg):
    # When split a list is returned. First item in list is the x axis tooltip. Then for each series
    print(msg.points)
    print(msg)
    return_list = [f'Year: {msg.x}']
    print('x', msg.x)
    for point in msg.points:
        s1 = f'<span style="color: {point.color}">&#129409;</span>'
        s1 = f'<div style="font-size:12px"> {s1} {point.series_name}   {point.x} {point.y}</div>'
        return_list.append(s1)
    # await asyncio.sleep(0.2)
    websocket = get_websocket(msg)
    # await websocket.send_json({'type': 'tooltip_update', 'data': f'<span style="font-size:20px">Daniel {msg.series_name} {msg.x} {msg.y}</span>', 'id': msg.id})
    print(return_list)
    await websocket.send_json({'type': 'tooltip_update', 'data': return_list, 'id': msg.id})
    return True


def add_point(self, msg):
    series = self.chart.options.series
    print(self.chart.events)
    print(series[0])
    series[0].data.append(30000)

def chart_test(request):
    wp = WebPage()
    Hello(a=wp)
    d = Div(classes='flex flex-wrap', a=wp)
    charts = [var_pie] #, s4, var_pie]
    for chart in charts:
        my_chart = HighCharts()

        my_chart.load_json(chart)
        my_chart.options.title.text = 'My Chart'
        my_chart.options.tooltip.shared = False
        # my_chart.options.tooltip.split = True
        my_chart.on('tooltip', my_tooltip)
        # my_chart.on('point_click', chart_click)
        print(my_chart.options)
        d.add(my_chart)
    b = Button(text='click me', classes='shadow m-2', click=add_point, a=wp)
    b.index = 0
    b.chart = my_chart

    return wp

@SetRoute('/tooltip')
def tool_tip_demo(request):
    wp = WebPage()
    d = Div(classes='flex flex-wrap ', a=wp)
    charts = [s3, s3, s3]
    my_charts = []
    for chart in charts:
        my_chart = HighCharts(a=d, classes='m-2 p-2 border')
        my_charts.append(my_chart)
        my_chart.load_json(chart)

        # my_chart.on('tooltip', my_shared_tooltip)
    my_charts[0].options.tooltip.shared = False
    my_charts[1].options.tooltip.shared = True
    my_charts[2].options.tooltip.split = True
    my_charts[0].options.title.text = 'Simple Tooltip'
    my_charts[1].options.title.text = 'Shared Tooltip'
    my_charts[2].options.title.text = 'Split Tooltip'

    d = Div(classes='flex flex-wrap', a=wp)
    charts = [s3, s3, s3]
    my_charts = []
    for chart in charts:
        my_chart = HighCharts(a=d, classes='m-2 p-2 border')
        my_charts.append(my_chart)
        my_chart.load_json(chart)


    my_charts[0].options.tooltip.shared = False
    my_charts[0].on('tooltip', my_tooltip)

    my_charts[1].options.tooltip.shared = True
    my_charts[1].on('tooltip', my_shared_tooltip)
    my_charts[2].options.tooltip.split = True
    my_charts[2].on('tooltip', my_split_tooltip)
    my_charts[0].options.title.text = 'Simple Tooltip - Formatter Example'
    my_charts[1].options.title.text = 'Shared Tooltip - Formatter Example'
    my_charts[2].options.title.text = 'Split Tooltip - Formatter Example'

    return wp

@SetRoute('/stock')
async def stock_chart(request):
    wp = WebPage()
    wp.highcharts_theme = 'grid-light'
    d = Div(classes='flex flex-wrap', a=wp)
    tickers = request.query_params.get('ticker', 'aapl')
    print(tickers)
    tick_list = tickers.split(',')
    print(tick_list)
    chart = HighStock(a=d, classes='border m-4')
    chart.options = Dict({'series': []})
    co = chart.options
    co.title.text = tickers.upper()
    for ticker in tick_list:
        print(f'https://api.iextrading.com/1.0/stock/{ticker}/chart?range=5y')
        # data = await get(f'https://api.iextrading.com/1.0/stock/{ticker}/chart?range=5y')
        with open('quotes.txt') as f:
            data = json.loads(f.read())
        s = []
        for i in data:
            quote_date = datetime.datetime.strptime(i['date'], '%Y-%m-%d')
            epoch_time = quote_date.timestamp() * 1000  # javascript time is milisecods not seconds
            s.append([epoch_time, i['open'], i['high'], i['low'], i['close']])
        temp = Dict()
        temp.name = ticker.upper()
        temp.data = s
        temp.tooltip.valueDecimals = 2
        temp.type = 'candlestick'
        co.series.append(temp)
        # co.series[0].name = ticker.upper()
        # co.series[0].data = s
        # co.series[0].tooltip.valueDecimals = 2
    chart1 = HighStock(a=d, classes='border m-4')
    chart1.options = chart.options

    return wp


def sine_together(request):
    wp = WebPage()
    a = demjson.decode("""
    {legend: {
        align: 'left',
        verticalAlign: 'top',
        layout: 'vertical',
        x: 0,
        y: 100
    }}
    """)
    b = """
    {legend: {
        align: 'right',
        verticalAlign: 'top',
        layout: 'vertical',
        x: 0,
        y: 0
    }}
    """
    # co = Dict({'legend': {'align': 'left', 'verticalAlign': 'top', 'layout': 'vertical', 'x': 0, 'y': 100}})
    # co = Dict(a)
    # co = Dict()
    # co['legend'] = Dict({'align': 'left', 'verticalAlign': 'top', 'layout': 'vertical', 'x': 0, 'y': 100})
    # co.legend.align = 'right'
    # co.legend.x = -50
    g = HighCharts( a=wp, classes='m-1 w-1/2')
    g.load_json(b)
    co = g.options
    co.legend.align = 'right'
    co.legend.layout = 'proximate'
    co.chart.type = 'spline'
    # co.chart.width = 600
    co.title.text = 'Sine Graph'
    # co.legend.layout = 'vertical'
    # co.legend.align = 'right'
    # co.legend.verticalAlign = 'top'
    # co.legend.x = 0
    # co.legend.y = 50
    a = {'legend': {'align': 'right', 'verticalAlign': 'top', 'layout': 'vertical', 'x': 0, 'y': 100}}
    x = np.linspace(-np.pi, 1.2*np.pi, 201)
    sinx = np.sin(x)
    co.series = []
    for f in range(1,6):
        s = Dict()
        s.name = f'Cycle {f}'
        sinx = np.sin(f * x)
        s.data = [list(i) for i in zip(x, sinx)]
        co.series.append(s)


    return wp


def sine_alone(request):
    wp = WebPage()
    d = Div(classes='flex flex-wrap', a=wp)
    x = np.linspace(-np.pi, np.pi, 201)

    for f in range(1,50):
        co = Dict()
        g = HighCharts(options=co, a=d, classes='m-1 border')
        co.chart.type = 'area'
        co.title.text = 'Sine Graph'
        co.series = []
        s = Dict()
        s.name = f'Cycle {f}'
        sinx = np.sin(f * x)
        s.data = [list(i) for i in zip(x, sinx)]
        co.series.append(s)
    return wp

def file_load_test_histogram(request):
    wp = WebPage()
    g = HighCharts(a=wp)
    co = g.load_json_from_file('highcharts/histogram.txt')
    data = [3.5, 3, 3.2, 3.1, 3.6, 3.9, 3.4, 3.4, 2.9, 3.1, 3.7, 3.4, 3, 3, 4, 4.4, 3.9, 3.5, 3.8, 3.8, 3.4, 3.7, 3.6,
            3.3, 3.4, 3, 3.4, 3.5, 3.4, 3.2, 3.1, 3.4, 4.1, 4.2, 3.1, 3.2, 3.5, 3.6, 3, 3.4, 3.5, 2.3, 3.2, 3.5, 3.8, 3,
            3.8, 3.2, 3.7, 3.3, 3.2, 3.2, 3.1, 2.3, 2.8, 2.8, 3.3, 2.4, 2.9, 2.7, 2, 3, 2.2, 2.9, 2.9, 3.1, 3, 2.7, 2.2,
            2.5, 3.2, 2.8, 2.5, 2.8, 2.9, 3, 2.8, 3, 2.9, 2.6, 2.4, 2.4, 2.7, 2.7, 3, 3.4, 3.1, 2.3, 3, 2.5, 2.6, 3,
            2.6, 2.3, 2.7, 3, 2.9, 2.9, 2.5, 2.8, 3.3, 2.7, 3, 2.9, 3, 3, 2.5, 2.9, 2.5, 3.6, 3.2, 2.7, 3, 2.5, 2.8,
            3.2, 3, 3.8, 2.6, 2.2, 3.2, 2.8, 2.8, 2.7, 3.3, 3.2, 2.8, 3, 2.8, 3, 2.8, 3.8, 2.8, 2.8, 2.6, 3, 3.4, 3.1,
            3, 3.1, 3.1, 3.1, 2.7, 3.2, 3.3, 3, 2.5, 3, 3.4, 3]
    co.series[1].data = data
    print(co)
    return wp

def file_load_test(request):
    wp = WebPage()
    g = HighCharts(a=wp)
    co = g.load_json_from_file('highcharts/streamgraph.txt')

    print(co)
    return wp

@SetRoute('/histogram')
def test_histogram(request):
    wp = WebPage()
    data = [3.5, 3, 3.2, 3.1, 3.6, 3.9, 3.4, 3.4, 2.9, 3.1, 3.7, 3.4, 3, 3, 4, 4.4, 3.9, 3.5, 3.8, 3.8, 3.4, 3.7, 3.6,
            3.3, 3.4, 3, 3.4, 3.5, 3.4, 3.2, 3.1, 3.4, 4.1, 4.2, 3.1, 3.2, 3.5, 3.6, 3, 3.4, 3.5, 2.3, 3.2, 3.5, 3.8, 3,
            3.8, 3.2, 3.7, 3.3, 3.2, 3.2, 3.1, 2.3, 2.8, 2.8, 3.3, 2.4, 2.9, 2.7, 2, 3, 2.2, 2.9, 2.9, 3.1, 3, 2.7, 2.2,
            2.5, 3.2, 2.8, 2.5, 2.8, 2.9, 3, 2.8, 3, 2.9, 2.6, 2.4, 2.4, 2.7, 2.7, 3, 3.4, 3.1, 2.3, 3, 2.5, 2.6, 3,
            2.6, 2.3, 2.7, 3, 2.9, 2.9, 2.5, 2.8, 3.3, 2.7, 3, 2.9, 3, 3, 2.5, 2.9, 2.5, 3.6, 3.2, 2.7, 3, 2.5, 2.8,
            3.2, 3, 3.8, 2.6, 2.2, 3.2, 2.8, 2.8, 2.7, 3.3, 3.2, 2.8, 3, 2.8, 3, 2.8, 3.8, 2.8, 2.8, 2.6, 3, 3.4, 3.1,
            3, 3.1, 3.1, 3.1, 2.7, 3.2, 3.3, 3, 2.5, 3, 3.4, 3]
    g = Histogram(data, a=wp)
    return wp

pie_string = """

{
    chart: {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false,
        width: 600,
        type: 'pie'
    },
    title: {
        text: 'Browser market shares in January, 2018'
    },
    tooltip: {
        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
    },
    plotOptions: {
        pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
                enabled: true,
                format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                
            }
        }
    },
    series: [{
        name: 'Brands',
        colorByPoint: true,
        data: [{
            name: 'Chrome',
            y: 61.41,
            sliced: true,
            selected: true
        }, {
            name: 'Internet Explorer',
            y: 11.84
        }, {
            name: 'Firefox',
            y: 10.85
        }, {
            name: 'Edge',
            y: 4.67
        }, {
            name: 'Safari',
            y: 4.18
        }, {
            name: 'Sogou Explorer',
            y: 1.64
        }, {
            name: 'Opera',
            y: 1.6
        }, {
            name: 'QQ',
            y: 1.2
        }, {
            name: 'Other',
            y: 2.61
        }]
    }]
}
"""

def pie_test1():

    wp = WebPage()
    g = HighCharts(a=wp)
    co = g.load_json(pie_string)
    return wp

def pie_test():
    wp = WebPage()
    g = Pie([1,2,3,4], ['a','b','c','d'], a=wp, name='Brands')
    print(g.options)
    g = PieSemiCircle([1, 2, 3, 4], ['a', 'b', 'c', 'd'], a=wp, name='Brands')
    g.options.chart.width = 600
    return wp

@SetRoute('/editor')
def editor_chart():
    wp = WebPage()
    ed = TextArea(a=wp, style='width: 50%; height: 300px')
    b = Button(text='Generate Chart', a=wp)
    chart_div = Div(a=wp, classes='w-1/2')
    b.chart_div = chart_div
    b.ed = ed
    def click_btn(self, msg):
        print(self.ed.value)
        c = HighCharts(options=self.ed.value, a=self.chart_div)
        print(c.options)
    b.on('click', click_btn)
    return wp

# justpy(chart_test)
justpy(pie_test)
# justpy(stock_chart)
# justpy(sine_alone)
# justpy(file_load_test)
# justpy(file_load_test_histogram)
# justpy(file_load_test, host='198.199.81.28', port=80, websockets=True)
# justpy(tool_tip_demo)
# justpy(test_histogram)