import justpy as jp
import pandas as pd
import datetime
import numpy as np

epoch = datetime.datetime(1970, 1, 1)
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

columns = [
    {'name': 'date', 'align': 'left', 'label': 'Date', 'field': 'Date', 'sortable': True},
    {'name': 'open', 'align': 'center', 'label': 'Open', 'field': 'Open', 'sortable': True},
    {'name': 'high', 'align': 'center', 'label': 'High', 'field': 'High', 'sortable': True},
    {'name': 'low', 'align': 'center', 'label': 'Low', 'field': 'Low', 'sortable': True},
    {'name': 'close', 'align': 'center', 'label': 'Close', 'field': 'Close', 'sortable': True},
    {'name': 'volume', 'align': 'center', 'label': 'Volume', 'field': 'Volume', 'sortable': True}
]

def create_columns_def(df):
    columns_def = []
    for col in df.columns:
        columns_def.append({'name': col, 'align': 'center', 'label': col, 'field': col, 'sortable': True})
    return columns_def

def convert_date(date_string):
    date = datetime.datetime.strptime(date_string, '%Y-%m-%d')
    return (date - epoch).total_seconds()*1000


async def stock_test(request):
    wp = jp.QuasarPage(highcharts_theme='grid')
    ticker = request.query_params.get('ticker', 'MSFT').upper()
    try:
        data = await jp.JustPy.loop.run_in_executor(None, pd.read_csv, f'https://elimintz.github.io/stocks/{ticker}.csv')
    except:
        ticker = 'MSFT'
        data = await jp.JustPy.loop.run_in_executor(None, pd.read_csv, f'https://elimintz.github.io/stocks/{ticker}.csv')
    chart = jp.HighStock(a=wp, options=chart_dict, style='height: 500px; margin: 0.25rem; padding: 0.5rem; border-width: 1px; border-style: solid; width: 80%;')
    o = chart.options
    o.title.text = f'{ticker} Historical Prices'
    x = list(data['Date'].map(convert_date))
    o.series[0].data = list(zip(x, data['Open'], data['High'], data['Low'], data['Close']))
    o.series[0].name = ticker
    o.series[1].data = list(zip(x, data['Volume']))
    jp.QTable(title=ticker, data=data.round(2).to_dict('records'), columns=columns, row_key='name', a=wp, dense=True, bordered=True, style='margin: 0.25rem; padding: 0.5rem; width: 80%;')
    return wp


@jp.SetRoute('/sine')
def sine_test():
    wp = jp.WebPage()
    chart = jp.HighCharts(a=wp, classes='border m-2 p-2 w-3/4')
    o = chart.options
    o.title.text = 'Sines Galore'
    x = np.linspace(-np.pi, np.pi, 201)
    o.series = []
    for frequency in range(1,11):
        y = np.sin(frequency * x)
        s = jp.Dict()
        s.name = f'F{frequency}'
        # s.data = jp.make_pairs_list(x, y)
        s.data = list(zip(x, y))
        o.series.append(s)
    return wp

jp.justpy(stock_test)

# jp.justpy(sine_test)
