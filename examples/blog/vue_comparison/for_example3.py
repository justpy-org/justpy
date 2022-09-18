# Justpy Tutorial demo for_example3 from docs/blog/vue_comparison.md
import justpy as jp


def for_example3():
    wp = jp.WebPage(tailwind=False)
    ul = jp.Ul(a=wp)
    object = {
      'title': 'How to do lists in Vue',
      'author': 'Jane Doe',
      'publishedAt': '2016-04-10'
    }
    for name, value in object.items():
        jp.Li(text=f'{name}: {value}', a=ul)
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("for_example3",for_example3)
