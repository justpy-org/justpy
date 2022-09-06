# Justpy Tutorial demo stock_test2 from docs/charts_tutorial/stock_charts.md
import justpy as jp
import pandas as pd
import datetime

epoch = datetime.datetime(1970, 1, 1)
grouping_units = [["week", [1]], ["month", [1, 2, 3, 4, 6]]]

chart_dict = {
    "rangeSelector": {"selected": 1},
    "yAxis": [
        {
            "labels": {"align": "right", "x": -3},
            "title": {"text": "OHLC"},
            "height": "60%",
            "lineWidth": 2,
            "resize": {"enabled": True},
        },
        {
            "labels": {"align": "right", "x": -3},
            "title": {"text": "Volume"},
            "top": "65%",
            "height": "35%",
            "offset": 0,
            "lineWidth": 2,
        },
    ],
    "tooltip": {"split": True},
    "series": [
        {
            "type": "candlestick",
            "tooltip": {"valueDecimals": 2},
            "dataGrouping": {"units": grouping_units},
        },
        {
            "type": "column",
            "name": "Volume",
            "yAxis": 1,
            "dataGrouping": {"units": grouping_units},
        },
    ],
}


def convert_date2(date_string):
    date = datetime.datetime.strptime(date_string, "%Y-%m-%d")
    return (date - epoch).total_seconds() * 1000


async def stock_test2(request):
    wp = jp.WebPage(highcharts_theme="grid")
    ticker = request.query_params.get("ticker", "MSFT").upper()
    if ticker not in ["AAPL", "IBM", "INTC", "MSFT"]:
        ticker = "MSFT"
    data = await jp.JustPy.loop.run_in_executor(
        None, pd.read_csv, f"https://elimintz.github.io/stocks/{ticker}.csv"
    )
    chart = jp.HighStock(
        a=wp,
        classes="m-1 p-2 border w-10/12",
        options=chart_dict,
        style="height: 600px",
    )
    o = chart.options
    o.title.text = f"{ticker} Historical Prices"
    x = list(data["Date"].map(convert_date2))
    o.series[0].data = list(
        zip(x, data["Open"], data["High"], data["Low"], data["Close"])
    )
    o.series[0].name = ticker
    o.series[1].data = list(zip(x, data["Volume"]))
    return wp


# initialize the demo
from examples.basedemo import Demo

Demo("stock_test2", stock_test2)
