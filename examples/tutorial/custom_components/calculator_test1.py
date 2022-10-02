# Justpy Tutorial demo calculator_test1 from docs/tutorial/custom_components.md
import justpy as jp
from justpy import Div, Input, Button, WebPage, justpy

class Calculator(Div):

    btn_classes = 'w-1/4 text-xl font-bold p-2 m-1 border bg-gray-200 hover:bg-gray-700 shadow'
    layout_text = [['7', '8', '9', '*'], ['4', '5', '6', '-'], ['1', '2', '3', '+'], ['C', '0', '.', '=']]

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.value = 0
        self.tape = Input(classes='block p-2 m-2  border text-right text-sm bg-gray-200', a=self, readonly=True, value=' ', style='width: 90%')
        self.result = Input(classes='block p-2 m-2 border text-2xl text-right', a=self, readonly=True, value='0', style='width: 90%')
        for line in self.__class__.layout_text:
            d = Div(classes='flex w-auto m-2', a=self)
            for b in line:
                b1 = Button(text=b, a=d, classes=self.__class__.btn_classes, click=self.calculator_click)
                b1.calc = self

    @staticmethod
    def calculator_click(self, msg):
        calc = self.calc
        if self.text == 'C':
            calc.result.value = '0'
            calc.tape.value = ' '
            calc.value = 0
        elif self.text == '=':
            calc.result.value = str(eval(calc.tape.value))
            calc.value = eval(calc.tape.value)
            calc.tape.value = calc.result.value
        else:
            if calc.tape.value[-1] in '*+-/' or self.text in '*+-/':
                calc.tape.value += ' ' + self.text
            else:
                calc.tape.value += self.text
            try:
                calc.result.value = str(eval(calc.tape.value))
                calc.value = eval(calc.tape.value)
            except:
                pass


def calculator_test1():
    wp = WebPage()
    for i in range(10):
        c = Calculator(a=wp, classes='m-1 border inline-block', style='width: 250px')
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("calculator_test1",calculator_test1)
