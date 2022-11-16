# Justpy Tutorial demo custom_comp_test2 from docs/tutorial/custom_components.md
import justpy as jp

class PillButton(jp.Button):

    def __init__(self, **kwargs):
        self.bg_color = 'blue'
        super().__init__(**kwargs)
        self.set_classes(f'bg-{self.bg_color}-500 hover:bg-{self.bg_color}-700 text-white font-bold py-2 px-4 rounded-full')

def custom_comp_test2():
    wp = jp.WebPage()
    for color in ['blue', 'red', 'yellow', 'pink']:
        PillButton(bg_color=color, text='Pill Button', click='self.text="I was clicked"', a=wp, classes='m-2')
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("custom_comp_test2",custom_comp_test2)
