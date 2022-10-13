# Justpy Tutorial demo histogram_test from docs/charts_tutorial/chart_components.md
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

# initialize the demo
from  examples.basedemo import Demo
Demo ("histogram_test",histogram_test)
