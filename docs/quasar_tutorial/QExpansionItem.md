# QExpansionItem Examples


## Example 1

Three expansion items are defined in a loop. All three are added to a QList instance. Each expansion item includes a QCard with a QCardSection with text. 
 
```python
import justpy as jp

sample_text = """
Lorem ipsum dolor sit amet, consectetur adipisicing elit. Quidem, eius reprehenderit eos corrupti
            commodi magni quaerat ex numquam, dolorum officiis modi facere maiores architecto suscipit iste
            eveniet doloribus ullam aliquid.
"""

def quasar_example():
    wp = jp.QuasarPage()
    d = jp.Div(classes="q-pa-md", style="max-width: 350px", a=wp)
    item_list = jp.QList(classes="rounded-borders", padding=True, bordered=True, a=d)
    for info in [("perm_identity", "Account settings"), ("signal_wifi_off", "Wifi settings"), ("drafts", "Drafts")]:
        expansion_item = jp.QExpansionItem(icon=info[0], label=info[1], a=item_list, header_class='text-purple',
                                           dense=True, dense_toggle=True, expand_separator=True)
        card= jp.QCard(a=expansion_item)
        jp.QCardSection(text=sample_text, a=card)

    return wp

jp.justpy(quasar_example)
```

## Example 2

In this example we define a custom component base on QExpansionItem. This component adds an image from the site [Lorem Picsum](https://picsum.photos/) to the expansion item and in addition formats the expansion item.

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


jp.justpy(expansion_test)
```