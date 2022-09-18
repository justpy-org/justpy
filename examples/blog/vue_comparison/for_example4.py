# Justpy Tutorial demo for_example4 from docs/blog/vue_comparison.md
import justpy as jp


def for_example4():
    wp = jp.WebPage(tailwind=False)
    object = {
      'title': 'How to do lists in Vue',
      'author': 'Jane Doe',
      'publishedAt': '2016-04-10'
    }
    for index, (name, value) in enumerate(object.items()):
        jp.Div(text=f'{index}. {name}: {value}', a=wp)
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("for_example4",for_example4)
