# Justpy Tutorial demo style_test from docs/reference/htmlcomponent.md
import justpy as jp

def style_test():
    wp = jp.WebPage()
    for size in range(1,101):
        jp.Div(text=f' {size}', style=f'font-size: {size}px; color: red', a=wp, classes='inline cursor-pointer', size=size,
               click='self.size *= 2; self.style=f"font-size: {self.size}px; color: green";')
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("style_test",style_test)
