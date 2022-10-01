# Justpy Tutorial demo inner_html_test from docs/reference/htmlcomponent.md
import justpy as jp

def inner_html_test():
    wp = jp.WebPage()
    for i in range(1,11):
        jp.Div(inner_html=f'<span style="color: orange">{i}) Hello!</span>', a=wp, classes='m-2 p-2 text-3xl')
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("inner_html_test",inner_html_test)
