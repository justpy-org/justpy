# Justpy Tutorial demo html_comps2 from docs/tutorial/html_components.md
import justpy as jp

def html_comps2():
    wp = jp.WebPage()
    jp.get_tag('i', text='Text in Italic', a=wp)
    jp.get_tag('br',a=wp)
    jp.get_tag('br',a=wp)
    jp.get_tag('br',a=wp)
    jp.get_tag('br',a=wp)
    jp.get_tag('strong', text='Text in the Strong element', a=wp)
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("html_comps2",html_comps2)
