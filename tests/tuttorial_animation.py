import justpy as jp
import random


def animate(self, msg):
    self.d.delete_components()  # remove all components from d
    directions = ['Up', 'Down', 'Left', 'Right']
    for letter in self.in1.value:
        letter = '&nbsp;' if letter == ' ' else letter  # Hard space for HTML, otherwise space ignored
        jp.Div(animation=f'slideIn{random.choice(directions)}', text=letter,
               classes='rounded-full bg-blue-500 text-white text-6xl', a=self.d, temp=True)


def animation_test():
    wp = jp.WebPage()
    input_classes = "m-2 bg-gray-200 appearance-none border-2 border-gray-200 rounded w-64 py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-purple-500"
    in1 = jp.Input(a=wp, classes=input_classes, placeholder='Enter text to animate', value='Animation Demo!', input='return True', change='return True')
    in1.disable_events = True
    b = jp.Button(text='Animate!', click=animate, classes='w-32 m-2 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded', a=wp)
    b.in1 = in1
    d = jp.Div(classes='flex items-center justify-center', style='height: 500px', a=wp)
    b.d = d
    return wp

jp.justpy(animation_test, websockets=False)

