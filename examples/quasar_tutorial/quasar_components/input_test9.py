# Justpy Tutorial demo input_test9 from docs/quasar_tutorial/quasar_components.md
import justpy as jp

def input_test9(request):
    wp = jp.QuasarPage(data={'text': ''})
    c1 = jp.Div(classes='q-pa-md', a=wp)
    c2 = jp.Div(classes='q-gutter-md', style='max-width: 300px', a=c1)
    jp.QInput(filled=True, label='Phone', mask='(###) ### - ####', hint="Mask: (###) ### - ####", a=c2)
    return wp

# initialize the demo
from examples.basedemo import Demo
Demo("input_test9", input_test9)
