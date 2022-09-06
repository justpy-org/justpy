# Justpy Tutorial demo hello_world3 from docs/tutorial/basic_concepts.md
import justpy as jp


def hello_world3():
    wp = jp.WebPage()
    my_paragraph_design = (
        "w-64 bg-blue-500 m-2 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
    )
    for i in range(1, 11):
        jp.P(text=f"{i}) Hello World!", a=wp, classes=my_paragraph_design)
    return wp


# initialize the demo
from examples.basedemo import Demo

Demo("hello_world3", hello_world3)
