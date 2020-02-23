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