# Justpy Tutorial demo calculator_test3 from docs/tutorial/custom_components.md
from justpy import Div, Input, Button, WebPage, justpy
import justpy as jp

class Calculator(Div):

    btn_classes = 'w-1/4 text-xl font-bold p-2 m-1 border bg-gray-200 hover:bg-gray-700 shadow'
    layout_text = [['7', '8', '9', '*'], ['4', '5', '6', '-'], ['1', '2', '3', '+'], ['C', '0', '.', '=']]

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.value = 0
        self.tape = Input(classes='block p-2 m-2  border text-right text-sm bg-gray-200', a=self, readonly=True, value=' ', style='width: 90%')
        self.result = Input(classes='block p-2 m-2 border text-2xl text-right', a=self, readonly=True, value='0', style='width: 90%')
        for line in type(self).layout_text:
            d = Div(classes='flex w-auto m-2', a=self)
            for b in line:
                b1 = Button(text=b, a=d, classes=type(self).btn_classes, click=self.calculator_click)
                b1.calc = self

    @staticmethod
    async def calculator_click(self, msg):
        calc = self.calc
        try:
            tape_value = eval(calc.tape.value)
        except:
            tape_value = 0
        changed = False
        if self.text == 'C':
            calc.result.value = '0'
            calc.tape.value = ' '
            if calc.value != 0:
                calc.value = 0
                changed = True
        elif self.text == '=':
            if calc.value != tape_value:
                calc.value = tape_value
                changed = True
            calc.result.value = str(tape_value)
            calc.tape.value = str(tape_value)
        else:
            if calc.tape.value[-1] in '*+-/' or self.text in '*+-/':
                calc.tape.value += ' ' + self.text
            else:
                calc.tape.value += self.text
            try:
                tape_value = eval(calc.tape.value)
                calc.result.value = str(tape_value)
                if calc.value != tape_value:
                    calc.value = tape_value
                    changed = True
            except:
                pass
        if changed:
            calc.set_model(calc.value)  #******************** updates model
            if calc.has_event_function('change'):
                calc_msg = msg
                calc_msg.event_type = 'change'
                calc_msg.id = calc.id
                calc_msg.button_text = self.text
                calc_msg.value = calc.value
                calc_msg.class_name = calc.__class__.__name__
                return await calc.run_event_function('change', calc_msg)

    def model_update(self):
        pass

def calculator_test3():
    wp = WebPage(data={'value': 0})
    Calculator(a=wp, classes='m-1 border inline-block', style='width: 250px', model=[wp, 'value'])
    for i in range(5):
        Div(classes='border m-2 p-1 w-64 text-xl', text='0', a=wp, model=[wp, 'value'])
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("calculator_test3",calculator_test3)
