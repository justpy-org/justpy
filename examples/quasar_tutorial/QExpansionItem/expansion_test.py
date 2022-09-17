# Justpy Tutorial demo expansion_test from docs/quasar_tutorial/QExpansionItem.md
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


def expansion_test(request):
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


# initialize the demo
from  examples.basedemo import Demo
Demo ("expansion_test",expansion_test)
