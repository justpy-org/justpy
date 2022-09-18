# Justpy Tutorial demo html_demo from docs/tutorial/working_with_html.md
import justpy as jp

def html_demo():
    wp = jp.WebPage()
    jp.Div(text='This will not be shown', a=wp)
    wp.html = '<p class="text-2xl m-2 m-1 text-red-500">Hello world!<p>'
    jp.Div(text='This will not be shown', a=wp)
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("html_demo",html_demo)
