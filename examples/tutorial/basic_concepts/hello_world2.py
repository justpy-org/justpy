# Justpy Tutorial demo hello_world2 from docs/tutorial/basic_concepts.md
import justpy as jp


def hello_world2():
    wp = jp.WebPage()
    for i in range(1, 11):
        jp.P(text=f"{i}) Hello World!", a=wp, style=f"font-size: {10*i}px")
    return wp


# initialize the demo
from examples.basedemo import Demo

Demo("hello_world2", hello_world2)
