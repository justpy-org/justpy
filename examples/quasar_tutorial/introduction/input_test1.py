# Justpy Tutorial demo input_test1 from docs/quasar_tutorial/introduction.md
import justpy as jp

def input_test1(request):
    wp = jp.QuasarPage()
    c1 = jp.Div(classes='q-pa-md', a=wp)
    c2 = jp.Div(classes='q-gutter-md', style='max-width: 300px', a=c1)
    icon1 = jp.QIcon(name='event', color='blue')
    icon2 = jp.QIcon(name='place', color='red')
    for slot in ['append', 'prepend', 'before']:
        in1 = jp.QInput(label=slot, filled=True, hint=f'Icon is in slot "{slot}" and "after"', a=c2, after_slot=icon2)
        setattr(in1, slot + '_slot', icon1)
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("input_test1",input_test1)
