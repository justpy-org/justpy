# Justpy Tutorial demo stock_test from docs/quasar_tutorial/quasar_components.md
import justpy as jp
from pandas_datareader import data as pdr
import datetime
import functools

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


class QInputDate(jp.QInput):
    """
    Custom Quasar date input field widget
    """

    def __init__(self, **kwargs):
        """
        constructor
        """
        super().__init__(**kwargs)

        date_slot = jp.QIcon(name='event', classes='cursor-pointer')
        c2 = jp.QPopupProxy(transition_show='scale', transition_hide='scale', a=date_slot)
        self.date = jp.QDate(mask='YYYY-MM-DD', name='date', a=c2)

        self.date.parent = self
        self.date.value = self.value
        self.append_slot = date_slot
        self.date.on('input', self.date_time_change)
        self.on('input', self.input_change)
        self.proxy = c2

    @staticmethod
    async def date_time_change(self, msg):
        """
        handle datetime field change
        """
        self.parent.value = self.value
        self.parent.date.value = self.value
        await self.parent.proxy.run_method('hide()', msg.websocket)

    @staticmethod
    def input_change(self, msg):
        """
        handle input field value changes
        """
        self.date.value = self.value


def convert_date(date_string):
    """
    convert given date string to datetime object
    """
    date = datetime.datetime.strptime(str(date_string), '%Y-%m-%d')
    return (date - epoch).total_seconds()*1000


async def get_chart(self, msg):
    """
    handle get_chart button click by retrieving the data from yahoo and displaying it as chart
    """
    self.loading = True
    await msg.page.update()
    self.loading = False
    data_reader = functools.partial(pdr.DataReader, data_source='yahoo', start=self.start_date.value, end=self.end_date.value)
    error_msg = ""
    data = None
    try:
        data = await jp.JustPy.loop.run_in_executor(None, data_reader, self.ticker.value)
        if data is None:
            error_msg = f'No data available for "{self.ticker.value}"'
    except KeyError as e:
            error_msg = f"{self.ticker.value}: Invalid input ({e})"
    except Exception as e:
        error_msg = e
    if data is not None:
        data['Date'] = data.index.astype(str)
        chart = jp.HighStock(a=msg.page, classes='q-ma-md', options=chart_dict, style='height: 600px')
        o = chart.options
        ticker = self.ticker.value
        o.title.text = f'{ticker} Historical Prices'
        x = list(data['Date'].map(convert_date))
        o.series[0].data = list(zip(x, data['Open'], data['High'], data['Low'], data['Close']))
        o.series[0].name = ticker
        o.series[1].data = list(zip(x, data['Volume']))
    self.error_msg.text = error_msg


async def stock_test(request):
    """
    Setup stock test webpage

    Returns:
        stock test webpage
    """
    wp = jp.QuasarPage(highcharts_theme='grid')
    d = jp.Div(classes="q-ma-md q-gutter-md row", a=wp)
    ticker = jp.QInput(label='Ticker', a=d, value='MSFT')
    start_date = QInputDate(a=d, label='Start Date', standout=True, value='2007-01-01')
    end_date = QInputDate(a=d, label='End Date', standout=True, value='2019-12-31')
    b = jp.QBtn(label='Get Chart', a=d, start_date=start_date, end_date=end_date, ticker=ticker, click=get_chart, loading=False)
    b.error_msg = jp.Div(a=wp)
    return wp



# initialize the demo
from examples.basedemo import Demo
Demo("stock_test", stock_test)
