# Justpy Tutorial demo html_comps3 from docs/tutorial/html_components.md
import justpy as jp

def html_comps3():
    wp = jp.WebPage()
    jp.Div(text='Text in italic', a=wp, classes='italic')
    jp.Div(text='Text in bold', a=wp, classes='font-bold')
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("html_comps3",html_comps3)
