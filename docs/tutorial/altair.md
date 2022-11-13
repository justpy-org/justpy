# Altair Charts
[Altair Charts live demo]({{demo_url}}/altair_chart_test)

[Altair charts](https://altair-viz.github.io/) are supported by JustPy using the `AltairChart` component.

The `AltairChart` component supports visualization of any [Vega](https://vega.github.io/vega/) defined object. Instead of setting the component's `chart` attribute, set the `vega_source` attribute with the Vega language definition. 

In the example below, in addition to the default route, the "/line" route is also defined. It is an example of how a slider can be used to change a chart.


```python
import altair as alt
import justpy as jp


# Load a simple dataset as a pandas DataFrame
from vega_datasets import data
cars = data.cars()

car_chart = alt.Chart(cars).mark_point().encode(
    x='Horsepower',
    y='Miles_per_Gallon',
    color='Origin',
).properties(
    width=500,
    height=300
)


def altair_chart_test(request):
    wp = jp.WebPage(tailwind=True)
    wp.altair_chart = jp.AltairChart(chart=car_chart, a=wp, classes='m-8')
    return wp


def change_limit(self, msg):
    wp = msg.page
    wp.chart.chart = create_chart(self.value)


def create_chart(value):
    source = alt.sequence(start=0, stop=value, step=0.1, as_='x')
    return alt.Chart(source).mark_line().transform_calculate(
        sin='sin(datum.x)',
        cos='cos(datum.x)'
    ).transform_fold(
        ['sin', 'cos']
    ).encode(
        x='x:Q',
        y='value:Q',
        color='key:N'
    ).properties(
        width=500,
        height=300
    )


@jp.SetRoute('/line')
def line_chart(request):
    wp = jp.QuasarPage(tailwind=True)
    jp.QSlider(a=wp, classes='m-8 p-2', style='width: 500px',input=change_limit, label=True, label_always=True,
               value=10, min=1, max=50, snap=True, markers=True)
    wp.chart = jp.AltairChart(chart=create_chart(10), a=wp, classes='m-4 p-2')
    return wp


jp.justpy(altair_chart_test, VEGA=True)
```