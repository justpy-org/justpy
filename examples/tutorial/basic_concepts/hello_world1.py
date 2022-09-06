# Justpy Tutorial demo hello_world1 from docs/tutorial/basic_concepts.md
import justpy as jp


def hello_world1():
    wp = jp.WebPage()
    p = jp.P(text="Hello World!", a=wp)
    return wp


## JustPy Requests
# initialize the demo
from examples.basedemo import Demo

Demo("hello_world1", hello_world1)
