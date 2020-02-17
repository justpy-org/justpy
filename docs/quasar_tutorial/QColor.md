# QColor

The [Color Picker](https://quasar.dev/vue-components/color-picker) can be used to select colors.


```python
import justpy as jp

def color_change(self, msg):
    self.div.style = f'color: {self.value}'

def input_test():
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


jp.justpy(input_test)
```