# Justpy Tutorial demo  from docs/tutorial/routes.md
import justpy as jp


def hello_function1():
    wp = jp.WebPage()
    wp.add(jp.P(text="Hello there!", classes="text-5xl m-2"))
    return wp


jp.Route("/hello", hello_function1)

# initialize the demo
from examples.basedemo import Demo

Demo("route1", None)
