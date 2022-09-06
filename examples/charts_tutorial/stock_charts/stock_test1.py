# Justpy Tutorial demo stock_test1 from docs/charts_tutorial/stock_charts.md
import justpy as jp
import pandas as pd
import datetime

epoch = datetime.datetime(1970, 1, 1)


def convert_date1(date_string):
    date = datetime.datetime.strptime(date_string, "%Y-%m-%d")
    return (date - epoch).total_seconds() * 1000


def stock_test1(request):
    wp = jp.WebPage()
    ticker = request.query_params.get("ticker", "MSFT")
    if ticker not in ["AAPL", "IBM", "INTC", "MSFT"]:
        ticker = "MSFT"
    data = pd.read_csv(f"https://elimintz.github.io/stocks/{ticker.upper()}.csv")
    chart = jp.HighStock(a=wp, classes="m-1 p-2 border w-10/12")
    o = chart.options
    o.title.text = "Historical Stock Price"
    o.legend = {"enabled": True, "align": "right", "layout": "proximate"}
    o.rangeSelector.selected = 4  # Set default range to 1 year
    x = list(data["Date"].map(convert_date1))
    y = data["Adj Close"].to_list()
    s = jp.Dict({"name": ticker.upper(), "data": jp.make_pairs_list(x, y)})
    o.series = [s]
    s.tooltip.valueDecimals = 2  # Price displayed by tooltip will have 2 decimal values
    return wp


# initialize the demo
from examples.basedemo import Demo

Demo("stock_test1", stock_test1)
