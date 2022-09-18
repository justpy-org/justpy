# Justpy Tutorial demo for_example1 from docs/blog/vue_comparison.md
import justpy as jp

def for_example1():
    wp = jp.WebPage(tailwind=False)  
    items = [{'message': 'Foo'},
             {'message': 'Bar'}]
    ul = jp.Ul(a=wp)
    for item in items:
        jp.Li(text=f'{item["message"]}', a=ul)
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("for_example1",for_example1)
