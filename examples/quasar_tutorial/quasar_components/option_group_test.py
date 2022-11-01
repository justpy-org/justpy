# Justpy Tutorial demo option_group_test from docs/quasar_tutorial/quasar_components.md
import justpy as jp

# Example from https://www.highcharts.com/docs/getting-started/your-first-chart
my_chart_def = """
{
        chart: {
            type: 'bar'
        },
        title: {
            text: 'Chart of Type Bar'
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

def radio_change(self, msg):
    print(msg)
    self.chart.options.chart.type = self.value

def option_group_test():
    wp = jp.QuasarPage()
    chart_type = jp.QOptionGroup(color='red', a=wp, inline=True, input=radio_change, value='bar')
    for type in ['bar', 'column', 'line', 'spline']:
        chart_type.options.append({'label': type.capitalize(), 'value': type})
    chart_type.chart = jp.HighCharts(a=wp, classes='q-ma-lg', options=my_chart_def)
    return wp


# initialize the demo
from examples.basedemo import Demo
Demo("option_group_test", option_group_test)
