# Justpy Tutorial demo hello_test3 from docs/tutorial/custom_components.md
import justpy as jp

def hello_test3():
    wp = jp.WebPage()
    for i in range(5):
        jp.Hello(a=wp, counter=100)
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("hello_test3",hello_test3)
