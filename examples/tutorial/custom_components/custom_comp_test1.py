# Justpy Tutorial demo custom_comp_test1 from docs/tutorial/custom_components.md
import justpy as jp

class PillButton(jp.Button):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_classes('bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full')


def custom_comp_test1():
    wp = jp.WebPage()
    for i in range(5):
        PillButton(text='Pill Button', click='self.text="I was clicked"', a=wp, classes='m-2')
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("custom_comp_test1",custom_comp_test1)
