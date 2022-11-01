# Justpy Tutorial demo input_test7 from docs/quasar_tutorial/quasar_components.md
import justpy as jp

def input_test7(request):
    wp = jp.QuasarPage()
    c1 = jp.Div(classes='q-pa-md', a=wp)
    c2 = jp.Div(classes='q-gutter-md', style='max-width: 300px', a=c1)

    password_input = jp.QInput(filled=True,  type='password', a=c2, hint="Password with toggle")
    visibility_icon = jp.QIcon(name='visibility_off', classes='cursor-pointer')
    visibility_icon.password_input = password_input

    password_input.append_slot = visibility_icon

    def toggle_password(self, msg):
        if self.name == 'visibility_off':
            self.name = 'visibility'
            self.password_input.type='text'
        else:
            self.name = 'visibility_off'
            self.password_input.type = 'password'

    visibility_icon.on('click', toggle_password)

    return wp

# initialize the demo
from examples.basedemo import Demo
Demo("input_test7", input_test7)
