The Quasar components are presented here in alphabetical order.
You might want to try out the components in the order that is reasonable for your usecases.
QInput e.g. might be a good start.
Please see [here](https://github.com/justpy-org/justpy/blob/48c3e857461ebeeea05ac65ebe7f72ff49ae63af/justpy/quasarcomponents.py) for all available Quasar components.

# Content
- [QAjaxBar](#qajaxbar)
- [QBtnToggle](#qbtntoggle)
- [QColor](#qcolor)
- [QDate and QTime](#qdate-and-qtime)
- [QDialog](#qdialog)
- [QDrawer](#qdrawer)
- [QExpansionItem](#qexpansionitem)
- [QInput](#qinput)
- [QList](#qlist-and-qitem)
- [QOptionGroup](#qoptiongroup)
- [QRating](#qrating)
- [QSplitter](#qsplitter)
- [QTree](#qtree)

# QAjaxBar


```python
import justpy as jp

async def start_bar(self, msg):
    wp = msg.page
    await wp.ajax_bar.run_method('start()', msg.websocket)

async def stop_bar(self, msg):
    wp = msg.page
    await wp.ajax_bar.run_method('stop()', msg.websocket)


def ajax_bar_example():
    wp = jp.QuasarPage()
    d = jp.Div(classes='q-pa-md', a=wp)
    # temp=False is important because this generates an id for the element that is required for run_method to work
    wp.ajax_bar = jp.QAjaxBar(position='bottom', color='accent', size='10px', skip_hijack=True, a=d, temp=False)
    btn_start = jp.QBtn(color='primary', label='Start Bar', a=d, click=start_bar, style='margin-right: 20px')
    btn_stop = jp.QBtn(color='primary', label='Stop Bar', a=d, click=stop_bar)
    return wp

jp.justpy(ajax_bar_example)

```

# QBtnToggle

[QBtnToggle component](https://quasar.dev/vue-components/button-toggle) is similar to a radio group but with buttons.

```python
import justpy as jp

# Example from https://www.highcharts.com/docs/getting-started/your-first-chart
my_chart_def = """
{
        chart: {
            type: 'bar'
        },
        title: {
            text: 'Chart of Type Bar'
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
            data: [1, 0, 4]
        }, {
            name: 'John',
            data: [5, 7, 3]
        }]
}
"""

def button_change(self, msg):
    print(msg)
    self.chart.options.chart.type = self.value
    self.chart.options.title.text = f'Chart of Type {self.value}'

def button_toggle_test():
    wp = jp.QuasarPage()
    chart_type = jp.QBtnToggle(toggle_color='red', push=True, glossy=True, a=wp, input=button_change, value='bar', classes='q-ma-md')
    for type in ['bar', 'column', 'line', 'spline']:
        chart_type.options.append({'label': type.capitalize(), 'value': type})
    chart_type.chart = jp.HighCharts(a=wp, classes='q-ma-lg', options=my_chart_def)
    return wp


jp.justpy(button_toggle_test)
```

# QColor

The [Color Picker](https://quasar.dev/vue-components/color-picker) can be used to select colors.


```python
import justpy as jp

def color_change(self, msg):
    self.div.style = f'color: {self.value}'

def input_test2():
    wp = jp.QuasarPage(data={'color': ''})
    in1 = jp.QInput(filled=True, style='width: 400px', a=wp, model=[wp, 'color'], classes="q-pa-md", input=color_change)
    j = jp.parse_html("""
        <q-icon name="colorize" class="cursor-pointer">
                <q-popup-proxy transition-show="scale" transition-hide="scale">
                  <q-color name="color_input"/>
                </q-popup-proxy>
              </q-icon>
        """)
    in1.add_scoped_slot('append', j)
    color_input = j.name_dict['color_input']
    color_input.model = [wp, 'color']
    color_input.on('change', color_change)
    in1.div = jp.Div(text='Change this text color using QInput above', classes="q-pa-md text-h4", a=wp)
    color_input.div = in1.div
    return wp


jp.justpy(input_test2)
```

# QDate and QTime

The [Date Picker](https://quasar.dev/vue-components/date) and [Time Picker](https://quasar.dev/vue-components/time) components can be used to input date and time.

```python
import justpy as jp

html_string = """
<div class="q-pa-md">
    <div class="q-gutter-sm">
      <q-badge color="teal" name="badge" classes="text-h3"/>
      <q-badge color="purple" text-color="white" class="q-ma-md">
        Mask: YYYY-MM-DD HH:mm
      </q-badge>
    </div>

    <div class="q-gutter-md row items-start">
      <q-date  mask="YYYY-MM-DD HH:mm" color="purple" name="date"/>
      <q-time  mask="YYYY-MM-DD HH:mm" color="purple" name="time"/>
    </div>
  </div>
"""


def date_time_test():
    wp = jp.QuasarPage(data={'date': '2020-01-01 07:00'})
    d = jp.parse_html(html_string, a=wp)
    for c in ['badge', 'date', 'time']:
        d.name_dict[c].model = [wp, 'date']
    return wp

jp.justpy(date_time_test)

```

## Using Function Style Property

In order to use a function-style property with QDate, the following is necessary:
```python
    qd = jp.QDate()
    qd.events_date = "(date) => {return date[9] %3 === 0}"
    qd.evaluate_prop.append('events')
```

Note that the mapping of property names is a little bit tricky. In Quasar, the property is named QDate.events. Due to the fact that 'events' is a reserved property in JustPy, the property is called events_date in the Python domain. However the evaluate_prop list is only analyzed in the JS domain, where the property name is 'events'.

## Date and Time as QInput slots

```python
import justpy as jp

# https://quasar.dev/vue-components/date#With-QInput

def input_test3():
    wp = jp.QuasarPage(data={'date': '2019-02-01 12:44'})
    in1 = jp.QInput(filled=True, style='width: 400px', a=wp, model=[wp, 'date'], classes="q-pa-md")
    date_slot = jp.parse_html("""
    <q-icon name="event" class="cursor-pointer">
          <q-popup-proxy transition-show="rotate" transition-hide="rotate">
            <q-date mask="YYYY-MM-DD HH:mm" name="date"/>
          </q-popup-proxy>
        </q-icon>
    """)
    time_slot = jp.parse_html("""
        <q-icon name="access_time" class="cursor-pointer">
          <q-popup-proxy transition-show="scale" transition-hide="scale">
            <q-time mask="YYYY-MM-DD HH:mm" format24h name="time"/>
          </q-popup-proxy>
        </q-icon>
        """)
    date_slot.name_dict['date'].model = [wp, 'date']
    time_slot.name_dict['time'].model = [wp, 'date']
    in1.prepend_slot = date_slot
    in1.append_slot = time_slot
    return wp
jp.justpy(input_test3)

```

Or you can arrive at the same result by creating a reusable component (class):

### Date and Time as QInput slots as class component
```python
import justpy as jp

# https://quasar.dev/vue-components/date#With-QInput

class QInputDateTime(jp.QInput):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mask = '####-##-## ##:##'
        date_slot = jp.QIcon(name='event', classes='cursor-pointer')
        c2 = jp.QPopupProxy(transition_show='scale', transition_hide='scale', a=date_slot)
        self.date = jp.QDate(mask='YYYY-MM-DD HH:mm', name='date', a=c2)

        time_slot = jp.QIcon(name='access_time', classes='cursor-pointer')
        c2 = jp.QPopupProxy(transition_show='scale', transition_hide='scale', a=time_slot)
        self.time = jp.QTime(mask='YYYY-MM-DD HH:mm', format24h=True, name='time', a=c2)

        self.date.parent = self
        self.time.parent = self
        self.date.value = self.value
        self.time.value = self.value
        self.prepend_slot = date_slot
        self.append_slot = time_slot
        self.date.on('input', self.date_time_change)
        self.time.on('input', self.date_time_change)
        self.on('input', self.input_change)

    @staticmethod
    def date_time_change(self, msg):
        print(self.value)
        self.parent.value = self.value
        self.parent.date.value = self.value
        self.parent.time.value = self.value

    @staticmethod
    def input_change(self, msg):
        self.date.value = self.value
        self.time.value = self.value


def input_test4():
    wp = jp.QuasarPage()
    QInputDateTime(filled=True, style='width: 600px', a=wp, classes="q-pa-md", value='')
    QInputDateTime(filled=True, style='width: 600px', a=wp, classes="q-pa-md", value='2020-03-01 12:44')
    QInputDateTime(filled=True, style='width: 600px', a=wp, classes="q-pa-md", value='2021-04-01 14:44')
    QInputDateTime(filled=True, style='width: 600px', a=wp, classes="q-pa-md", value='2022-05-01 18:44')
    return wp


jp.justpy(input_test4)
```

# QDialog

Quasar provides a versatile [QDialog component](https://quasar.dev/vue-components/dialog). Checkout the many options in the Quasar documentation.

In the program below, two examples are implemented.

When a Dialog is closed by the user, it generates an input event.

The `v-close-popup` directive closes the dialog automatically when the associated button is clicked. Use `v_close_popup` in JustPy commands.

```python
import justpy as jp

alert_dialog_html = """
<div class="q-pa-md q-gutter-sm">
    <q-btn label="Alert" color="primary" name="alert_button" />
    <q-dialog name="alert_dialog" persistent>
      <q-card>
        <q-card-section>
          <div class="text-h6">Alert</div>
        </q-card-section>

        <q-card-section>
          Lorem ipsum dolor sit amet consectetur adipisicing elit. Rerum repellendus sit voluptate voluptas eveniet porro. Rerum blanditiis perferendis totam, ea at omnis vel numquam exercitationem aut, natus minima, porro labore.
        </q-card-section>

        <q-card-actions align="right">
          <q-btn flat label="OK" color="primary" v-close-popup />
        </q-card-actions>
      </q-card>
    </q-dialog>
</div>
"""

seamless_dialog_html = """
<div class="q-pa-md q-gutter-sm">
    <q-btn label="Open seamless Dialog" color="primary" name="seamless_button" />

    <q-dialog seamless position="bottom" name="seamless_dialog">
      <q-card style="width: 350px">
        <q-linear-progress :value="0.6" color="pink" />

        <q-card-section class="row items-center no-wrap">
          <div>
            <div class="text-weight-bold">The Walker</div>
            <div class="text-grey">Fitz & The Tantrums</div>
          </div>

          <q-space />

          <q-btn flat round icon="play_arrow" />
          <q-btn flat round icon="pause" />
          <q-btn flat round icon="close" v-close-popup />
        </q-card-section>
      </q-card>
    </q-dialog>
  </div>
"""


def open_dialog(self, msg):
    self.dialog.value = True

def dialog_test():
    wp = jp.QuasarPage()

    c = jp.parse_html(alert_dialog_html, a=wp)
    c.name_dict["alert_button"].dialog = c.name_dict["alert_dialog"]
    c.name_dict["alert_button"].on('click', open_dialog)

    c = jp.parse_html(seamless_dialog_html, a=wp)
    c.name_dict["seamless_button"].dialog = c.name_dict["seamless_dialog"]
    c.name_dict["seamless_button"].on('click', open_dialog)

    return wp

jp.justpy(dialog_test)

```

# QDrawer

Quasars [QDrawer](https://quasar.dev/layout/drawer) is the sidebar part of QLayout which allows you to configure your views as a 3x3 matrix, containing optional left-side and/or right-side Drawers.
The example below shows a minimal implementation of a collapsible side bar in JustPy.

```python
"""
Quasar Drawer example see https://github.com/justpy-org/justpy/issues/589
"""
import justpy as jp


def toggle_visible_drawer(self, msg):
    self.drawer.value = not self.drawer.value


def qdrawer_page():
    wp = jp.QuasarPage()

    btn_drawer = jp.QBtn(
        flat=True,
        round=True,
        dense=True,
        icon="menu",
        a=wp,
        click=toggle_visible_drawer,
    )

    wp_layout = jp.QLayout(a=wp)
    PageContainer = jp.QPageContainer(a=wp_layout)
    pageText = jp.Div(a=PageContainer, text="page container")

    drawer = jp.QDrawer(
        width=200,
        breakpoint=500,
        bordered=True,
        a=wp_layout,
    )
    btn_drawer.drawer = drawer
    ScrollArea = jp.QScrollArea(classes="fit", a=drawer)
    c2 = jp.Div(a=ScrollArea, text="scroll area left")

    return wp

jp.justpy(qdrawer_page)
```

# QExpansionItem
See also [quasar vue expansion-item](https://quasar.dev/vue-components/expansion-item)
The QExpansionItem component allows the hiding of content that is not immediately relevant to the user.
Think of them as accordion elements that expand when clicked on. It’s also known as a collapsible.

They are basically QItem components wrapped with additional functionality. So they can be included in QLists and inherit QItem component properties.

## QExpansionItem Example 1

Three expansion items are defined in a loop. All three are added to a QList instance. Each expansion item includes a QCard with a QCardSection with text.

```python
import justpy as jp

sample_text = """
Lorem ipsum dolor sit amet, consectetur adipisicing elit. Quidem, eius reprehenderit eos corrupti
            commodi magni quaerat ex numquam, dolorum officiis modi facere maiores architecto suscipit iste
            eveniet doloribus ullam aliquid.
"""

def quasar_expansion_item1():
    wp = jp.QuasarPage()
    d = jp.Div(classes="q-pa-md", style="max-width: 350px", a=wp)
    item_list = jp.QList(classes="rounded-borders", padding=True, bordered=True, a=d)
    for info in [("perm_identity", "Account settings"), ("signal_wifi_off", "Wifi settings"), ("drafts", "Drafts")]:
        expansion_item = jp.QExpansionItem(icon=info[0], label=info[1], a=item_list, header_class='text-purple',
                                           dense=True, dense_toggle=True, expand_separator=True)
        card= jp.QCard(a=expansion_item)
        jp.QCardSection(text=sample_text, a=card)

    return wp

jp.justpy(quasar_expansion_item1)
```

## QExpansionItem Example 2

In this example we define a custom component based on QExpansionItem. This component adds an image from the site [Lorem Picsum](https://picsum.photos/) to the expansion item and in addition formats the expansion item.

```python
import justpy as jp

class My_expansion(jp.QExpansionItem):

    image_num = 10      # Start from image 10, previous are boring to my taste

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        outer_div = jp.Div(classes="q-pa-md", a=self)
        jp.QImg(src=f'https://picsum.photos/400/300/?image={My_expansion.image_num}', a=outer_div)
        self.icon = "photo"
        self.label = f'Image {My_expansion.image_num}'
        self.value = True
        self.expand_separator = True
        self.header_class = "bg-teal text-white text-overline"
        My_expansion.image_num += 1


def quasar_expansion_item2(request):
    wp = jp.QuasarPage(dark=False)
    d = jp.Div(classes="q-pa-md ", style="max-width: 500px", a=wp)
    jp.Link(href='https://quasar.dev/vue-components/expansion-item', text='Quasar Expansion Item Example', target='_blank',
            classes="text-h5 q-mb-md", a=d, style='display: block;')
    add_btn = jp.QBtn(label='Add Image', classes="q-mb-md", color='primary', a=d)
    close_btn = jp.QBtn(label='Close All', classes="q-ml-md q-mb-md", color='negative', a=d)
    open_btn = jp.QBtn(label='Open All', classes="q-ml-md q-mb-md", color='positive', a=d)
    l = jp.QList(bordered=True, a=d)
    wp.list = l
    l.add_component(My_expansion(), 0)

    def add_pic(self, msg):
        msg.page.list.add_component(My_expansion(), 0)
    add_btn.on('click', add_pic)

    def close_pics(self, msg):
        for c in msg.page.list.components:
            c.value = False
    close_btn.on('click', close_pics)

    def open_pics(self, msg):
        for c in msg.page.list.components:
            c.value = True
    open_btn.on('click', open_pics)

    return wp


jp.justpy(quasar_expansion_item2)
```

# QInput

## Introduction

The [Quasar QInput component](https://quasar.dev/vue-components/input) is very versatile and comes with many features and options. Almost all are supported by JustPy.

QInput like Input creates an input event when its value changes.

The program below puts on the page several QInput elements with different features. All are connected using the the same `model` attribute.

### Several QInput elements
```python
import justpy as jp

def input_test5(request):
    wp = jp.QuasarPage(data={'text': ''})
    c1 = jp.Div(classes='q-pa-md', a=wp)
    c2 = jp.Div(classes='q-gutter-md', style='max-width: 300px', a=c1)
    c3 = jp.QInput(label='Standard', a=c2, model=[wp, 'text'])
    c4 = jp.QInput(filled=True, label='Filled', a=c2, model=[wp, 'text'])
    c5 = jp.QInput(outlined=True, label='Outlined', a=c2, model=[wp, 'text'])
    c6 = jp.QInput(standout=True, label='Standout', a=c2, model=[wp, 'text'])
    c7 = jp.QInput(standout='bg-teal text-white', label='Custom standout', a=c2, model=[wp, 'text'])
    c8 = jp.QInput(borderless=True, label='Borderless', a=c2, model=[wp, 'text'])
    c9 = jp.QInput(rounded=True, filled=True, label='Rounded filled', a=c2, model=[wp, 'text'])
    c10 = jp.QInput(rounded=True, outlined=True, label='Rounded outlined', a=c2, model=[wp, 'text'])
    c11 = jp.QInput(rounded=True, standout=True, label='Rounded standout', a=c2, model=[wp, 'text'])
    c12 = jp.QInput(square=True, filled=True, label='Square filled', hint='This is a hint', a=c2, model=[wp, 'text'])
    c13 = jp.QInput(square=True, outlined=True, label='Square outlined', a=c2, model=[wp, 'text'])
    c14 = jp.QInput(square=True, standout=True, label='Square standout', a=c2, model=[wp, 'text'])
    return wp

jp.justpy(input_test5)
```

## Using Slots

```python
import justpy as jp

def input_test6(request):
    wp = jp.QuasarPage()
    c1 = jp.Div(classes='q-pa-md', a=wp)
    c2 = jp.Div(classes='q-gutter-md', style='max-width: 300px', a=c1)
    icon1 = jp.QIcon(name='event', color='blue')
    icon2 = jp.QIcon(name='place', color='red')
    for slot in ['append', 'prepend', 'before']:
        in1 = jp.QInput(label=slot, filled=True, hint=f'Icon is in slot "{slot}" and "after"', a=c2, after_slot=icon2)
        #in1.after_slot = icon2    # Alternative to keyword method used in line above
        setattr(in1, slot + '_slot', icon1)
    return wp

jp.justpy(input_test6)

```

## Password Visibility Toggle Example

```python
import justpy as jp

def input_test7(request):
    wp = jp.QuasarPage()
    c1 = jp.Div(classes='q-pa-md', a=wp)
    c2 = jp.Div(classes='q-gutter-md', style='max-width: 300px', a=c1)

    password_input = jp.QInput(filled=True,  type='password', a=c2, hint="Password with toggle")
    visibility_icon = jp.QIcon(name='visibility_off', classes='cursor-pointer')
    visibility_icon.password_input = password_input

    password_input.append_slot = visibility_icon

    def toggle_password(self, msg):
        if self.name == 'visibility_off':
            self.name = 'visibility'
            self.password_input.type='text'
        else:
            self.name = 'visibility_off'
            self.password_input.type = 'password'

    visibility_icon.on('click', toggle_password)

    return wp

jp.justpy(input_test7)
```

Or better yet, as a reusable component

### PasswordWithToggle as a reusable component

```python
import justpy as jp

class PasswordWithToggle(jp.QInput):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'password'
        visibility_icon = jp.QIcon(name='visibility_off', classes='cursor-pointer')
        visibility_icon.password_input = self
        self.append_slot = visibility_icon
        visibility_icon.on('click', self.toggle_password)

    @staticmethod
    def toggle_password(self, msg):
        if self.name == 'visibility_off':
            self.name = 'visibility'
            self.password_input.type = 'text'
        else:
            self.name = 'visibility_off'
            self.password_input.type = 'password'


def input_test8(request):
    wp = jp.QuasarPage(data={'text': ''})
    c1 = jp.Div(classes='q-pa-md', a=wp)
    c2 = jp.Div(classes='q-gutter-md', style='max-width: 300px', a=c1)
    for i in range(1,6):
        PasswordWithToggle(filled=True,  type='password', a=c2, hint=f'Password with toggle #{i}')
    return wp

jp.justpy(input_test8)

```

## Input Masks


```python
import justpy as jp

def input_test9(request):
    wp = jp.QuasarPage(data={'text': ''})
    c1 = jp.Div(classes='q-pa-md', a=wp)
    c2 = jp.Div(classes='q-gutter-md', style='max-width: 300px', a=c1)
    jp.QInput(filled=True, label='Phone', mask='(###) ### - ####', hint="Mask: (###) ### - ####", a=c2)
    return wp

jp.justpy(input_test9)

```

## Input Validation

In the example below, a regular expression is used to validate a field as the user is typing (you of course may use instead any one of the available data validation packages). It uses QInput's `error` and `error_message` props.

```python
import justpy as jp
import re

email_regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

def input_change(self, msg):
    print(self.value)
    if re.match(email_regex,self.value):
        self.error = False
    else:
        self.error = True
        self.error_message = 'Enter valid email address'
        self.bottom_slots = True


def input_test10():
    wp = jp.QuasarPage()
    in1 = jp.QInput(label='Enter email', style='width: 150px; margin: 20px', a=wp, input=input_change)
    return wp


jp.justpy(input_test10)
```

You can also use QInput's internal validation prop `rules`. The prop needs to be a list that contains a string that represents JavaScript functions. See the [examples](https://quasar.dev/vue-components/input#Internal-validation) in the Quasar documentation

### QInput internal validation with rules
```python
import justpy as jp

def input_test11():
    wp = jp.QuasarPage()
    in1 = jp.QInput(label='Enter email', style='width: 150px; margin: 20px', a=wp, lazy_rules=False)
    in1.rules = ["val => val.length <= 3 || 'Please use maximum 3 characters'"]
    return wp

jp.justpy(input_test11)
```

## QInputChange and QInputBlur - Disabling the Input Event

In some cases the debounce feature may not be sufficient to provide a good user experience. This may happen when users type in bursts. Setting debounce to 1000 almost always solves these problems but there is another option if the large debounce is causing other issues. You can disable the input event altogether and capture the value of the QInput when it loses focus.

You can control this yourself by setting the `disable_input_event` attribute to `True` or use the predefined QInputChange and QInputBlur components. QInputBlur will only update the value of the field when the component loses focus. QInputChange will update the value when the change event is fired. Both are very similar except that change will also fire when the Enter key is pressed and focus remains on the component.

The regular QInput component generates an event each time a character is typed into the field. In some case this is not necessary and may put unwanted burden on the server. If you are not implementing a look ahead or validating the field on the server as the user is typing, it is preferable to use QInputChange and QInputBlur instead of QInput.
[QInputChange and QInputBlur live demo]({{demo_url}}/input_demo_quasar1)


```python
import justpy as jp

def my_blur(self, msg):
    """
    event handler for loosing the focus
    """
    self.div.text = self.value

def input_demo_quasar1(request):
    """
    show how the blue event works
    """
    wp = jp.QuasarPage()
    c1 = jp.Div(classes='q-pa-md', a=wp)
    c2 = jp.Div(classes='q-gutter-md', style='max-width: 300px', a=c1)
    in1 = jp.QInputBlur(a=c2,placeholder='Please type here', label='QInputBlur')
    in1.div = jp.Div(text='What you type will show up here only when Input element loses focus',
                      classes='text-h6', a=c2)
    in1.on('blur', my_blur)
    return wp

jp.justpy(input_demo_quasar1)
```

## Yahoo Stock Charts Example

!!! warning
    You need to install the [pandas-datareader](https://pandas-datareader.readthedocs.io/en/latest/) package to run this example

In the example below we define a component which simplifies entering dates. Click on the calendar icon of the QInput elements to have the a QDate element pop-up.

Using a ticker and the dates provided by the user, data is retrieved from Yahoo and a chart is displayed.

This is also an example of how you would change a Quasar button to the loading state while data is being retrieved.

```python
import justpy as jp
from pandas_datareader import data as pdr
import datetime
import functools

epoch = datetime.datetime(1970, 1, 1)
grouping_units = [['week', [1]], ['month', [1, 2, 3, 4, 6]]]

chart_dict = {
    'rangeSelector': {'selected': 1},
    'yAxis': [
        {'labels': {'align': 'right', 'x': -3}, 'title': {'text': 'OHLC'}, 'height': '60%', 'lineWidth': 2, 'resize': {'enabled': True}},
        {'labels': {'align': 'right', 'x': -3}, 'title': {'text': 'Volume'}, 'top': '65%', 'height': '35%', 'offset': 0, 'lineWidth': 2}
    ],
    'tooltip': {'split': True},
    'series': [
        {'type': 'candlestick', 'tooltip': {'valueDecimals': 2}, 'dataGrouping': {'units': grouping_units}},
        {'type': 'column', 'name': 'Volume', 'yAxis': 1, 'dataGrouping': {'units': grouping_units}}
    ]
}


class QInputDate(jp.QInput):
    """
    Custom Quasar date input field widget
    """

    def __init__(self, **kwargs):
        """
        constructor
        """
        super().__init__(**kwargs)

        date_slot = jp.QIcon(name='event', classes='cursor-pointer')
        c2 = jp.QPopupProxy(transition_show='scale', transition_hide='scale', a=date_slot)
        self.date = jp.QDate(mask='YYYY-MM-DD', name='date', a=c2)

        self.date.parent = self
        self.date.value = self.value
        self.append_slot = date_slot
        self.date.on('input', self.date_time_change)
        self.on('input', self.input_change)
        self.proxy = c2

    @staticmethod
    async def date_time_change(self, msg):
        """
        handle datetime field change
        """
        self.parent.value = self.value
        self.parent.date.value = self.value
        await self.parent.proxy.run_method('hide()', msg.websocket)

    @staticmethod
    def input_change(self, msg):
        """
        handle input field value changes
        """
        self.date.value = self.value


def convert_date(date_string):
    """
    convert given date string to datetime object
    """
    date = datetime.datetime.strptime(str(date_string), '%Y-%m-%d')
    return (date - epoch).total_seconds()*1000


async def get_chart(self, msg):
    """
    handle get_chart button click by retrieving the data from yahoo and displaying it as chart
    """
    self.loading = True
    await msg.page.update()
    self.loading = False
    data_reader = functools.partial(pdr.DataReader, data_source='yahoo', start=self.start_date.value, end=self.end_date.value)
    error_msg = ""
    data = None
    try:
        data = await jp.JustPy.loop.run_in_executor(None, data_reader, self.ticker.value)
        if data is None:
            error_msg = f'No data available for "{self.ticker.value}"'
    except KeyError as e:
            error_msg = f"{self.ticker.value}: Invalid input ({e})"
    except Exception as e:
        error_msg = e
    if data is not None:
        data['Date'] = data.index.astype(str)
        chart = jp.HighStock(a=msg.page, classes='q-ma-md', options=chart_dict, style='height: 600px')
        o = chart.options
        ticker = self.ticker.value
        o.title.text = f'{ticker} Historical Prices'
        x = list(data['Date'].map(convert_date))
        o.series[0].data = list(zip(x, data['Open'], data['High'], data['Low'], data['Close']))
        o.series[0].name = ticker
        o.series[1].data = list(zip(x, data['Volume']))
    self.error_msg.text = error_msg


async def stock_test(request):
    """
    Setup stock test webpage

    Returns:
        stock test webpage
    """
    wp = jp.QuasarPage(highcharts_theme='grid')
    d = jp.Div(classes="q-ma-md q-gutter-md row", a=wp)
    ticker = jp.QInput(label='Ticker', a=d, value='MSFT')
    start_date = QInputDate(a=d, label='Start Date', standout=True, value='2007-01-01')
    end_date = QInputDate(a=d, label='End Date', standout=True, value='2019-12-31')
    b = jp.QBtn(label='Get Chart', a=d, start_date=start_date, end_date=end_date, ticker=ticker, click=get_chart, loading=False)
    b.error_msg = jp.Div(a=wp)
    return wp



jp.justpy(stock_test)

```

# QList and QItem

Use the [QList component](https://quasar.dev/vue-components/option-group)  to group items in a list.

```python
import justpy as jp

def check_box_clicked(self, msg):
    wp = msg.page

    def my_filter(var):
        for letter in self.value:
            if var.startswith(letter):
                return True
        return False

    filtered_list = list(filter(my_filter, wp.list_item_text))

    for c in wp.q_list.components:
        if c.components[0].text not in filtered_list:
            c.show = False
        else:
            c.show = True


def reactive_list_test():
    wp = jp.QuasarPage()
    d = jp.Div(classes="q-pa-md", style="max-width: 400px", a=wp)
    wp.list_item_text = ['apple', 'ad', 'aardvark', 'again', 'bean', 'bath', 'beauty', 'can', 'corner', 'capital']
    wp.q_list = jp.QList(dense=True, bordered=True, padding=True, classes="rounded-borders", a=d)
    for word in wp.list_item_text:
        q_item = jp.QItem(clickable=True, v_ripple=True, a=wp.q_list)
        jp.QItemSection(text=word, a=q_item)

    option_group = jp.QOptionGroup(type='checkbox', color='green', a=d, input=check_box_clicked, value=['a', 'b', 'c'],
                                   inline=True, classes='q-ma-lg',
                    options=[{'label': 'A words', 'value': 'a'}, {'label': 'B words', 'value': 'b'}, {'label': 'C words', 'value': 'c'}])

    return wp

jp.justpy(reactive_list_test)

```

# QOptionGroup

Use the [QOptionGroup component](https://quasar.dev/vue-components/option-group)  to group radio buttons, checkboxes or toggles.

!!! warning "Use instead of QRadio always."  

In the example below, the type of the chart is based on the radio button selection.

```python
import justpy as jp

# Example from https://www.highcharts.com/docs/getting-started/your-first-chart
my_chart_def = """
{
        chart: {
            type: 'bar'
        },
        title: {
            text: 'Chart of Type Bar'
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
            data: [1, 0, 4]
        }, {
            name: 'John',
            data: [5, 7, 3]
        }]
}
"""

def radio_change(self, msg):
    print(msg)
    self.chart.options.chart.type = self.value

def option_group_test():
    wp = jp.QuasarPage()
    chart_type = jp.QOptionGroup(color='red', a=wp, inline=True, input=radio_change, value='bar')
    for type in ['bar', 'column', 'line', 'spline']:
        chart_type.options.append({'label': type.capitalize(), 'value': type})
    chart_type.chart = jp.HighCharts(a=wp, classes='q-ma-lg', options=my_chart_def)
    return wp


jp.justpy(option_group_test)
```


# QRating

[Quasar Rating](https://quasar.dev/vue-components/rating) is a Component which allows users to rate items.

It generates an input event each time it is clicked with the value of the input being the rating.

```python
import justpy as jp

def quasar_rating_test1():
    wp = jp.QuasarPage(data={'rating': 2})
    d = jp.Div(classes='q-pa-md', a=wp)
    rating_div = jp.Div(classes='q-gutter-y-md column', a=d)
    jp.QRating(size='1.5em', icon='thumb_up', a=rating_div, model=[wp, 'rating'])
    jp.QRating(size='2em', icon='favorite_border',color='red-7', a=rating_div, model=[wp, 'rating'])
    jp.QRating(size='2.5em', icon='create',color='purple-4', a=rating_div, model=[wp, 'rating'])
    jp.QRating(size='3em', icon='pets',color='brown-5', a=rating_div, model=[wp, 'rating'])
    jp.QRating(size='4.5em', icon='star_border',color='green-5', a=rating_div, model=[wp, 'rating'])
    jp.QRating(size='5em', icon='star_border',icon_selected='star',color='grey', a=rating_div, model=[wp, 'rating'],
               color_selected=['light-green-3', 'light-green-6', 'green', 'green-9', 'green-10'])
    jp.QRating(size='5em', icon='star_border',icon_selected='star',color='green-5', a=rating_div, model=[wp, 'rating'])
    jp.QRating(size='3.5em', max=4,color='red-5', a=rating_div, model=[wp, 'rating'],
               icon=['sentiment_very_dissatisfied', 'sentiment_dissatisfied', 'sentiment_satisfied', 'sentiment_very_satisfied'])
    return wp

jp.justpy(quasar_rating_test1)

```

## QRating With tooltips

```python
import justpy as jp

def quasar_rating_test2():
    wp = jp.QuasarPage()
    wp.tailwind = True
    num_stars = 3
    r = jp.QRating(size='2em', max=num_stars, color='primary', classes='m-2 p-2', a=wp, value=2, debounce=0)
    for i in range(1,num_stars + 1,1):
        t = jp.QTooltip(text=f'{i} rating')
        r.add_scoped_slot(f'tip-{i}', t)
    return wp


jp.justpy(quasar_rating_test2)

```

# QSplitter

The [QSplitter component](https://quasar.dev/vue-components/splitter) allows containers to be split vertically and/or horizontally through a draggable separator bar.

This component has three scoped slots or slots for short: `['before_slot', 'after_slot', 'separator_slot']`

QSplitter generates an input event when the the user changes the panes.

In the example below change the the panes and see the value of the splitter refelected in the chip at the bottom of the page and in the avatar that was put in the `separator_slot`.


```python
import justpy as jp

lorem = 'Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quis praesentium cumque magnam odio iure quidem, quod illum numquam possimus obcaecati commodi minima assumenda consectetur culpa fuga nulla ullam. In, libero.'

def quasar_splitter_test():
    wp = jp.QuasarPage()

    before = jp.Div(classes='q-pa-md')
    jp.Div(text='Before', classes='text-h4 q-mb-md', a=before)
    for i in range(20):
        jp.Div(text=f'{i}. {lorem}', a=before, classes='q-my-md')

    after = jp.Div(classes='q-pa-md')
    jp.Div(text='After', classes='text-h4 q-mb-md', a=after)
    for i in range(20):
        jp.Div(text=f'{i}. {lorem}', a=after, classes='q-my-md')

    s = jp.QSplitter(style='height: 400px', a=wp, classes='q-ma-lg')
    s.separator_class='bg-orange'
    s.separator_style='width: 3px'
    s.before_slot = before
    s.after_slot = after

    chip = jp.QChip(a=wp, classes='q-ma-lg')
    value_avatar = jp.QAvatar(text='50', color='red', text_color='white', a=chip)
    jp.Span(text='Splitter value', a=chip)

    s.value_avatar = value_avatar

    def splitter_input(self, msg):
        self.value_avatar.text = int(self.value)

    s.on('input', splitter_input)
    s.separator_slot = value_avatar

    return wp

jp.justpy(quasar_splitter_test)

```

# QTree

Quasars [Qtree](https://quasar.dev/vue-components/tree) component allows displaying hierarchical data in a tree structure.

```python
import justpy as jp

async def expand_tree(self, msg):
    return await self.tree.run_method('expandAll()', msg.websocket)

async def collapse_tree(self, msg):
    return await self.tree.run_method('collapseAll()', msg.websocket)


def quasar_tree_test():
    wp = jp.QuasarPage()
    d = jp.Div(classes="q-pa-md q-gutter-sm", a=wp)
    node_string = """
    [
        {
          label: 'Satisfied customers (with avatar)',
          avatar: 'https://cdn.quasar.dev/img/boy-avatar.png',
          children: [
            {
              label: 'Good food (with icon)',
              icon: 'restaurant_menu',
              children: [
                { label: 'Quality ingredients', icon: 'favorite' },
                { label: 'Good recipe' }
              ]
            },
            {
              label: 'Good service (disabled node with icon)',
              icon: 'room_service',
              disabled: true,
              children: [
                { label: 'Prompt attention' },
                { label: 'Professional waiter' }
              ]
            },
            {
              label: 'Pleasant surroundings (with icon)',
              icon: 'photo',
              children: [
                {
                  label: 'Happy atmosphere (with image)',
                  img: 'https://cdn.quasar.dev/img/logo_calendar_128px.png'
                },
                { label: 'Good table presentation' },
                { label: 'Pleasing decor' }
              ]
            }
          ]
        }
      ]
    """

    b1 = jp.QBtn(label='Expand', a=d, click=expand_tree)
    b2 = jp.QBtn(label='Collapse', a=d, click=collapse_tree)

    tree = jp.QTree(a=d, node_key='label', nodes=node_string, tick_strategy="leaf", no_connectors=False, default_expand_all=True)
    d1 = jp.Div(text='', a=d)

    def my_updated(self, msg):
        print('in my updated')
        d1.text = str(msg.value)
    tree.on('update:ticked', my_updated)

    b1.tree = tree
    b2.tree = tree
    return wp

jp.justpy(quasar_tree_test)
```
