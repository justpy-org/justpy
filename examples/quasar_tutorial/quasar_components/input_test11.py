# Justpy Tutorial demo input_test11 from docs/quasar_tutorial/quasar_components.md
import justpy as jp

def input_test11():
    wp = jp.QuasarPage()
    in1 = jp.QInput(label='Enter email', style='width: 150px; margin: 20px', a=wp, lazy_rules=False)
    in1.rules = ["val => val.length <= 3 || 'Please use maximum 3 characters'"]
    return wp

# initialize the demo
from examples.basedemo import Demo
Demo("input_test11", input_test11)
