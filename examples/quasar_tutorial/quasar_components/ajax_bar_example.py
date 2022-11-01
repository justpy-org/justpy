# Justpy Tutorial demo ajax_bar_example from docs/quasar_tutorial/quasar_components.md
import justpy as jp

async def start_bar(self, msg):
    wp = msg.page
    await wp.ajax_bar.run_method('start()', msg.websocket)

async def stop_bar(self, msg):
    wp = msg.page
    await wp.ajax_bar.run_method('stop()', msg.websocket)


def ajax_bar_example():
    wp = jp.QuasarPage()
    d = jp.Div(classes='q-pa-md', a=wp)
    # temp=False is important because this generates an id for the element that is required for run_method to work
    wp.ajax_bar = jp.QAjaxBar(position='bottom', color='accent', size='10px', skip_hijack=True, a=d, temp=False)
    btn_start = jp.QBtn(color='primary', label='Start Bar', a=d, click=start_bar, style='margin-right: 20px')
    btn_stop = jp.QBtn(color='primary', label='Stop Bar', a=d, click=stop_bar)
    return wp

# initialize the demo
from examples.basedemo import Demo
Demo("ajax_bar_example", ajax_bar_example)
