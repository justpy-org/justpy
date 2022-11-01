# Justpy Tutorial demo input_test4 from docs/quasar_tutorial/quasar_components.md
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


# initialize the demo
from examples.basedemo import Demo
Demo("input_test4", input_test4)
