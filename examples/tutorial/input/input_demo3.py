# Justpy Tutorial demo input_demo3 from docs/tutorial/input.md
import justpy as jp

input_classes = "m-2 bg-gray-200 border-2 border-gray-200 rounded w-64 py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-purple-500"
p_classes = 'm-2 p-2 h-32 text-xl border-2'

def my_input2(self, msg):
    self.div.text = self.value

def input_demo3(request):
    wp = jp.WebPage()
    in1 = jp.InputChangeOnly(a=wp, classes=input_classes, placeholder='Please type here')
    in1.div = jp.Div(text='What you type will show up here only when Input element loses focus or you press Enter',
                     classes=p_classes, a=wp)
    in1.on('input', my_input2)
    in1.on('change', my_input2)
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("input_demo3",input_demo3)
