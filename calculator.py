from justpy import *


class CalendarDateJP(Div):

    def __init__(self, **kwargs):
        self.month = 'Jan'
        self.year = '2010'
        self.weekday = 'Sun'
        self.day = '1'
        super().__init__(**kwargs)
        self.template_string = """
        <div class="w-24 flex-no-shrink rounded-t overflow-hidden bg-white text-center m-2">
            <div class="bg-red-500 text-white py-1">
                {{ month }}
            </div>
            <div class="pt-1 border-l border-r">
                <span class="text-4xl font-bold">{{ day }}</span>
            </div>
            <div class="pb-2 px-2 border-l border-r border-b rounded-b flex justify-between">
                <span class="text-xs font-bold">{{ weekday }}</span>
                <span class="text-xs font-bold">{{ year }}</span>
            </div>
        </div>

        """

    def convert_object_to_dict(self):  # Every object needs to redefine this
        d = super().convert_object_to_dict()
        # Add read from file capability
        # with open('template.html.jinja2') as file_:
        #     template = Template(file_.read())
        self.template = Template(self.template_string)
        d['inner_html'] = self.template.render(month=self.month, day=self.day, weekday=self.weekday, year=self.year)
        return d


class Calculator(Div):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        def calculator_click(self, msg):
            calc = self.calculator
            if self.text == 'C':
                calc.result.value = '0'
                calc.tape.value = ' '
            elif self.text == '=':
                calc.result.value = str(eval(calc.tape.value))
                calc.tape.value = calc.result.value
            else:
                if calc.tape.value[-1] in '*+-/' or self.text in '*+-/':
                    calc.tape.value += ' ' + self.text
                else:
                    calc.tape.value += self.text
                try:
                    calc.result.value = str(eval(calc.tape.value))
                except:
                    pass

        self.tape = Input(classes='block p-2 m-2  border text-right text-sm bg-gray-200', a=self, readonly=True, value=' ', style='width: 90%')
        self.result = Input(classes='block p-2 m-2 border text-2xl text-right', a=self, readonly=True, value='0', style='width: 90%')
        btn_classes = 'w-1/4 text-xl font-bold p-2 m-1 border bg-gray-200 hover:bg-gray-700 shadow'
        layout_text = [['7', '8', '9', '*'], ['4', '5', '6', '-'], ['1', '2', '3', '+'], ['C', '0', '.', '=']]
        for line in layout_text:
            d = Div(classes='flex w-auto m-2', a=self)
            for b in line:
                b1 = Button(text=b, a=d, classes=btn_classes, click=calculator_click)
                b1.calculator = self



def calculator_component():
    wp = WebPage()
    for i in range(10):
        c = Calculator(a=wp, classes='m-1 border inline-block', style='width: 250px')
    return wp

justpy(calculator_component)
