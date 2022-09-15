# Justpy Tutorial demo altair_chart_test from docs/tutorial/altair.md
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


# initialize the demo
from  examples.basedemo import Demo
Demo ("altair_chart_test",altair_chart_test, VEGA=True)
