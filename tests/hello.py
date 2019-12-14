from justpy import Div
import justpy as jp

class TabGroup(Div):
    """
    Displays a tab based on its value. Has a dict of tabs whose keys is the value. A tab is any JustPy component.

    format of dict: {'value1': {'tab': comp1, 'order': number}, 'value2': {'tab': comp2, 'order': number} ...}
    self.tabs - tab dict
    self.animation_next = 'slideInRight'    set animation for tab coming in
    self.animation_prev = 'slideOutLeft'    set animation for tab going out
    self.animation_speed = 'faster'  can be on of  '' | 'slow' | 'slower' | 'fast'  | 'faster'
    self.value  value of group and tab to display
    self.previous - previous tab, no need to change except to set to '' in order to dislpay tab without animation which is default at first

    """

    wrapper_classes = ' '
    wrapper_style = 'display: flex; position: absolute; width: 100%; height: 100%;  align-items: center; justify-content: center; background-color: #fff;'

    def __init__(self, **kwargs):

        self.tabs = {}  # Dict with format 'value': {'tab': Div component, 'order': number} for each entry
        self.value = ''
        self.previous_value = ''
        # https://github.com/daneden/animate.css
        self.animation_next = 'slideInRight'
        self.animation_prev = 'slideOutLeft'
        self.animation_speed = 'faster'  # '' | 'slow' | 'slower' | 'fast'  | 'faster'

        super().__init__(**kwargs)

    def __setattr__(self, key, value):
        if key == 'value':
            try:
                self.previous_value = self.value
            except:
                pass
        self.__dict__[key] = value

    def model_update(self):
        self.value = self.model[0].data[self.model[1]]

    def convert_object_to_dict(self):  # Every object needs to redefine this
        self.components = []
        self.wrapper_div_classes = self.animation_speed  # Component in this will be centered

        if self.previous_value:
            self.wrapper_div = Div(classes=self.wrapper_div_classes, animation=self.animation_next, temp=True,
                                   style=f'{self.__class__.wrapper_style} z-index: 50;', a=self)
            self.wrapper_div.add(self.tabs[self.value]['tab'])
            self.wrapper_div = Div(classes=self.wrapper_div_classes, animation=self.animation_prev, temp=True,
                                   style=f'{self.__class__.wrapper_style} z-index: 0;', a=self)
            self.wrapper_div.add(self.tabs[self.previous_value]['tab'])
        else:
            self.wrapper_div = Div(classes=self.wrapper_div_classes, temp=True, a=self,
                                   style=self.__class__.wrapper_style)
            self.wrapper_div.add(self.tabs[self.value]['tab'])

        self.style = ' position: relative; overflow: hidden; ' + self.style  # overflow: hidden;
        d = super().convert_object_to_dict()
        return d

def my_click(self, msg):
    print(msg)
    self.text = 'clicked sdfasdf'

def tab_test():
    wp = jp.QuasarPage()
    jp.Button(text='click now', a=wp, click=my_click)
    jp.QBtn(label='click me', a=wp, click=my_click)
    return(wp)

jp.justpy(tab_test)