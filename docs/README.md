# Introduction

## What is JustPy?

JustPy is an object-oriented, component based, high-level Python Web Framework that requires no front-end programming. With a few lines of only Python code, you can create interactive websites with no need for JavaScript programming.  

When developing with JustPy, there is no frontend/backend distinction. All programming is done on the backend allowing a simpler and more Pythonic web development experience. This is a major difference from other frameworks that is hard to describe in words but will become evident when you see some concrete examples. The best way to understand JustPy is to follow the [tutorial](tutorial/getting_started.md). 

In JustPy, elements on the web page are instances of component classes. A component in JustPy is a Python class. Customized, reusable components can be created from other components. Out of the box, JustPy comes with support for HTML and SVG components as well as more complex components such as charts and grids.  It also supports most of the components and the functionality of the [Quasar](https://quasar.dev/) library of [Material Design 2.0](https://material.io/) components. 

JustPy integrates seamlessly with [pandas](https://pandas.pydata.org/) and makes it simple to build web sites based on pandas analysis. With a simple command you can create an interactive [Highcharts chart](https://www.highcharts.com/) or [Ag-Grid grid](https://www.ag-grid.com/) from a pandas data frame.  

!> One time only marketing pitch: **Experimenting with JustPy is worth your time. It has made me an order of magnitude more productive. You will be surprised how little code is required to develop sophisticated web sites** 

Hopefully, JustPy enables teaching web development in introductory Python courses by reducing the technologies that need to be mastered to basically only Python and reducing the complexity of web development.


## Hello World

```python
import justpy as jp

def hello_world():
    wp = jp.WebPage()
    d = jp.Div(text='Hello world!')
    wp.add(d)
    return wp
    
jp.justpy(hello_world)
```

That's it. The program above activates a web server that returns a web page with 'Hello world!' for any request. Locally, you would go to http://localhost:8000/ or http://127.0.0.1:8000 to see the result.
   
## Pandas, Charts and Grids Examples

JustPy comes with a [pandas](https://pandas.pydata.org/) [extension](https://pandas.pydata.org/pandas-docs/stable/development/extending.html) that makes it simple to create charts and grids from pandas data frames.

The charts are created using [Higcharts](https://www.highcharts.com/products/highcharts/) or [Highstock](https://www.highcharts.com/products/highstock/)

#@@ World Happiness Index
JustPy comes with a [pandas](https://pandas.pydata.org/) [extension](https://pandas.pydata.org/pandas-docs/stable/development/extending.html) that makes it simple to create charts and grids using pandas data frames.

You can try the following program at http://justpy.ogr/happiness or try running it yourself ([getting started](tutorial/getting_started)).

In under 50 lines of code...
```python
import justpy as jp
import pandas as pd

# https://worldhappiness.report/ed/2019/
df = pd.read_csv('http://elimintz.github.io/happiness_report_2019.csv').round(3)


def grid_change(self, msg):
    # Called when grid changes due to sorting or filtering. Chart is updated based on changes
    msg.page.df = jp.read_csv_from_string(msg.data)
    c = msg.page.df.jp.plot('Country', msg.page.cols_to_plot, kind='column', title='World Happiness Ranking',
                    subtitle='Click and drag in the plot area to zoom in. Shift + drag to pan', temp=True)
    c.options.plotOptions.series.stacking = msg.page.stacking
    msg.page.c.options = c.options


def stack_change(self, msg):
    # Called when stacking option is changed.
    msg.page.c.options.plotOptions.series.stacking = self.value
    msg.page.stacking = self.value


def happiness_plot():
    # The request handler, creates a page with the graph and the gird
    wp = jp.QuasarPage()
    wp.stacking = ''
    wp.cols_to_plot = ['Unexplained', 'GDP', 'Social_support', 'Health', 'Freedom', 'Generosity', 'Corruption']
    wp.df = df
    d = jp.Div(classes='q-ma-lg', a=wp)
    bg = jp.QBtnToggle(push=True, glossy=True, toggle_color='primary', value='', a=d, input=stack_change)
    bg.options = [
          {'label': 'No Stacking', 'value': ''},
          {'label': 'Normal', 'value': 'normal'},
          {'label': 'percent', 'value': 'percent'}
        ]
    # Create chart
    c = df.jp.plot('Country', wp.cols_to_plot, kind='column', a=wp, title='World Happiness Ranking',
                   subtitle='Click and drag in the plot area to zoom in. Shift + drag to pan',
                   stacking='', classes='border m-2 p-2 q-ma-lg p-ma-lg')
    # Create grid
    g = df.jp.ag_grid(a=wp)
    for event_name in ['sortChanged', 'filterChanged']:
        g.on(event_name, grid_change)
    wp.c = c
    return wp


jp.justpy(happiness_plot)
```

### Stock Chart

See program run in 

```python
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
```

## Under the Hood

JustPy's backend is built using: 
* [starlette](https://www.starlette.io/) - "a lightweight [ASGI](https://asgi.readthedocs.io/en/latest/) framework/toolkit, which is ideal for building high performance asyncio services".
* [uvicorn](https://www.uvicorn.org/) - "a lightning-fast [ASGI](https://asgi.readthedocs.io/en/latest/) server, built on [uvloop](https://github.com/MagicStack/uvloop) and [httptools](https://github.com/MagicStack/httptools)".

JustPy's frontend (which is transparent to JustPy developers) is built using: 
* [Vue.js](https://vuejs.org/) - "The Progressive JavaScript Framework"

