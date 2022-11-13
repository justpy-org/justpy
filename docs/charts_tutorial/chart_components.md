# Chart Custom Components

Components in JustPy are Python classes that inherit from other JustPy components. Components that inherit from HighCharts can also be defined. For example, below we define and use a pie chart component.

## Pie Chart Component
[Pie Chart Component live demo]({{demo_url}}/pie_test)

```python
import justpy as jp

class MyPie(jp.HighCharts):

    _options = """
{
    chart: {
        type: 'pie'
    },
    title: {
        text: 'Pie Chart'
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
                format: '<b>{point.name}</b>: {point.percentage:.1f}%',
            }
        }
    },
    series: []
}
    """

    def __init__(self, data, **kwargs):
        self.labels = []
        super().__init__(**kwargs)
        self.load_json(self._options)
        pie_series = jp.Dict()
        pie_series.data = []
        for i, value in enumerate(data):
            c = jp.Dict()
            try:
                c.name = self.labels[i]
            except:
                c.name = str(value)
            c.y = value
            pie_series.data.append(c)
        self.options.series.append(pie_series)


def pie_test(request):
    wp = jp.WebPage()
    chart = MyPie([2,3,4,5], labels=['Apples', 'Pears', 'Bananas', 'Melons'], a=wp, classes='m-2 p-2 border w-1/2')
    chart.options.title.text = 'Fruit Distribution'
    chart.options.series[0].name = 'Fruits'
    return wp

jp.justpy(pie_test)

```

The chart instance that is created can be further modified by changing its options. In the example above we change the chart title and the name of the series.

## Histogram Component
[Histogram Component live demo]({{demo_url}}/histogram_test)

A component that comes with JustPy is Histogram. It simplifies creating a histogram chart. In this example, we include the  definition.

!!! warning
    In order to run this example, you need to install [numpy](https://numpy.org/)

```python
import justpy as jp
import random
import numpy

class Histogram(jp.HighCharts):

    _options = """
{
    title: {
        text: 'Highcharts Histogram'
    },
    xAxis: [{
        title: { text: 'Data' },
        alignTicks: false
    }, {
        title: { text: 'Histogram' },
        alignTicks: false,
        opposite: true
    }],

    yAxis: [{
        title: { text: 'Data' }
    }, {
        title: { text: 'Histogram' },
        opposite: true
    }],

    series: [{
        name: 'Histogram',
        type: 'histogram',
        xAxis: 1,
        yAxis: 1,
        baseSeries: 's1',
        zIndex: -1
    }, {
        name: 'Data',
        type: 'scatter',
        data: [],
        id: 's1',
        marker: {
            radius: 1.5
        }
    }]
}

    """

    def __init__(self, data, **kwargs):
        super().__init__(**kwargs)
        self.load_json(self._options)
        self.options.series[1].data = list(data)

def histogram_test(request):
    wp = jp.WebPage()
    # Uniform distribution
    data = [random.randrange(10) for i in range(100)]
    chart = jp.Histogram(data, a=wp, classes='m-2 border w-1/2')
    chart.options.title.text = 'Uniform Distribution Histogram'
    # Normal distribution
    data = [numpy.random.normal() for i in range(1000)]
    chart = jp.Histogram(data, a=wp, classes='m-2 border w-1/2')
    chart.options.title.text = 'Normal Distribution Histogram'
    return wp

jp.justpy(histogram_test)

```

The Histogram class relies on a [chart definition](https://www.highcharts.com/docs/chart-and-series-types/histogram-series) from the Highcharts documentation.

Encompassing the chart definition in a class simplifies its use. If you build such classes for your favorite charts, please send them to me to include in JustPy. Once the Histogram class (component) is defined, reusing it is simple and does not require remembering the specifics of the Highcharts API. The instance of HighCharts can be further modified. In the example above, we change the chart titles after the chart has been created.

## Scatter with Regression
[Scatter with Regression live demo]({{demo_url}}/scatter_test)
Let's build a component that automatically adds a regression line to a scatter chart. We will use the predefined JustPy Scatter component.

```python
import justpy as jp
import numpy as np

class ScatterWithRegression(jp.Scatter):

    def __init__(self, x, y, **kwargs):
        super().__init__(x, y, **kwargs)
        x = np.asarray(x)
        y = np.asarray(y)
        m = (len(x) * np.sum(x * y) - np.sum(x) * np.sum(y)) / (len(x) * np.sum(x * x) - np.sum(x) ** 2)
        b = (np.sum(y) - m * np.sum(x)) / len(x)
        s = jp.Dict()   # The new series
        s.type = 'line'
        s.marker.enabled = False
        s.enableMouseTracking = False
        min = float(x.min())
        max = float(x.max())
        s.data = [[min, m * min + b], [max, m * max + b]]
        s.name = f'Regression, m: {round(m, 3)}, b: {round(b, 3)}'
        self.options.series.append(s)


def scatter_test(request):
    wp = jp.WebPage(highcharts_theme='grid-light')
    x = [108,19,13,124,40,57,23,14,45,10,5,48,11,23,7,2,24,6,3,23,6,9,9,3,29,7,4,20,7,4,0,25,6,5,22,11,61,12,4,16,13,60,41,37,55,41,11,27,8,3,17,13,13,15,8,29,30,24,9,31,14,53,26]
    y = [392.5,46.2,15.7,422.2,119.4,170.9,56.9,77.5,214,65.3,20.9,248.1,23.5,39.6,48.8,6.6,134.9,50.9,4.4,113,14.8,48.7,52.1,13.2,103.9,77.5,11.8,98.1,27.9,38.1,0,69.2,14.6,40.3,161.5,57.2,217.6,58.1,12.6,59.6,89.9,202.4,181.3,152.8,162.8,73.4,21.3,92.6,76.1,39.9,142.1,93,31.9,32.1,55.6,133.3,194.5,137.9,87.4,209.8,95.5,244.6,187.5]
    jp.Scatter(x, y, a=wp, classes='m-2 w-1/2 border', style='height: 300px')
    sr = ScatterWithRegression(x, y, a=wp, classes='m-2 w-1/2 border', style='height: 300px')
    sr.options.title.text = 'Scatter Chart with Regression'
    return wp

jp.justpy(scatter_test)
```

The new component adds another series to the chart. This series has only two points which are the regression values of the smallest and largest x values. The line between them is the regression line. We now have a component we can reuse to plot a scatter plot with a regression line.
