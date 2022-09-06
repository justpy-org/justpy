# Justpy Tutorial demo women_majors2 from docs/charts_tutorial/pandas.md
import justpy as jp
import pandas as pd


wm = pd.read_csv("https://elimintz.github.io/women_majors.csv").round(2)
wm_under_20 = list(
    wm.loc[0, wm.loc[0] < 20].index
)  # Create list of majors which start under 20%


def women_majors2():
    wp = jp.WebPage()

    # First chart
    wm.jp.plot(
        0,
        wm_under_20,
        kind="spline",
        a=wp,
        title="The gender gap is transitory - even for extreme cases",
        subtitle="Percentage of Bachelors conferred to women form 1970 to 2011 in the US for extreme cases where the percentage was less than 20% in 1970",
        classes="m-2 p-2 w-3/4",
    )

    # Second Chart
    wm_chart = wm.jp.plot(
        0,
        wm_under_20,
        kind="spline",
        a=wp,
        categories=False,
        title="The gender gap is transitory - even for extreme cases",
        subtitle="Percentage of Bachelors conferred to women form 1970 to 2011 in the US for extreme cases where the percentage was less than 20% in 1970",
        classes="m-2 p-2 w-3/4 border",
        style="height: 700px",
    )
    o = wm_chart.options
    o.title.align = "left"
    o.title.style.fontSize = "24px"
    o.subtitle.align = "left"
    o.subtitle.style.fontSize = "20px"
    o.xAxis.title.text = "Year"
    o.xAxis.gridLineWidth = 1
    o.yAxis.title.text = "% Women in Major"
    o.yAxis.labels.format = "{value}%"
    o.legend.layout = "proximate"
    o.legend.align = "right"
    o.plotOptions.series.marker.enabled = False

    return wp


# initialize the demo
from examples.basedemo import Demo

Demo("women_majors2", women_majors2)
