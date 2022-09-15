# Justpy Tutorial demo input_demo5 from docs/tutorial/input.md
import justpy as jp

class InputWithDiv(jp.Div):

    input_classes = "m-2 bg-gray-200 border-2 border-gray-200 rounded w-64 py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-purple-500"

    @staticmethod
    def input_handler(self, msg):
        self.div.text = self.value

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.in1 = jp.Input(a=self, classes=self.input_classes, placeholder='Please type here', input=self.input_handler)
        self.in1.div = jp.Div(text='What you type will show up here', classes='m-2 p-2 h-32 text-xl border-2', a=self)


def input_demo5(request):
    wp = jp.WebPage()
    for i in range(10):
        InputWithDiv(a=wp)
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("input_demo5",input_demo5)
