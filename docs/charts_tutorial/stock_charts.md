# Stock Charts
In addition to Highcharts, Highsoft offers a great stock charting product called [Highstock](https://www.highcharts.com/blog/products/highstock/). To use Highstock, set the attribute `stock` of an HighCharts instance to `True` or use the HighStock class.

The program below serves a chart of stock price data.

!!! hint
    You need to install pandas to run the program successfully
### Stock Charts price data
[Stock Charts price data live demo]({{demo_url}}/stock_test1)
    

```python
import justpy as jp
import pandas as pd
import datetime

epoch = datetime.datetime(1970, 1, 1)


def convert_date1(date_string):
    date = datetime.datetime.strptime(date_string, "%Y-%m-%d")
    return (date - epoch).total_seconds() * 1000


def stock_test1(request):
    wp = jp.WebPage()
    ticker = request.query_params.get("ticker", "msft")
    if ticker not in ["aapl", "ibm", "intc", "msft"]:
        ticker = "msft"
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


jp.justpy(stock_test1)
```

I used [yahoo finance](https://finance.yahoo.com) to download data in CSV format. The first few lines of the file look like this:
```
Date,Open,High,Low,Close,Adj Close,Volume
2005-01-03,4.627143,4.650714,4.471428,4.520714,3.945287,172998000
2005-01-04,4.556428,4.676429,4.497857,4.567143,3.985806,274202600
2005-01-05,4.604286,4.660714,4.575000,4.607143,4.020715,170108400
2005-01-06,4.619286,4.636428,4.523571,4.610714,4.023832,176388800
2005-01-07,4.642857,4.973571,4.625000,4.946429,4.316814,556862600
2005-01-10,4.987857,5.050000,4.848571,4.925714,4.298736,431327400
2005-01-11,4.875000,4.939286,4.581429,4.611429,4.024456,652906800
2005-01-12,4.675000,4.707143,4.521429,4.675714,4.080557,479925600
2005-01-13,5.265000,5.315714,4.980714,4.985714,4.351099,791179200
2005-01-14,5.017857,5.122857,4.942143,5.014286,4.376033,442685600
2005-01-18,4.989286,5.050000,4.839286,5.046429,4.404085,251615000
2005-01-19,5.035000,5.104286,4.982143,4.991428,4.356086,187973800
2005-01-20,4.975000,5.090714,4.962143,5.032857,4.392241,228730600
```

The program uses pandas to read a CSV file corresponding to the ticker parameter (only the tickers MSFT, AAPL, IBM and INTC have data behind them, the rest default to MSFT). Try http://127.0.0.1:8000/?ticker=intc for example.

The program needs to convert the dates to support the Highcharts (standard JavaScript) format which is number of milliseconds since the Epoch (1/1/1970). The short function convert_date1 does this using the Python datetime library. We use `map` to apply `convert_date1` to all values in the 'Date' column in order to generate the list of x values for the series.

## Stock Chart with Volume
[Stock Chart with Volume live demo]({{demo_url}}/stock_test2)

The CSV file contains additional data, not just the end of day price. 
We will now create a more sophisticated chart that uses this data.

```python
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


jp.justpy(stock_test2)
```

The chart is defined in this case using a standard Python dictionary. When assigned to the chart `options` attribute, it is automatically converted to a Dict in order to enable dot notation.

In this example, reading the remote CSV file is done in a non-blocking manner (if you are unfamiliar with `asyncio`, please skip this paragraph). The loop that JustPy runs in can be found in `JustPy.loop`. It is used to run `pd.read_csv` in the default thread or process pool. In order to allow awaiting a coroutine, `stock_test` is also defined as a coroutine using the `async` keyword.

The chart has two series with two different Y axis. The first series is a [candlestick](https://www.investopedia.com/trading/candlestick-charting-what-is-it/) series and shows the OHLC (open high low close) data succinctly, and the second series is a simple column series that shows the volume. The data list for each series is created by zipping together the appropriate columns of the pandas frame.

We also use the Highcharts theme 'grid' to give the chart a different look.
