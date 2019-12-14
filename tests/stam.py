import justpy as jp
import random
import numpy



def histogram_test(request):
    wp = jp.WebPage()
    # wp = jp.QuasarPage()
    data = [random.randrange(10) for i in range(100)]
    chart = jp.Histogram(data, a=wp, classes='m-2 border w-1/2')
    chart.options.title.text = 'Uniform Distribution Histogram'
    data = [numpy.random.normal() for i in range(1000)]
    chart = jp.Histogram(data, a=wp, classes='m-2 border w-1/2')
    chart.options.title.text = 'Normal Distribution Histogram'
    return wp

# jp.justpy(histogram_test)

class MyPie(jp.HighCharts):

    _s1 = """
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
        labels = []
        super().__init__(**kwargs)
        chart = self
        chart.load_json(self._s1)
        series = jp.Dict()
        series.name = 'Fruits'
        series.data = []
        for i, value in enumerate(data):
            c = jp.Dict()
            try:
                c.name = self.labels[i]
            except:
                c.name = str(value)
            c.y = value
            series.data.append(c)
        chart.options.series.append(series)


def pie_test(request):
    wp = jp.WebPage()
    chart = MyPie([2,3,4,5], labels=['Apples', 'Pears', 'Bananas', 'Melons'], a=wp, classes='m-2 p-2 border w-1/2')
    chart.options.title.text = 'Fruit Distribution'
    chart = jp.PieSemiCircle([2,3,4,5], labels=['Apples', 'Pears', 'Bananas', 'Melons'], a=wp, classes='m-2 p-2 border w-1/2')
    chart.options.title.text = 'Fruit Distribution'
    return wp

jp.justpy(pie_test)