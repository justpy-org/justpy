import justpy as jp
import re

email_regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

def input_change(self, msg):
    print(self.value)
    # if self.value != 'hello':
    if re.match(email_regex,self.value):
        self.error = False
        # self.error_message = 'Do not type 1!'
    else:
        self.error = True
        self.error_message = 'Enter valid email address'
        self.bottom_slots = True


def input_test():
    wp = jp.QuasarPage()
    in1 = jp.QInput(label='Enter email', style='width: 150px; margin: 20px', a=wp, input=input_change)
    return wp


jp.justpy(input_test)
