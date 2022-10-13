# Justpy Tutorial demo pie_test from docs/charts_tutorial/chart_components.md

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

# initialize the demo
from  examples.basedemo import Demo
Demo ("pie_test",pie_test)
