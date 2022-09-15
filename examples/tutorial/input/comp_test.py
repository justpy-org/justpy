# Justpy Tutorial demo comp_test from docs/tutorial/input.md
import justpy as jp


def change_color(self, msg):
    self.color_div.set_class(f'bg-{self.value}-600')


def comp_test():
    wp = jp.WebPage()
    colors = ['red', 'green', 'blue', 'pink', 'yellow', 'teal', 'purple']
    select = jp.Select(classes='w-32 text-xl m-4 p-2 bg-white  border rounded', a=wp, value='red',
                  change=change_color)
    for color in colors:
        select.add(jp.Option(value=color, text=color, classes=f'bg-{color}-600'))
    select.color_div = jp.Div(classes='bg-red-600 w-32 h-16 m-4',a=wp)
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("comp_test",comp_test)
