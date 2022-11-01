# Justpy Tutorial demo quasar_splitter_test from docs/quasar_tutorial/quasar_components.md
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

# initialize the demo
from examples.basedemo import Demo
Demo("quasar_splitter_test", quasar_splitter_test)
