# Justpy Tutorial demo women_majors1 from docs/charts_tutorial/pandas.md
import justpy as jp
import pandas as pd


wm = pd.read_csv("https://elimintz.github.io/women_majors.csv").round(2)
# Create list of majors which start under 20% women students
wm_under_20 = list(wm.loc[0, wm.loc[0] < 20].index)


def women_majors1():
    wp = jp.WebPage()
    wm.jp.plot(
        0,
        wm_under_20,
        kind="spline",
        a=wp,
        title="The gender gap is transitory - even for extreme cases",
        subtitle="Percentage of Bachelors conferred to women form 1970 to 2011 in the US for extreme cases where the percentage was less than 20% in 1970",
        classes="m-2 p-2 w-3/4",
    )
    return wp


# initialize the demo
from examples.basedemo import Demo

Demo("women_majors1", women_majors1)
