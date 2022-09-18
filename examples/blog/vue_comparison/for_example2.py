# Justpy Tutorial demo for_example2 from docs/blog/vue_comparison.md
import justpy as jp

def for_example2():
    wp = jp.WebPage(tailwind=False)
    ul = jp.Ul(a=wp)
    ul.items = [{'message': 'Foo'},
             {'message': 'Bar'}]
    ul.parent_message = 'Parent'
    for index, item in enumerate(ul.items):
        jp.Li(text=f'{ul.parent_message}-{index}-{item["message"]}', a=ul)
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("for_example2",for_example2)
