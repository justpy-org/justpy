# Justpy Tutorial demo input_demo1 from docs/tutorial/input.md
import justpy as jp

input_classes = "m-2 bg-gray-200 border-2 border-gray-200 rounded w-64 py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-purple-500"

def input_demo1(request):
    wp = jp.WebPage()
    in1 = jp.Input(a=wp, classes=input_classes, placeholder='Please type here')
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("input_demo1",input_demo1)
