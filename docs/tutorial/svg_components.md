# SVG Components

>Scalable Vector Graphics (SVG) is an XML-based markup language for describing two dimensional based vector graphics. SVG is essentially to graphics what HTML is to text.  
- [mozilla.org](https://developer.mozilla.org/en-US/docs/Web/SVG)

JustPy comes with components for all the SVG elements. 

## Basic Example

```python
import justpy as jp

def svg_demo():
    wp = jp.WebPage()
    for color in ['red', 'green', 'blue']:
        svg = jp.Svg(viewBox='0 0 100 100', xmlns='http://www.w3.org/2000/svg', a=wp, width=100, height=100, classes='m-2 inline-block')
        circle = jp.Circle(cx='50', cy='50', r='50', fill=color, a=svg)
    for radius in range(10, 51, 10):
        svg = jp.Svg(viewBox='0 0 100 100', xmlns='http://www.w3.org/2000/svg', a=wp, width=100, height=100, classes='m-2 inline-block')
        ellipse = jp.Ellipse(cx=50, cy=50, rx=radius, ry=radius/2, fill='teal', a=svg)
    return wp

jp.justpy(svg_demo)
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


def svg_demo():
    wp = jp.WebPage()
    g = jp.parse_html(svg_html, a=wp, keep_id=True)
    return wp


jp.justpy(svg_demo)
```

Notice, that we need to set the `keep_id` keyword argument of `parse_html` to `True`. This tells the parser not to use JustPy's system of giving `id`s to elements, but to keep the original `id`s in the HTML string. In this case, this is required because in the `defs` section of the SVG, a `radialGradient` is defined and given an id which is later used in the fill attribute value of the `circle` tag that follows. 

The downside of this method is that the children elements of the SVG element cannot respond to events.

## Advanced parse_html example

This problem can be solved using [`name_dict`](tutorial/working_with_html?id=the-name_dict-dictionary) to access specific elements of the SVG definition.

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

def my_click(self, msg):
    self.stop.stop_color = 'orange'

def svg_demo():
    wp = jp.WebPage()
    colors = ['pink', 'red', 'blue', 'green', 'teal', 'yellow']
    for color in colors:
        g = jp.parse_html(svg_html, a=wp)
        gradient = g.name_dict["gradient"]
        g.name_dict["gradient_circle"].fill = f'url(#{gradient.id})'
        g.name_dict["gradient_circle"].stop = g.name_dict["stop"]
        g.name_dict["gradient_circle"].on('click', my_click)
        g.name_dict["stop"].stop_color = color
        g.name_dict["simple_circle"].fill = color
    return wp

jp.justpy(svg_demo)
```

In `svg_demo`, in a loop that iterates over a list of colors, an element is created from parsing the string `svg_html`. Then, the result is modified using the [name_dict](tutorial/working_with_html?id=the-name_dict-dictionary) attribute. In the HTML string we named the elements we plan to modify later and they can be found in [name_dict](tutorial/working_with_html?id=the-name_dict-dictionary).

Notice the two lines:

```python
        gradient = g.name_dict["gradient"]
        g.name_dict["gradient_circle"].fill = f'url(#{gradient.id})'
```

The fill attribute of the circle with the gradient needs to refer the id of the radialGradient element. In the HTML string it is set to "myGradient" but JustPy ignores this in the parsing and assigns its own id which we retrieve by referring to `gradient.id`. 


## Light Source Filters and Animation

The more complex example below is taken from https://css-tricks.com/look-svg-light-source-filters/

!> The example below works only on Chrome as far as I can tell

```python
import justpy as jp
# https://css-tricks.com/look-svg-light-source-filters/

sun_html = """
  <svg width="375" height="300" viewBox="0 0 375 300" xmlns="http://www.w3.org/2000/svg">
    <desc>Filter to create light on tree graphic.</desc>
      <filter id="demo4" name="tree_filter">
        <!--Blur effect-->
        <feGaussianBlur stdDeviation="3" result="blur4" />
        <!--Lighting effect-->
        <feSpecularLighting result="spec4" in="blur4" specularExponent="35" lighting-color="#cccccc">
            <!--Light source effect-->
            <fePointLight x="75" y="100" z="200">
              <!--Lighting Animation-->
              <animate attributeName="x" values="75;320;75" dur="10s" repeatCount="indefinite" />
            </fePointLight>
        </feSpecularLighting>
        <!--Composition of inputs-->
        <feComposite in="SourceGraphic" in2="spec4" operator="arithmetic" k1="0" k2="1" k3="1" k4="0" />
      </filter>
      <desc>Filter to blur sun graphic.</desc>
      <filter id="demo5" name="sun_filter">
        <feGaussianBlur in="SourceGraphic" stdDeviation="2" result="blur5" />
        <!--Composition of inputs-->
        <feComposite in="SourceGraphic" in2="blur5" operator="arithmetic" k1="0" k2="3" k3="3" k4="0" />
      </filter>
    <desc>Tree with three red apples and a sun to demonstrate lighting filter animations.</desc>
    <!--Apple tree graphic-->
    <g class="tree" filter="url(#3)" name="tree">
      <g>
        <path fill="#60432D" d="M164.946 295.159c-1.1 0-1.483-0.737-0.85-1.637 0 0 16.417-23.364 15.008-70.364 0 0 26.5 0 26.5 0 0.098 6.118 0.523 12.264 0.988 18.364 0.901 11.82 2.561 23.979 5.527 35.467 1.626 6.298 6.668 16.396 6.668 16.396 0.491 0.984-0.007 1.785-1.107 1.78 0 0-1.699-0.008-2.18-0.008 -1.677-0.003-3.354-0.001-5.03 0 -4.573 0.004-9.147 0.001-13.72 0 -9.247-0.002-18.494 0-27.74 0.001C166.989 295.159 164.946 295.159 164.946 295.159z" />
      </g>
      <path fill="#A6BA50" stroke="#A6BA50" stroke-linecap="round" d="M251.203 175.839c3.07 4.72 4.84 10.35 4.84 16.39 0 16.69-13.52 30.22-30.21 30.22 -4.68 0-9.11-1.06-13.06-2.96 -5.32 8.66-14.87 14.43-25.77 14.43 -12.5 0-23.22-7.59-27.82-18.41 -0.79 0.08-1.58 0.11-2.39 0.11 -16.69 0-30.21-13.53-30.21-30.22 0-4.14 0.83-8.09 2.34-11.69 -1.51-3.6-2.34-7.55-2.34-11.69 0-16.68 13.52-30.21 30.21-30.21 4.59 0 8.94 1.02 12.84 2.86 5.26-8.86 14.93-14.8 25.99-14.8 9.05 0 17.18 3.99 22.71 10.3 2.4-0.61 4.91-0.94 7.5-0.94 16.69 0 30.21 13.53 30.21 30.22C256.043 165.489 254.273 171.119 251.203 175.839z" />
      <g>
        <path fill="none" stroke="#59351C" stroke-width="1" stroke-linecap="round" d="M160.321 181.962c0 0-1.144-2.095 0.864-5.069"/>
        <path fill="#ED6E46" stroke="#ED6E46" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" d="M170.869 192.267c-0.599 6.451-4.196 11.391-8.032 11.034 -0.803-0.075-1.553-0.376-2.229-0.863 -0.575 0.41-1.21 0.676-1.895 0.78 -3.81 0.578-7.685-4.142-8.66-10.546 -0.975-6.405 1.324-12.068 5.132-12.646 1.775-0.27 3.564 0.612 5.07 2.278 1.371-1.623 3.04-2.522 4.756-2.361C168.845 180.301 171.468 185.819 170.869 192.267z" />
      </g>
      <g>
        <path fill="none" stroke="#59351C" stroke-width="1" stroke-linecap="round" d="M191.058 145.324c0 0-1.209-2.214 0.913-5.356"/>
        <path class="apple-top" fill="#ED6E46" stroke="#ED6E46" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" d="M202.205 156.214c-0.633 6.817-4.434 12.038-8.488 11.66 -0.849-0.079-1.641-0.397-2.356-0.912 -0.608 0.433-1.279 0.715-2.002 0.824 -4.026 0.611-8.121-4.377-9.151-11.145 -1.03-6.768 1.4-12.753 5.423-13.364 1.876-0.285 3.766 0.646 5.358 2.408 1.449-1.715 3.213-2.665 5.026-2.495C200.066 143.568 202.838 149.4 202.205 156.214z" />
      </g>
      <g>
        <path fill="none" stroke="#59351C" stroke-width="1" stroke-linecap="round" d="M226.558 180.564c0 0-1.209-2.214 0.913-5.356"/>
        <path class="right-apple" fill="#ED6E46" stroke="#ED6E46" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" d="M237.705 191.454c-0.633 6.817-4.434 12.038-8.488 11.66 -0.849-0.079-1.641-0.397-2.356-0.912 -0.608 0.433-1.279 0.715-2.002 0.824 -4.026 0.611-8.121-4.377-9.151-11.145 -1.03-6.768 1.4-12.753 5.423-13.364 1.876-0.285 3.766 0.646 5.358 2.408 1.449-1.715 3.213-2.665 5.026-2.495C235.566 178.808 238.338 184.64 237.705 191.454z" />
      </g>
    </g>
    <desc>Yellow sun moving from left to right.</desc>
    <circle class="sun" fill="#F9EC48" cx="57" cy="90" r="27" filter="url(#10)" name="sun">
        <!--Sun Animation-->
        <animate attributeName="cx" values="57;320;57" dur="10s" repeatCount="indefinite" />
        <animate attributeName="cy" values="100;70;100;70;100" dur="10s" repeatCount="indefinite" />
    </circle>
  </svg>
"""



def svg_demo():
    wp = jp.WebPage()
    g = jp.parse_html(sun_html, a=wp)
    g.name_dict["tree"].filter = f'url(#{g.name_dict["tree_filter"].id})'
    g.name_dict["sun"].filter = f'url(#{g.name_dict["sun_filter"].id})'
    return wp

jp.justpy(svg_demo)
```

Use example in hello.py in tests



