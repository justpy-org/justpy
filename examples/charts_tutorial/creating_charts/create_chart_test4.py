# Justpy Tutorial demo create_chart_test4 from docs/charts_tutorial/creating_charts.md
import justpy as jp

my_chart_def = """
{
    chart: {
        type: 'bar'
    },
    xAxis: {
        categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    },
    legend: {
        layout: 'vertical',
        floating: true,
        backgroundColor: '#FFFFFF',
        align: 'right',
        verticalAlign: 'top',
        y: 60,
        x: -60
    },
    series: [{
        data: [29.9, 71.5, 106.4, 129.2, 144.0, 176.0, 135.6, 148.5, 216.4, 194.1, 95.6, 54.4]
    }]
}
"""


def create_chart_test4():
    wp = jp.WebPage()
    my_chart = jp.HighCharts(a=wp, classes="m-2 p-2 border w-1/2", options=my_chart_def)
    my_chart.options.series[0].name = "'Tourists in \'000'"
    my_chart.options.title.text = "Tourists in Middle Earth"
    return wp


# initialize the demo
from examples.basedemo import Demo
Demo("create_chart_test4", create_chart_test4)
