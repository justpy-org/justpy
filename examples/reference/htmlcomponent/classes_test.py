# Justpy Tutorial demo classes_test from docs/reference/htmlcomponent.md
import justpy as jp

def classes_test():
    wp = jp.WebPage()
    d = jp.Div(text='Classes Example', a=wp)
    # Assign Tailwind classes to d
    d.classes = 'text-5xl text-white bg-blue-500 hover:bg-blue-700 m-2 p-2 w-64'
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("classes_test",classes_test)
