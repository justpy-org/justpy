The Quasar components are presented here in alphabetical order.
You might want to try out the components in the order that is reasonable for your usecases.

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

```

Or you can arrive at the same result by creating a reusable component:

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