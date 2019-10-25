import justpy as jp

class MyHello(jp.Hello):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.classes = 'm-1 p-1 text-6xl text-center text-red-500 bg-yellow-500 hover:bg-yellow-800 cursor-pointer'
        self.text = 'Much Better Hello! (click me)'

wp = jp.WebPage().add(*[MyHello() for i in range(5)])

def hello_test():
    return wp

jp.justpy(hello_test)

import random

input_classes = 'm-2 bg-gray-200 appearance-none border-2 border-gray-200 rounded w-64 py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-purple-500'
button_classes = 'w-32 m-2 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full'
letter_classes = 'rounded-full bg-blue-500 text-white text-6xl'

# return jp.WebPage().add(*[jp.Hello()]*5)
def animate(self, msg):
    self.d.components = []  # remove all components from d
    directions = ['Up', 'Down', 'Left', 'Right']
    for letter in self.in1.value:
        letter = '&nbsp;' if letter == ' ' else letter  # Hard space for HTML, otherwise space ignored
        jp.Div(animation=f'slideIn{random.choice(directions)}', text=letter, temp=True,
               classes=letter_classes, a=self.d)


def animation_test():
    wp = jp.WebPage()
    in1 = jp.Input(a=wp, classes=input_classes, placeholder='Enter text to animate', value='Animation Demo!',  change='return True')
    in1.disable_events = True
    b = jp.Button(text='Animate!', click=animate, classes=button_classes, a=wp)
    b.in1 = in1
    d = jp.Div(classes='flex items-center justify-center', style='height: 500px', a=wp)
    b.d = d
    return wp

# jp.justpy(animation_test)