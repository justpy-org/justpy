# Justpy Tutorial demo hello_test2 from docs/tutorial/custom_components.md
import justpy as jp

def hello_test2():
    wp = jp.WebPage()
    for i in range(5):
        wp.add(jp.Hello()) # or jp.Hello(a=wp)
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("hello_test2",hello_test2)
