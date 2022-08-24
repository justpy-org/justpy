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

def input_test():
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


def input_test():
    wp = jp.QuasarPage()
    QInputDateTime(filled=True, style='width: 600px', a=wp, classes="q-pa-md", value='')
    QInputDateTime(filled=True, style='width: 600px', a=wp, classes="q-pa-md", value='2020-03-01 12:44')
    QInputDateTime(filled=True, style='width: 600px', a=wp, classes="q-pa-md", value='2021-04-01 14:44')
    QInputDateTime(filled=True, style='width: 600px', a=wp, classes="q-pa-md", value='2022-05-01 18:44')
    return wp


jp.justpy(input_test)
```