from justpy import *
import demjson
# from types import SimpleNamespace
import numpy as np

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
    await websocket.send_json({'type': 'tooltip_update', 'data': f'<span style="font-size:20px">hello eli {msg.series_name} {msg.x} {msg.y}</span>', 'id': msg.id})
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
    charts = [s3] #, s4, var_pie]
    for chart in charts:
        my_chart = HighCharts()
        my_chart.load_json(chart)
        my_chart.on('tooltip', my_tooltip)
        my_chart.on('point_click', chart_click)
        print(my_chart.options)
        d.add(my_chart)
    b = Button(text='click me', classes='shadow m-2', click=add_point, a=wp)
    b.index = 0
    b.chart = my_chart

    return wp

async def stock_chart(request):
    wp = WebPage()
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
    co = Dict()
    g = HighCharts(options=co, a=wp)
    co.chart.type = 'spline'
    co.title.text = 'Sine Graph'
    x = np.linspace(-np.pi, np.pi, 201)
    sinx = np.sin(x)
    co.series = []
    for f in range(1,10):
        s = Dict()
        s.name = f'Cycle {f}'
        sinx = np.sin(f * x)
        s.data = [list(i) for i in zip(x, sinx)]
        co.series.append(s)


    return wp


def sine_alone(request):
    wp = WebPage()
    co = Dict()
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




# justpy(chart_test)
# justpy(stock_chart)
justpy(sine_alone)