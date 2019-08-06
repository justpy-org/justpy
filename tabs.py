from justpy import *



class TabGroup(Div):
    """
    Displays a tab basedon its value. Has a dict of tabs whose keys is the value. A tab is any JustPy component.

    format of dict: {'value1': {'tab': comp1, 'order': number}, 'value2': {'tab': comp2, 'order': number} ...}
    self.tabs - tab dict
    self.animation_next = 'slideInRight'    set animation for tab coming in
    self.animation_prev = 'slideOutLeft'    set animation for tab going out
    self.animation_speed = 'faster'  can be on of  '' | 'slow' | 'slower' | 'fast'  | 'faster'
    self.value  value of group and tab to display
    self.previous - previous tab, no need to change except to set to '' in order to dispay tab without animation which is default at first

    """

    wrapper_classes = ' '
    wrapper_style = 'display: flex; position: absolute; width: 100%; height: 100%;  align-items: center; justify-content: center; background-color: #fff;'

    def __init__(self,  **kwargs):

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

    def convert_object_to_dict(self):    # Every object needs to redefine this
        self.components = []
        self.wrapper_div_classes = self.animation_speed # Component in this will be centered

        if self.previous_value:
            self.wrapper_div = Div(classes=self.wrapper_div_classes, animation=self.animation_next, temp=True, style=f'{self.__class__.wrapper_style} z-index: 50;', a=self )
            self.wrapper_div.add(self.tabs[self.value]['tab'])
            self.wrapper_div = Div(classes=self.wrapper_div_classes, animation=self.animation_prev, temp=True, style=f'{self.__class__.wrapper_style} z-index: 0;', a=self)
            self.wrapper_div.add(self.tabs[self.previous_value]['tab'])
        else:
            self.wrapper_div = Div(classes=self.wrapper_div_classes, temp=True, a=self, style=self.__class__.wrapper_style)
            self.wrapper_div.add(self.tabs[self.value]['tab'])

        self.style = ' position: relative; overflow: hidden; ' + self.style  # overflow: hidden;
        d = super().convert_object_to_dict()
        return d


def tab_test():
    wp = WebPage()
    # wp = QuasarPage()
    b = Button(text='Tab Change', classes='bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full faster', animation='bounceIn', a=wp)
    # b = QButton(text='Tab Change', animation='bounceIn', a=wp, color='primary')
    b.counter = -1

    tg = TabGroup(a=wp, value='hello', style='width: 500px; height:400px',classes='m-1 border')
    b.tg = tg
    tab_data = ['hello', 'Eli', 'Liat', 'Michael']
    for i,s in enumerate(tab_data):

        # d1 = Div(text=s, classes='text-h1')
        d1 = Div(text=s, classes='text-5xl')
        tg.tabs[s] = {'tab': d1, 'order': i}
    tg.value = 'Liat'
    tg.previous_value = ''
    # tg.animation_next = 'bounceInRight'
    # tg.animation_prev = 'bounceOutLeft'
    # tg.animation_next = 'rotateIn'
    # tg.animation_prev = 'rotateOut'
    # tg.animation_speed = 'slower'
    def my_click(self, msg):
        self.counter += 1
        # self.text = f'Tab: {self.counter}'
        # return
        flag = False
        for tab in self.tg.tabs:
            if self.counter == self.tg.tabs[tab]['order']:
                self.tg.value = tab
                flag = True
                self.text = f'Tab: {self.counter}'
        if not flag:
            self.counter = -1
            my_click(self, msg)
    b.on('click', my_click)
    return wp


def panels_tab_test():
    wp = QuasarPage()
    c = parse_html("""
    <div class="q-pa-md">
    <div class="" style="max-width: 600px" name="outer">
      <q-card>
        <q-tabs
          name="tab"
          dense
          class="text-grey"
          active-color="primary"
          indicator-color="primary"
          align="justify"
          narrow-indicator
        >
          <q-tab name="mails" label="Mails" />
          <q-tab name="alarms" label="Alarms" />
          <q-tab name="movies" label="Movies" />
        </q-tabs>

        <q-separator />
        </div>
        </div>
    """, a=wp)
    outer = c.name_dict['outer']
    outer.data = {'panel': 'mails'}
    tab = c.name_dict['tab']
    tab.value = 'mails'
    tab.model = [outer, 'panel']
    pg = TabGroup(a=outer, value='mails',  style='height: 70px; border-style: solid;  border-color: #e6e6e6; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06); ', classes= ' ')
    pg.model = [outer, 'panel']

    tab.pg = pg
    options = ['mails', 'alarms', 'movies']
    for i, opt in enumerate(options):
        tab_comp = parse_html(f"""
        <div class="q-pa-lg" style="width: 100%;">
        <div class="text-h6">{opt.capitalize()}</div>
            <span>Lorem ipsum dolor sit amet consectetur adipisicing elit.</span>
        </div>
        """)
        pg.tabs[opt] = {'tab': tab_comp, 'order': i}
    def tab_change(self, msg):
        self.pg.value = self.value
    # tab.on('input', tab_change)
    return wp


import random
def animation_test(request):
    wp = WebPage()
    s = request.query_params.get('s', 'Animation demo!')
    d = Div(classes='flex items-center justify-center h-screen w-screen',  a=wp)
    directions = ['Up', 'Down', 'Left', 'Right']
    for v in s:
        v = '&nbsp;' if v == ' ' else v  # Hard space for HTML, otherwise space ignored
        Div(animation=f'slideIn{random.choice(directions)}', text=v, classes='rounded-full bg-blue-500 text-white text-6xl slower', a=d)
    return wp

# justpy(tab_test)
justpy(animation_test)
# justpy(panels_tab_test)

