import justpy as jp
from justpy import WebPage, Input
from justpy import *


d = jp.Div(classes='m-2 h-1/2 border')

async def comp_update_test(request):
    global d
    wp = WebPage()
    jp.Div(text='Chat', classes='text-3xl', a=wp)
    in1 = jp.Input(placeholder='Enter text', a=wp, classes='m-2')
    b = jp.Button(text='Add', a=wp, classes='m-2 p-2 text-blue-500 bg-white hover:bg-blue-200 hover:text-blue-500 border')

    wp.add(d)
    d.pages.append(wp)
    print(d.pages)
    b.in1 = in1
    b.d = d
    b.show = True
    async def b_click(self, msg):
        msg_div = jp.Div(text=self.in1.value)
        self.d.add(msg_div)
        await self.d.update()
        return True
    b.on('click', b_click)
    return wp


def mouse_test(request):
    wp = WebPage()
    d = jp.Div(text='initial', a=wp, classes='text-5xl')
    def m_enter(self, msg):
        self.text = 'mouse inside'
    def m_leave(self, msg):
        self.text = 'mouse outside'
    d.on('mouseenter', m_enter)
    d.on('mouseleave', m_leave)
    return wp


def in_test(request):
    wp = WebPage()
    in1= Input(placeholder='type here', classes='text-xl m-1 p-1', a=wp)
    d = Div(classes='text-2xl m-1 p-1 w-1/3 h-64 overflow-auto', a=wp)
    in1.d = d
    def input_event(self, msg):
        d.text = self.value.upper()
    in1.on('input', input_event)
    return wp


class My_component(Div):

    def __init__(self,  **kwargs):
        self.div_nums = 5

        super().__init__(**kwargs)
        self.classes = 'text-xl text-white bg-red-500'
        for i in range(self.div_nums):
            self.add(Div(text='I am my component'))

def comp_test1(request):
    wp = WebPage()
    wp.add(My_component(div_nums=13))
    return wp


class ListComponent(Ul):

    def __init__(self,  **kwargs):
        self.item_list = []

        super().__init__(**kwargs)
        self.classes = 'list-disc list-outside bg-gray-200 text-gray-800 py-2 m-4'

    def convert_object_to_dict(self):    # Every object needs to redefine this
        self.components = []
        for i in self.item_list:
            self.add(Li(text=i, classes=''))
        d = super().convert_object_to_dict()
        return d
import inspect

async def radio_change(self, msg):
    print('in radion change')
    # print(inspect.getframeinfo(inspect.currentframe()).lineno, msg)
    # print(inspect.getframeinfo(inspect.currentframe()).filename, inspect.getframeinfo(inspect.currentframe()).lineno, msg)
    Div(text=msg.value, a=msg.page, classes='m-2 text-lg')
    self.value = 'e'
    for c in self.components:
        c.set_class('outline-none')

def comp_test(request):
    wp = WebPage()
    # my_list = ListComponent(a=wp)
    f1 = Form(a=wp)
    my_list = RadioGroup(radio_list=list('abcde'), a=f1, item_classes='ml-2')
    my_list.on('change', radio_change)
    Div(text='--------------', a=wp, classes='m-2')
    in1 = Input(type='checkbox', classes='form-checkbox', a=wp, checked=True)
    b = Button(text='click me', click=check_click, classes='m-1 p-1 resize', a=wp)
    b.in1 = in1
    Div(text='--------------', a=wp, classes='m-2 resize')
    Br(a=wp)
    in2 = TextArea(classes='text-xl m-1 border resize shadow-2xl', a=wp)
    Div(text='--------------', a=wp, classes='m-2 resize')
    f2 = Form(a=wp)
    my_list1 = RadioGroup(radio_list=list('abcde'), a=f2, item_classes='text-xl text-white bg-blue-400 ml-2')
    # print(my_list.has_event_function('change'))
    return wp

class RadioGroup(Div):
# Need maybe prevent default ******** YES
    def __init__(self,  **kwargs):
        self.radio_list = []
        self.name = 'radio_group_name'
        self.item_classes= ''
        self.value = ''
        super().__init__(**kwargs)
        self.radio_components = []
        for counter, radio_text in enumerate(self.radio_list):
            outer_div = Div(a=self, classes='m-1')
            item_label = Label(a=outer_div)
            in1 = Input(type='radio', classes='form-radio ', value=radio_text, name=self.name, a=item_label, change=self.change_function, parent=self)
            # in1.events = ['change']
            in1.event_propagation = False
            self.radio_components.append(in1)
            temp_span = Span(classes=self.item_classes, text=radio_text, a=item_label)


    @staticmethod
    async def change_function(radio_button, msg):
        radio_button.parent.value = msg.value
        if radio_button.parent.has_event_function('change'):
            event_function = getattr(radio_button.parent, 'on_' + 'change')
            event_result = await event_function(msg)
            return event_result
        else:
            logging.warning('%s', 'No event handler: "change" for RadioGroup ')  # Function was not defined

    def react(self, data):
        for c in self.radio_components:
            if c.value == self.value:
                c.checked = True
            else:
                c.checked = False


    def convert_object_to_dict(self):    # Every object needs to redefine this

        d = super().convert_object_to_dict()
        return d

def check_click(self, msg):
    self.in1.checked = not self.in1.checked
    print(self.in1.checked)

def test_checkbox(request):
    wp = WebPage()
    in1 = Input(type='checkbox', classes='form-checkbox', a=wp)
    b = Button(text='click me', click=check_click, classes='m-1 p-1', a=wp)
    b.in1 = in1
    # in1.checked = True
    return wp


jp.justpy(comp_test)
# jp.justpy(test_checkbox)

