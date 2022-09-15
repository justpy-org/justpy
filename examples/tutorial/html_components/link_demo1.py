# Justpy Tutorial demo link_demo1 from docs/tutorial/html_components.md
import justpy as jp

def link_demo1():
    wp = jp.WebPage()
    jp.A(text='Python Org', href='https://python.org', a=wp, classes='m-2 p-2 text-xl text-white bg-blue-500 hover:bg-blue-700')
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("link_demo1",link_demo1)
