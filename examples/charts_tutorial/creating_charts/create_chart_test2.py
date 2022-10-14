# Justpy Tutorial demo create_chart_test2 from docs/charts_tutorial/creating_charts.md
import justpy as jp

# Example from https://www.highcharts.com/docs/getting-started/your-first-chart
my_chart_def = """
{
        chart: {
            type: 'bar'
        },
        title: {
            text: 'Fruit Consumption'
        },
        xAxis: {
            categories: ['Apples', 'Bananas', 'Oranges']
        },
        yAxis: {
            title: {
                text: 'Fruit eaten'
            }
        },
        series: [{
            name: 'Jane',
            data: [1, 0, 4]
        }, {
            name: 'John',
            data: [5, 7, 3]
        }]
}
"""


def create_chart_test2():
    wp = jp.WebPage()
    for chart_type in ["bar", "column", "line", "spline"]:
        my_chart = jp.HighCharts(a=wp, classes="m-2 p-2 border w-1/2", options=my_chart_def)
        my_chart.options.chart.type = chart_type
        my_chart.options.title.text = f"Chart of Type {chart_type.capitalize()}"
        my_chart.options.subtitle.text = f"Subtitle {chart_type.capitalize()}"
    return wp

# initialize the demo
from examples.basedemo import Demo
Demo("create_chart_test2", create_chart_test2)
