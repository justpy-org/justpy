from justpy import Div, WebPage, Ul, Li, HighCharts, A, justpy
import justpy as jp


class Tabs(Div):

    tab_label_classes = 'overflow-hidden cursor-pointer bg-white inline-block py-2 px-4 text-blue-500 hover:text-blue-800 font-semibold'
    tab_label_classes_selected = 'overflow-hidden cursor-pointer bg-white inline-block border-l border-t border-r rounded-t py-2 px-4 text-blue-700 font-semibold'
    item_classes = 'flex-shrink mr-1'
    item_classes_selected = 'flex-shrink -mb-px mr-1'
    wrapper_style = 'display: flex; position: absolute; width: 100%; height: 100%;  align-items: center; justify-content: center; background-color: #fff;'

    def __init__(self, **kwargs):

        self.tabs = []  # list of {'id': id, 'label': label, 'content': content}
        self.value = None  # The value of the tabs component is the id of the selected tab
        self.content_height = 500
        self.last_rendered_value = None
        self.animation = False
        self.animation_next = 'slideInRight'
        self.animation_prev = 'slideOutLeft'
        self.animation_speed = 'faster'  # '' | 'slow' | 'slower' | 'fast'  | 'faster'

        super().__init__(**kwargs)

        self.tab_list = Ul(classes="flex flex-wrap border-b", a=self)
        self.content_div = Div(a=self)


    def __setattr__(self, key, value):
        if key == 'value':
            try:
                self.previous_value = self.value
            except:
                pass
        self.__dict__[key] = value

    def add_tab(self, id, label, content):
        self.tabs.append({'id': id, 'label': label, 'content': content})
        if not self.value:
            self.value = id

    def get_tab_by_id(self, id):
        for tab in self.tabs:
            if tab['id'] == id:
                return tab
        return None

    def set_content_div(self, tab):
        self.content_div.add(tab['content'])
        self.content_div.set_classes('relative overflow-hidden border')
        self.content_div.style = f'height: {self.content_height}px'

    def set_content_animate(self, tab):
        self.wrapper_div_classes = self.animation_speed  # Component in this will be centered

        if self.previous_value:
            self.wrapper_div = Div(classes=self.wrapper_div_classes, animation=self.animation_next, temp=True,
                                   style=f'{self.wrapper_style} z-index: 50;', a=self.content_div)
            self.wrapper_div.add(tab['content'])
            self.wrapper_div = Div(classes=self.wrapper_div_classes, animation=self.animation_prev, temp=True,
                                   style=f'{self.wrapper_style} z-index: 0;', a=self.content_div)
            self.wrapper_div.add(self.get_tab_by_id(self.previous_value)['content'])
        else:
            self.wrapper_div = Div(classes=self.wrapper_div_classes, temp=True, a=self.content_div,
                                   style=self.wrapper_style)
            self.wrapper_div.add(tab['content'])

        self.content_div.set_classes('relative overflow-hidden border')
        self.content_div.style = f'height: {self.content_height}px'


    def model_update(self):
        val = self.model[0].data[self.model[1]]
        if self.get_tab_by_id(val):
            self.value = val

    def delete(self):
        if self.delete_flag:
            for tab in self.tabs:
                tab['content'].delete()
                tab['content'] = None
        super().delete()

    @staticmethod
    async def tab_click(self, msg):
        if self.tabs.value != self.tab_id:
            previous_tab = self.tabs.value
            self.tabs.value = self.tab_id
            if hasattr(self.tabs, 'model'):
                self.tabs.model[0].data[self.tabs.model[1]] = self.tabs.value
            # Run change if it exists
            if self.tabs.has_event_function('change'):
                msg.previous_tab = previous_tab
                msg.new_tab = self.tabs.value
                msg.id = self.tabs.id
                msg.value = self.tabs.value
                msg.class_name = self.tabs.__class__.__name__
                return await self.tabs.run_event_function('change', msg)
        else:
            return True  # No need to update page

    def convert_object_to_dict(self):
        if hasattr(self, 'model'):
            self.model_update()
        self.set_classes('flex flex-col')
        self.tab_list.delete_components()
        self.content_div.components = []
        for tab in self.tabs:
            if tab['id'] != self.value:
                tab_li = Li(a=self.tab_list, classes=self.item_classes)
                li_item = A(text=tab['label'], classes=self.tab_label_classes, a=tab_li)
            else:
                tab_li = Li(a=self.tab_list, classes=self.item_classes_selected)
                li_item = A(text=tab['label'], classes=self.tab_label_classes_selected, a=tab_li)
                if self.animation and (self.value != self.last_rendered_value):
                    self.set_content_animate(tab)
                else:
                    self.set_content_div(tab)
            li_item.tab_id = tab['id']
            li_item.tabs = self
            li_item.on('click', self.tab_click)
        self.last_rendered_value = self.value
        d = super().convert_object_to_dict()

        return d


class TabsPills(Tabs):
    tab_label_classes = 'cursor-pointer inline-block border border-white rounded hover:border-gray-200 text-blue-500 hover:bg-gray-200 py-1 px-3'
    tab_label_classes_selected = 'cursor-pointer inline-block border border-blue-500 rounded py-1 px-3 bg-blue-500 text-white'
    item_classes = 'flex-shrink mr-3'
    item_classes_selected = 'flex-shrink -mb-px mr-3'


my_chart_def = """
{
        chart: {
            type: 'bar'
        },
        title: {
            text: 'Fruit Consumption'
        },
        xAxis: {
            categories: ['Apples', 'Bananas', 'Oranges']
        },
        yAxis: {
            title: {
                text: 'Fruit eaten'
            }
        },
        series: [{
            name: 'Jane',
            data: [1, 0, 4],
            animation: false
        }, {
            name: 'John',
            data: [5, 7, 3],
            animation: false
        }]
}
"""
# https://dog.ceo/api/breed/papillon/images/random
pics_french_bulldogs = ['5458', '7806', '5667', '4860']
pics_papillons = ['5037', '2556', '7606', '8241']

def tab_change(self, msg):
    print('in change', msg)

def tab_comp_test():
    wp = jp.WebPage(data={'tab': 'id2556'})

    t = Tabs(a=wp, classes='w-3/4 m-4', style='', animation=True, content_height=550)
    for chart_type in ['bar', 'column', 'line', 'spline']:
        d = jp.Div(style=Tabs.wrapper_style, delete_flag=True)
        my_chart = jp.HighCharts(a=d, classes='m-2 p-2 border', style='width: 1000px;', options=my_chart_def, use_cache=False)
        my_chart.options.chart.type = chart_type
        my_chart.options.title.text = f'Chart of Type {chart_type.capitalize()}'
        my_chart.options.subtitle.text = f'Subtitle {chart_type.capitalize()}'
        t.add_tab(f'id{chart_type}', f'{chart_type}', d)

    d_flex = Div(classes='flex', a=wp)  # Container for the two dog pictures tabs

    t = Tabs(a=d_flex, classes=' w-1/2 m-4', animation=True, content_height=550, model=[wp, 'tab'], change=tab_change)
    for pic_id in pics_papillons:
        d = jp.Div(style=Tabs.wrapper_style)
        jp.Img(src=f'https://images.dog.ceo/breeds/papillon/n02086910_{pic_id}.jpg', a=d)
        t.add_tab(f'id{pic_id}', f'Pic {pic_id}', d)

    t = TabsPills(a=d_flex, classes='w-1/2 m-4', animation=True, content_height=550, change=tab_change)
    for pic_id in pics_french_bulldogs:
        d = jp.Div(style=Tabs.wrapper_style)
        jp.Img(src=f'https://images.dog.ceo/breeds/bulldog-french/n02108915_{pic_id}.jpg', a=d)
        t.add_tab(f'id{pic_id}', f'Pic {pic_id}', d)

    input_classes = "w-1/3 m-2 bg-gray-200 border-2 border-gray-200 rounded w-64 py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-purple-500"

    in1 = jp.Input(classes=input_classes, model=[wp, 'tab'], a=wp)

    return wp


justpy(tab_comp_test)



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
tabs_html = """
<div>
<ul class="flex border-b">
  <li class="-mb-px mr-1">
    <a class="bg-white inline-block border-l border-t border-r rounded-t py-2 px-4 text-blue-700 font-semibold" href="#">Active</a>
  </li>
  <li class="mr-1">
    <a class="bg-white inline-block py-2 px-4 text-blue-500 hover:text-blue-800 font-semibold" href="#">Tab</a>
  </li>
  <li class="mr-1">
    <a class="bg-white inline-block py-2 px-4 text-blue-500 hover:text-blue-800 font-semibold" href="#">Tab</a>
  </li>
  <li class="mr-1">
    <a class="bg-white inline-block py-2 px-4 text-gray-400 font-semibold" href="#">Tab</a>
  </li>
</ul>
</div>
"""


# justpy(tab_test)
# justpy(animation_test)
# justpy(panels_tab_test)
def tab_test():
    wp = WebPage()
    tabsxx = parse_html(tabs_html, a=wp, classes='w-1/2')
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
chart_def_tt = """
{
 chart: {
        type: 'spline'
    },
    title: {
        text: ''
    },
    subtitle: {
        text: 'JustPy Tooltip Demo'
    },
    yAxis: {
        title: {
            text: 'Number of Employees'
        }
    },
    legend: {
        layout: 'vertical',
        align: 'right',
        verticalAlign: 'middle'
    },
    plotOptions: {
        series: {
            pointStart: 2010
        }
    },
    series: [{
        name: 'Installation',
        data: [43934, 52503, 57177, 69658, 97031, 119931, 137133, 154175]
    }, {
        name: 'Manufacturing',
        data: [24916, 24064, 29742, 29851, 32490, 30282, 38121, 40434]
    }, {
        name: 'Sales & Distribution',
        data: [11744, 17722, 16005, 19771, 20185, 24377, 32147, 39387]
    }, {
        name: 'Project Development',
        data: [null, null, 7988, 12169, 15112, 22452, 34400, 34227]
    }, {
        name: 'Other',
        data: [12908, 5948, 8105, 11248, 8989, 11816, 18274, 18111]
    }]
}
"""
def tool_top_spare():
    wp = WebPage()
    my_charts = []
    for i in range(3):
        my_charts.append(jp.HighCharts(classes='m-2 p-2 border', options=chart_def_tt, use_cache=False))

    my_charts[0].options.tooltip.shared = False
    my_charts[1].options.tooltip.shared = True
    my_charts[2].options.tooltip.split = True
    my_charts[0].options.title.text = 'Simple Tooltip - Formatter Example'
    my_charts[1].options.title.text = 'Shared Tooltip - Formatter Example'
    my_charts[2].options.title.text = 'Split Tooltip - Formatter Example'

    my_charts[0].on('tooltip', simple_tooltip_formatter)
    my_charts[1].on('tooltip', shared_tooltip_formatter)
    my_charts[2].on('tooltip', split_tooltip_formatter)

    t = Tabs(a=wp, classes='w-2/3 m-4', style='', animation=True, content_height=550)
    for i in range(3):
        d = jp.Div(style=Tabs.wrapper_style, delete_flag=True)
        d.add(my_charts[i])
        t.add_tab(f'idd{i}', f'Chart {i}', d)


async def simple_tooltip_formatter(self, msg):
    tooltip_html = f"""
    <div class="text-red-500">
    <div><span style="color: {msg.color}">&#x25CF;&nbsp;</span>{msg.series_name}</div>
    <div>Year: {msg.x}</div>
    <div>Number of employees: {"{:,}".format(msg.y)}</div>
    </div>
    """
    return await self.tooltip_update(tooltip_html, msg.websocket)


async def shared_tooltip_formatter(self, msg):
    tooltip_div = jp.Div(classes="text-white bg-blue-400", temp=True)
    jp.Span(text=f'Year: {msg.x}', classes='text-lg', a=tooltip_div, temp=True)
    for point in msg.points:
        point_div = jp.Div(a=tooltip_div, temp=True)
        jp.Span(text=f'&#x25CF; {point.series_name}', classes='bg-white', style=f'color: {point.color}', a=point_div, temp=True)
        jp.Span(text=f'Number of employees: {"{:,}".format(point.y)}', a=point_div, temp=True)
    return await self.tooltip_update(tooltip_div.to_html(), msg.websocket)


async def split_tooltip_formatter(self, msg):
    tooltip_array = [f'The x value is {msg.x}']
    for point in msg.points:
        point_div = jp.Div(temp=True)
        jp.Span(text='&#x25CF;', classes='bg-white', style=f'color: {point.color}', a=point_div, temp=True)
        jp.Span(text=f'{point.series_name}', a=point_div, temp=True)
        jp.Span(text=f'Year: {point.x}', a=point_div, temp=True)
        jp.Span(text=f'Number of employees: {"{:,}".format(point.y)}', a=point_div, temp=True)
        tooltip_array.append(point_div.to_html())
    return await self.tooltip_update(tooltip_array, msg.websocket)