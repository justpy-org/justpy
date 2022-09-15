# Justpy Tutorial demo input_demo2 from docs/tutorial/input.md
import justpy as jp

input_classes = "m-2 bg-gray-200 border-2 border-gray-200 rounded w-64 py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-purple-500"
p_classes = 'm-2 p-2 h-32 text-xl border-2'

def my_input1(self, msg):
    self.div.text = self.value

def input_demo2(request):
    wp = jp.WebPage()
    in1 = jp.Input(a=wp, classes=input_classes, placeholder='Please type here')
    in1.div = jp.Div(text='What you type will show up here', classes=p_classes, a=wp)
    in1.on('input', my_input1)
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("input_demo2",input_demo2)
