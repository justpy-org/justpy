# Justpy Tutorial demo input_test10 from docs/quasar_tutorial/quasar_components.md
import justpy as jp
import re

email_regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

def input_change(self, msg):
    print(self.value)
    if re.match(email_regex,self.value):
        self.error = False
    else:
        self.error = True
        self.error_message = 'Enter valid email address'
        self.bottom_slots = True


def input_test10():
    wp = jp.QuasarPage()
    in1 = jp.QInput(label='Enter email', style='width: 150px; margin: 20px', a=wp, input=input_change)
    return wp


# initialize the demo
from examples.basedemo import Demo
Demo("input_test10", input_test10)
