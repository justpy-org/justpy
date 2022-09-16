# Justpy Tutorial demo hello_test1 from docs/tutorial/custom_components.md
import justpy as jp

def hello_test1():
    wp = jp.WebPage()
    h = jp.Hello()
    for i in range(5):
        wp.add(h)
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("hello_test1",hello_test1)
