# Justpy Tutorial demo animation_test from docs/reference/htmlcomponent.md
import justpy as jp
import random

input_classes = "m-2 bg-gray-200 appearance-none border-2 border-gray-200 rounded w-64 py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-purple-500"


def animate(self, msg):
    self.d.delete_components()  # remove all components from d
    directions = ['Up', 'Down', 'Left', 'Right']
    html_entity = False
    for letter in self.text_to_animate.value:
        if letter == ' ':
            letter = '&nbsp;'
            html_entity = True
        jp.Div(animation=f'fadeIn{random.choice(directions)}', text=letter, html_entity=html_entity,
               classes='rounded-full bg-blue-500 text-white text-6xl', a=self.d)
        html_entity = False


def animation_test():
    wp = jp.WebPage()
    text_to_animate = jp.Input(a=wp, classes=input_classes, placeholder='Enter text to animate', value='Animation Demo!', input='return True')
    animate_btn = jp.Button(text='Animate!', click=animate, classes='w-32 m-2 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded', a=wp)
    animate_btn.text_to_animate= text_to_animate
    d = jp.Div(classes='flex items-center justify-center', style='height: 500px', a=wp)
    animate_btn.d = d
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("animation_test",animation_test)
