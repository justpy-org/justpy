# Justpy Tutorial demo quasar_expansion_item1 from docs/quasar_tutorial/quasar_components.md
import justpy as jp

sample_text = """
Lorem ipsum dolor sit amet, consectetur adipisicing elit. Quidem, eius reprehenderit eos corrupti
            commodi magni quaerat ex numquam, dolorum officiis modi facere maiores architecto suscipit iste
            eveniet doloribus ullam aliquid.
"""

def quasar_expansion_item1():
    wp = jp.QuasarPage()
    d = jp.Div(classes="q-pa-md", style="max-width: 350px", a=wp)
    item_list = jp.QList(classes="rounded-borders", padding=True, bordered=True, a=d)
    for info in [("perm_identity", "Account settings"), ("signal_wifi_off", "Wifi settings"), ("drafts", "Drafts")]:
        expansion_item = jp.QExpansionItem(icon=info[0], label=info[1], a=item_list, header_class='text-purple',
                                           dense=True, dense_toggle=True, expand_separator=True)
        card= jp.QCard(a=expansion_item)
        jp.QCardSection(text=sample_text, a=card)

    return wp

# initialize the demo
from examples.basedemo import Demo
Demo("quasar_expansion_item1", quasar_expansion_item1)
