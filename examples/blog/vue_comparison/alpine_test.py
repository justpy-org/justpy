# Justpy Tutorial demo alpine_test from docs/blog/vue_comparison.md
import justpy as jp

class SimpleDropdown(jp.Div):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        b = jp.Button(text='Open Dropdown', a=self, click='self.u.show = not self.u.show')
        b.u = jp.Ul(a=self, text='Drop Down Body', show=False, click__out='self.show = False')

def alpine_test():
    wp =jp.WebPage()
    SimpleDropdown(a=wp)
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("alpine_test",alpine_test)
