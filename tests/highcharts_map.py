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

def chart_test():
    wp = jp.WebPage()
    my_chart = jp.HighCharts(a=wp, classes='m-2 p-2 border', style='width: 600px')
    my_chart.options = my_chart_def
    return wp

jp.justpy(chart_test, highcharts=True)
