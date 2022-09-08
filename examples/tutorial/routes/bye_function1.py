# Justpy Tutorial demo bye_function1 from docs/tutorial/routes.md
import justpy as jp


def hello_function2():
    wp = jp.WebPage()
    wp.add(jp.P(text="Hello there!", classes="text-5xl m-2"))
    return wp


def bye_function1():
    wp = jp.WebPage()
    wp.add(jp.P(text="Goodbye!", classes="text-5xl m-2"))
    return wp


jp.Route("/hello", hello_function2)

# initialize the demo
from examples.basedemo import Demo

Demo("bye_function1", bye_function1)
