# Justpy Tutorial demo focus_test_input from docs/tutorial/input.md
import justpy as jp

def my_blur(self, msg):
        self.set_focus = False

def key_down(self, msg):
    # print(msg.key_data)
    key = msg.key_data.key
    if key=='Escape':
        self.value=''
        return
    if key=='Enter':
        self.set_focus = False
        try:
            next_to_focus = self.input_list[self.num + 1]
        except:
            next_to_focus = self.input_list[0]
        next_to_focus.set_focus = True
        return
    return True  # Don't update the page


def focus_test_input():
    wp = jp.WebPage()
    d = jp.Div(classes='flex flex-col  m-2', a=wp, style='width: 600 px')
    input_list = []
    number_of_fields = 5
    for i in range(1, number_of_fields + 1):
        label = jp.Label( a=d, classes='m-2 p-2')
        jp.Span(text=f'Field {i}', a=label)
        in1 = jp.Input(classes=jp.Styles.input_classes, placeholder=f'{i} Type here', a=label, keydown=key_down, spellcheck="false")
        in1.on('blur', my_blur)
        in1.input_list = input_list
        in1.num = i - 1
        input_list.append(in1)
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("focus_test_input",focus_test_input)
