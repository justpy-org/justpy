# Justpy Tutorial demo svg_demo1 from docs/tutorial/svg_components.md
import justpy as jp

def svg_demo1():
    wp = jp.WebPage()
    for color in ['red', 'green', 'blue']:
        svg = jp.Svg(viewBox='0 0 100 100', xmlns='http://www.w3.org/2000/svg', a=wp, width=100, height=100, classes='m-2 inline-block')
        circle = jp.Circle(cx='50', cy='50', r='50', fill=color, a=svg)
    for radius in range(10, 51, 10):
        svg = jp.Svg(viewBox='0 0 100 100', xmlns='http://www.w3.org/2000/svg', a=wp, width=100, height=100, classes='m-2 inline-block')
        ellipse = jp.Ellipse(cx=50, cy=50, rx=radius, ry=radius/2, fill='teal', a=svg)
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("svg_demo1",svg_demo1)
