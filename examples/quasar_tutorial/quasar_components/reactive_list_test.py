# Justpy Tutorial demo reactive_list_test from docs/quasar_tutorial/quasar_components.md
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

# initialize the demo
from examples.basedemo import Demo
Demo("reactive_list_test", reactive_list_test)
