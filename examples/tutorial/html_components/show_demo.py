# Justpy Tutorial demo show_demo from docs/tutorial/html_components.md
import justpy as jp

button_classes='m-2 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded'

def show_demo():
    wp = jp.WebPage()
    b = jp.Button(text='Click to toggle show', a=wp, classes=button_classes)
    d = jp.Div(text='Toggled by show', classes='m-2 p-2 text-2xl border w-48', a=wp)
    b.d = d
    jp.Div(text='Will always show', classes='m-2', a=wp)

    def toggle_show(self, msg):
        self.d.show = not self.d.show

    b.on('click', toggle_show)

    b = jp.Button(text='Click to toggle visibility', a=wp, classes=button_classes)
    d = jp.Div(text='Toggled by visible', classes='m-2 p-2 text-2xl border w-48', a=wp)
    d.visibility_state = 'visible'
    b.d = d
    jp.Div(text='Will always show', classes='m-2', a=wp)

    def toggle_visible(self, msg):
        if self.d.visibility_state == 'visible':
            self.d.set_class('invisible')
            self.d.visibility_state = 'invisible'
        else:
            self.d.set_class('visible')
            self.d.visibility_state = 'visible'

    b.on('click', toggle_visible)
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("show_demo",show_demo)
