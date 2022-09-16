# Justpy Tutorial demo hello_test4 from docs/tutorial/custom_components.md
import justpy as jp

class MyHello(jp.Hello):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.classes = 'm-1 p-1 text-6xl text-center text-red-500 bg-yellow-500 hover:bg-yellow-800 cursor-pointer'
        self.text = 'Much Better Hello! (click me)'

def hello_test4():
    wp = jp.WebPage()
    for i in range(5):
        MyHello(a=wp, counter=100)
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("hello_test4",hello_test4)
