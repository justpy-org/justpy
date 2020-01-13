import justpy as jp
import pandas as pd
import datetime


grouping_units = [['week', [1]], ['month', [1, 2, 3, 4, 6]]]

chart_dict = {
    'rangeSelector': {'selected': 1},
    'yAxis': [
        {'labels': {'align': 'right', 'x': -3}, 'title': {'text': 'OHLC'}, 'height': '60%', 'lineWidth': 2, 'resize': {'enabled': True}},
        {'labels': {'align': 'right', 'x': -3}, 'title': {'text': 'Volume'}, 'top': '65%', 'height': '35%', 'offset': 0, 'lineWidth': 2}
    ],
    'tooltip': {'split': True},
    'series': [
        {'type': 'candlestick', 'tooltip': {'valueDecimals': 2}, 'dataGrouping': {'units': grouping_units}},
        {'type': 'column', 'name': 'Volume', 'yAxis': 1, 'dataGrouping': {'units': grouping_units}}
    ]
}

epoch = datetime.datetime(1970, 1, 1)

def convert_date(date_string):
    date = datetime.datetime.strptime(date_string, '%Y-%m-%d')
    return (date - epoch).total_seconds()*1000


async def stock_test(request):
    wp = jp.WebPage()
    ticker= 'MSFT'
    data = pd.read_csv(f'https://elimintz.github.io/stocks/{ticker}.csv').round(2)
    chart = jp.HighStock(a=wp, options=chart_dict, style='height: 500px; margin: 0.25rem; padding: 0.5rem; border-width: 1px; border-style: solid; width: 80%;')
    chart.options.title.text = f'{ticker} Historical Prices'
    x = list(data['Date'].map(convert_date))
    chart.options.series[0].data = list(zip(x, data['Open'], data['High'], data['Low'], data['Close']))
    chart.options.series[0].name = ticker
    chart.options.series[1].data = list(zip(x, data['Volume']))
    data.jp.ag_grid(a=wp, style='height: 500px; width: 80%; margin: 0.25rem; ')
    return wp


jp.justpy(stock_test)