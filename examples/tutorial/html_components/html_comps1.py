# Justpy Tutorial demo html_comps1 from docs/tutorial/html_components.md
import justpy as jp

def html_comps1():
    wp = jp.WebPage()
    jp.I(text='Text in Italic', a=wp)
    jp.Br(a=wp)
    jp.Strong(text='Text in the Strong element', a=wp)
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("html_comps1",html_comps1)
