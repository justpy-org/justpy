# Justpy Tutorial demo svg_demo2 from docs/tutorial/svg_components.md
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


# initialize the demo
from  examples.basedemo import Demo
Demo ("svg_demo2",svg_demo2)
