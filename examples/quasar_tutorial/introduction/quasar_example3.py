# Justpy Tutorial demo quasar_example3 from docs/quasar_tutorial/introduction.md
import justpy as jp

def quasar_example3():
    wp = jp.QuasarPage()
    d = jp.Div(classes='q-pa-md row justify-center', a=wp)
    jp.QDiv(v_ripple=True, classes='relative-position flex flex-center text-white bg-primary',
                style='border-radius: 3px; cursor: pointer; height: 150px; width: 80%;',
                a=d, text='Click/tap me')
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("quasar_example3",quasar_example3)
