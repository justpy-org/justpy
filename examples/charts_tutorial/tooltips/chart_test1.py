# Justpy Tutorial demo chart_test1 from docs/charts_tutorial/tooltips.md
import justpy as jp

my_chart_def = """
{
    chart: {
        type: 'column'
    },
    title: {
        text: 'Tourists in Middle Earth'
        },
    xAxis: {
        categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    },
    series: [{
        name: "Tourists in '000",
        data: [29.9, 71.5, 106.4, 129.2, 144.0, 176.0, 135.6, 148.5, 216.4, 194.1, 95.6, 54.4]
    }]
}
"""

async def tooltip_formatter1(self, msg):
    return await self.tooltip_update('<div>My tooltip!</div>', msg.websocket)

def chart_test1():
    wp = jp.WebPage()
    # First chart
    wp.css = '.h-chart {height: 300px;}'
    chart1 = jp.HighCharts(a=wp, classes='m-2 p-2 border w-1/2', options=my_chart_def)
    chart1.options.subtitle.text = 'Default Tooltip'
    # Second chart
    chart2 = jp.HighCharts(a=wp, classes='m-2 p-2 border w-1/2', options=my_chart_def)
    chart2.options.subtitle.text = 'Custom Tooltip'
    chart2.on('tooltip', tooltip_formatter1)
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("chart_test1",chart_test1)
