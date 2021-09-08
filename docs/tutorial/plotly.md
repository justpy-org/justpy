# Plotly Charts

[Plotly charts](https://plotly.com/python/) are supported by JustPy using the `PlotlyChart` component.

Assign a `plotly.graph_objects.Figure` object to the `chart` attribute of a `PlotlyChart` instance or alternatively, assign a dict describing the chart to the `chart_dict` attribute.

In the example below, a histogram is generated from random data and regenerated when with new random data when the users clicks a button.

```python
import justpy as jp
import plotly.figure_factory as ff
import numpy as np


def create_chart(numpoints):
    x1 = np.random.randn(numpoints) - 2
    x2 = np.random.randn(numpoints)
    x3 = np.random.randn(numpoints) + 2
    # Group data together
    hist_data = [x1, x2, x3]
    group_labels = ['Group 1', 'Group 2', 'Group 3']
    # Create display with custom bin_size
    fig = ff.create_distplot(hist_data, group_labels, bin_size=[.1, .25, .5])
    fig.update_layout(width=500, height=600)
    return fig


def generate_data(self, msg):
    wp = msg.page
    wp.c.chart = create_chart(wp.numpoints)


def plotly_test(request):
    wp = jp.WebPage()
    wp.numpoints = 500
    jp.Button(text='Generate New Data', click=generate_data, a=wp, classes=jp.Styles.button_simple + ' m-2 p-2')
    wp.c = jp.PlotlyChart(chart=create_chart(wp.numpoints), a=wp, classes='border m-2 p-6', style='width: 600px')
    return wp


jp.justpy(plotly_test, PLOTLY=True)
```