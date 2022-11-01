# Justpy Tutorial demo input_test3 from docs/quasar_tutorial/quasar_components.md
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
# initialize the demo
from examples.basedemo import Demo
Demo("input_test3", input_test3)
