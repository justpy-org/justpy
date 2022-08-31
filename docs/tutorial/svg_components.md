# SVG Components

>Scalable Vector Graphics (SVG) is an XML-based markup language for describing two dimensional based vector graphics. SVG is essentially to graphics what HTML is to text.  
- [mozilla.org](https://developer.mozilla.org/en-US/docs/Web/SVG)

JustPy comes with components for all the SVG elements. 

## Basic Example

```python
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

jp.justpy(svg_demo1)
```

The example above puts a few circles and ellipses on the page.

## Simple parse_html

The following example is based on https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/fill

Usually, you will find some SVG graphic you would like to use on you page. The simplest way to do so is to use `parse_html`.

```python
import justpy as jp
# Example based on https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/fill

svg_html = """
<svg viewBox="0 0 300 100" xmlns="http://www.w3.org/2000/svg" width=300 height=100>
  <!-- Simple color fill -->
  <circle cx="50" cy="50" r="40" fill="pink" />

  <!-- Fill circle with a gradient -->
  <defs>
    <radialGradient id="myGradient">
      <stop offset="0%"   stop-color="pink"/>
      <stop offset="100%" stop-color="black" />
    </radialGradient>
  </defs>

  <circle cx="150" cy="50" r="40" fill="url(#myGradient)" />

  <!--
  Keeping the final state of an animated circle
  which is a circle with a radius of 40.
  -->
  <circle cx="250" cy="50" r="20">
    <animate attributeType="XML"
             attributeName="r"
             from="0" to="40" dur="5s"
             fill="freeze" />
  </circle>
</svg>
"""


def svg_demo2():
    wp = jp.WebPage()
    jp.parse_html(svg_html, a=wp)
    return wp


jp.justpy(svg_demo2)
```

## Advanced parse_html example

Please run the following program and click on any middle circle. 

```python
import justpy as jp
# Example based on https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/fill

svg_html = """
<svg viewBox="0 0 300 100" xmlns="http://www.w3.org/2000/svg" width=300 height=100>
  <!-- Simple color fill -->
  <circle cx="50" cy="50" r="40" fill="pink" name="simple_circle"/>

  <!-- Fill circle with a gradient -->
  <defs>
    <radialGradient id="myGradient" name="gradient">
      <stop offset="0%"   stop-color="pink" name="stop"/>
      <stop offset="100%" stop-color="black" />
    </radialGradient>
  </defs>

  <circle cx="150" cy="50" r="40" fill="url(#myGradient)" name="gradient_circle"/>

  <!--
  Keeping the final state of an animated circle
  which is a circle with a radius of 40.
  -->
  <circle cx="250" cy="50" r="20">
    <animate attributeType="XML"
             attributeName="r"
             from="0" to="40" dur="5s"
             fill="freeze" />
  </circle>
</svg>
"""

def circle_click(self, msg):
    if self.stop.stop_color == 'orange':
        self.stop.stop_color = self.original_color
    else:
        self.stop.stop_color = 'orange'

def svg_demo3():
    wp = jp.WebPage()
    colors = ['pink', 'red', 'blue', 'green', 'teal', 'yellow']
    for color in colors:
        g = jp.parse_html(svg_html.replace('id="myGradient"', f'id="{color}"'), a=wp)
        g.name_dict["gradient_circle"].original_color = color
        gradient = g.name_dict["gradient"]
        g.name_dict["gradient_circle"].fill = f'url(#{gradient.id})'
        g.name_dict["gradient_circle"].stop = g.name_dict["stop"]
        g.name_dict["gradient_circle"].on('click', circle_click)
        g.name_dict["stop"].stop_color = color
        g.name_dict["simple_circle"].fill = color
    return wp

jp.justpy(svg_demo3)
```

In `svg_demo`, in a loop that iterates over a list of colors, an element is created from parsing a modification of of the string `svg_html` (we change the id of the gradient definition to be unique). Then, the result is modified using the [name_dict](../working_with_html/#the-name_dict-dictionary) attribute. In the HTML string we named the elements we plan to modify later and they can be found in [name_dict](../working_with_html/#the-name_dict-dictionary).

Notice the two lines:

```python
        gradient = g.name_dict["gradient"]
        g.name_dict["gradient_circle"].fill = f'url(#{gradient.id})'
```

The fill attribute of the circle with the gradient needs to refer the id of the radialGradient element. In the HTML string it is set to "myGradient" which we replace with a unique id in each loop iteration. 



