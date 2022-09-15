# Justpy Tutorial demo color_demo from docs/tutorial/input.md
import justpy as jp

def color_demo(request):
    wp = jp.WebPage()
    in1 = jp.Input(type='color', a=wp, classes='m-2 p-2', style='width: 100px; height: 100px', input=color_change, debounce=30)
    in1.d = jp.Div(text='Click box above to change color of this text', a=wp, classes='border m-2 p-2 text-2xl font-bold')
    return wp

def color_change(self, msg):
    self.d.style=f'color: {self.value}'
    self.d.text = f'The color of this text is: {self.value}'

# initialize the demo
from  examples.basedemo import Demo
Demo ("color_demo",color_demo)
