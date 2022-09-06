# Justpy Tutorial demo bokeh_test from docs/tutorial/bokeh.md
import justpy as jp
import bokeh

bokeh.sampledata.download()  # Run this the first time you run the program
from bokeh.plotting import figure, output_file, show
from bokeh.sampledata.iris import flowers
from bokeh.embed.standalone import json_item
from bokeh.models import LogColorMapper
from bokeh.palettes import Viridis6 as palette1
from bokeh.plotting import figure
from bokeh.sampledata.unemployment import data as unemployment
from bokeh.sampledata.us_counties import data as counties1


def create_iris_figure(*, width=500, height=500):
    colormap = {"setosa": "red", "versicolor": "green", "virginica": "blue"}
    colors = [colormap[x] for x in flowers["species"]]

    p = figure(title="Iris Morphology", plot_width=width, plot_height=height)
    p.xaxis.axis_label = "Petal Length"
    p.yaxis.axis_label = "Petal Width"

    p.circle(
        flowers["petal_length"],
        flowers["petal_width"],
        color=colors,
        fill_alpha=0.2,
        size=10,
    )
    return p


def create_texas_figure(*, width=500, height=500):
    palette = tuple(reversed(palette1))

    counties = {
        code: county for code, county in counties1.items() if county["state"] == "tx"
    }

    county_xs = [county["lons"] for county in counties.values()]
    county_ys = [county["lats"] for county in counties.values()]

    county_names = [county["name"] for county in counties.values()]
    county_rates = [unemployment[county_id] for county_id in counties]
    color_mapper = LogColorMapper(palette=palette)

    data = dict(
        x=county_xs,
        y=county_ys,
        name=county_names,
        rate=county_rates,
    )

    TOOLS = "pan,wheel_zoom,reset,hover,save"

    p = figure(
        title="Texas Unemployment, 2009",
        tools=TOOLS,
        x_axis_location=None,
        y_axis_location=None,
        tooltips=[
            ("Name", "@name"),
            ("Unemployment rate", "@rate%"),
            ("(Long, Lat)", "($x, $y)"),
        ],
    )
    p.grid.grid_line_color = None
    p.hover.point_policy = "follow_mouse"

    p.patches(
        "x",
        "y",
        source=data,
        fill_color={"field": "rate", "transform": color_mapper},
        fill_alpha=0.7,
        line_color="white",
        line_width=0.5,
    )
    return p


def bokeh_test(request):
    wp = jp.WebPage(tailwind=True)
    p = create_iris_figure()
    wp.c = jp.BokehChart(chart=p, a=wp)
    p1 = create_iris_figure(width=300, height=300)
    jp.BokehChart(chart=p1, a=wp)
    p2 = create_texas_figure()
    jp.BokehChart(chart=p2, a=wp)
    return wp


# initialize the demo
from examples.basedemo import Demo

Demo("bokeh_test", bokeh_test, BOKEH=True)
