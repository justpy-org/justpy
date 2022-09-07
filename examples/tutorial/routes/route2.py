# Justpy Tutorial demo  from docs/tutorial/routes.md
import justpy as jp


@jp.SetRoute("/hello")
def hello_function3():
    wp = jp.WebPage()
    wp.add(jp.P(text="Hello there!", classes="text-5xl m-2"))
    return wp


@jp.SetRoute("/bye")
def bye_function2():
    wp = jp.WebPage()
    wp.add(jp.P(text="Goodbye!", classes="text-5xl m-2"))
    return wp


# initialize the demo
from examples.basedemo import Demo

Demo("route2", None)
