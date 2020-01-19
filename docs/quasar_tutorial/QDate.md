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

## Date and Time as QInput slots

Coming soon