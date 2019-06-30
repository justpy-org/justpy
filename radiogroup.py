from justpy import *


class RadioGroup(Div):
    def __init__(self,  **kwargs):
        self.radio_list = []
        self.options = []
        self.group_name = 'radio_group_name'
        self.item_classes= ''
        self.value = ''
        super().__init__(**kwargs)
        self._options = copy.deepcopy(self.options)  #self.options.copy()
        self.set_class('flex')
        self.radio_components = []  # A list of the Input components with type='radio'. Needed for model parameter
        for option in self._options:
            if 'value' not in option:
                option['value'] = ''
            if 'label' not in option:
                option['label'] = ''
            if 'classes' not in option:
                option['classes'] = self.item_classes
            outer_div = Div(a=self, classes='m-1')
            item_label = Label(a=outer_div)
            in1 = Input(type='radio', classes='form-radio ', value=option['value'], name=self.group_name, a=item_label, change=self.change_function, parent=self)
            in1.event_propagation = False
            self.radio_components.append(in1)
            temp_span = Span(classes=option['classes'], text=option['label'], a=item_label)
        return



    @staticmethod
    async def change_function(radio_button, msg):
        radio_button.parent.value = msg.value
        # Need to update model here. Done in before for individual radio buttons
        if hasattr(radio_button.parent, 'model'):
            radio_button.parent.model[0].data[radio_button.parent.model[1]] = msg.value
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

    def model_update(self):
        self.value = self.model[0].data[self.model[1]]
        # Modify the checked value of the radio buttons to reflect new value
        for r in self.radio_components:
            if r.value == self.value:
                r.checked = True
            else:
                r.checked = False


    def convert_object_to_dict(self):    # Every object needs to redefine this

        d = super().convert_object_to_dict()
        return d

async def radio_change(self, msg):
    print('in radion change')
    Div(text=msg.value, a=msg.page, classes='m-2 text-lg')
    # self.value = 'op3'
    self.in2.value += msg.value


def check_click(self, msg):
    self.in1.checked = not self.in1.checked
    print(msg.page.data['radio'])
    if self.in1.checked:
        msg.page.data['radio'] = 'op1'
    else:
        msg.page.data['radio'] = 'op3'
    print(self.in1.checked)

radio_options = [
        {
          'label': 'Option 1',
          'value': 'op1'
        },
        {
          'label': 'Option 2',
          'value': 'op2'
        },
        {
          'label': 'Option 3',
          'value': 'op3'
        }
      ]

radio_options_2 = [
        {
          'label': 'Option 1',
          'value': 'op1'
        },
        {
          'label': 'Option 2',
          'value': 'op2'
        },
        {
          'label': 'Option 3',
          'value': 'op3'
        }
      ]
# TODO: Use this as an example of model
def comp_test(request):
    wp = WebPage(data={'radio': 'op3'})
    print(wp)
    # my_list = ListComponent(a=wp)
    f1 = Form(a=wp)
    print(f1)
    # my_list = RadioGroup(radio_list=list('abcde'), a=f1, item_classes='ml-2')
    my_list = RadioGroup(options=radio_options, a=f1, item_classes='ml-2', model=[wp, 'radio'])
    my_list.on('change', radio_change)
    Div(text='--------------', a=wp, classes='m-2')
    in1 = Input(type='checkbox', classes='form-checkbox', a=wp, checked=True)
    Br(a=wp)
    b = Button(text='click me', click=check_click, classes='m-1 p-1 resize', a=wp)
    b.in1 = in1
    Div(text='--------------', a=wp, classes='m-2 resize')
    print(Br(a=wp))
    in2 = TextArea(classes='text-xl m-1 border resize shadow-2xl', a=wp)
    print(in2)
    my_list.in2 = in2
    Div(text='--------------', a=wp, classes='m-2 resize')
    f2 = Form(a=wp)
    my_list1 = RadioGroup(options=radio_options, a=f2, item_classes='text-xl text-white bg-blue-400 mr-2 ml-2 p-1')
    in1 = Input(type='text', classes='border text-xl', a=wp, model=[wp, 'radio'])
    # print(my_list.has_event_function('change'))
    print(wp)
    return wp

def model_test(request):
    # wp1 = WebPage(data={'flag': True})
    wp1 = WebPage()
    wp = Div(a=wp1, data={'flag': True})
    # wp.data['flag'] = True
    # in1 = jp.TextArea(placeholder='test', classes='m-1 p-1 border text-xl', a=wp, model=[wp, 'initial'])
    for i in range(10):
        in1 = Input(type='checkbox', classes='form-checkbox m-2', a=wp, model=[wp, 'flag'])
        Br(a=wp)
    Br(a=wp)
    in2 = Input(type='text', classes='border text-xl shadow-lg ml-2', a=wp, model=[wp, 'flag'])
    return wp1

def my_radio_change(self, msg):
    print('in radio change', self)
    print(msg)
    print(msg.page.data)
    # msg.page.data['radio'] = 'fiat'



def radio_test(request):
    wp = WebPage(data={'radio': 'audi'})
    f = Form(a=wp, classes='m-1')
    r = Input(type='radio', name='cat1', value='volvo', a=f, classes='form-radio m-2', change=my_radio_change, model=[wp, 'radio'])
    Span(text='Volvo', a=f)
    r = Input(type='radio', name='cat1', value='audi', a=f, classes='form-radio m-2', change=my_radio_change, model=[wp, 'radio'])
    Span(text='Audi', a=f)
    r = Input(type='radio', name='cat1', value='fiat', a=f, change=my_radio_change, classes='form-radio m-2', model=[wp, 'radio'])
    Span(text='Fiat', a=f)
    Br(a=f)
    r = Input(type='checkbox', name='cat1123', value='volvocheck', a=f, change=my_radio_change, model=[wp, 'radio'])
    b = Button(text='Click me now', a=f)
    Br(a=f)
    in1 = TextArea( classes='m-2 border', a=f, model=[wp, 'radio'])
    # in1 = TextArea( classes='m-2 border', a=f, text='this is text')

    in2 = Input( classes='m-2 border', a=f, model=[wp, 'radio'])
    d = Div(a=wp, model=[wp, 'radio'])
    select_string = '<select><option value="audi" >Audi</option><option value="african" selected>african</option><option value="airedale">airedale</option></select'
    s = parse_html(select_string, a=wp, classes='m-2 text-xl')
    s.model = [wp, 'radio']
    in3 = Input(classes='m-2 border', a=f, value='initial value')
    in3 = Input(type='checkbox',classes='form-checkbox m-2', a=f, checked=False)
    return wp



justpy(comp_test)
# justpy(model_test)
# justpy(radio_test)