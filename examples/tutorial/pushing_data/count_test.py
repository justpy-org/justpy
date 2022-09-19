# Justpy Tutorial demo count_test from docs/tutorial/pushing_data.md
import justpy as jp
import asyncio

button_classes = 'm-2 p-2 text-red-700 bg-white hover:bg-red-200 hover:text-red-500 border focus:border-red-500 focus:outline-none'

async def count_down(self, msg):
    self.show = False
    if hasattr(msg.page, 'd'):
        msg.page.remove(msg.page.d)
    bomb_icon = jp.Icon(icon='bomb', classes='inline-block text-5xl ml-1 mt-1', a=msg.page)
    d = jp.Div(classes='text-center m-4 p-4 text-6xl text-red-600 bg-blue-500 faster', a=msg.page, animation=self.count_animation)
    msg.page.d = d
    for i in range(self.start_num, 0 , -1):
        d.text = str(i)
        await msg.page.update()
        await asyncio.sleep(1)
    d.text = 'Boom!'
    d.animation = 'zoomIn'
    d.set_classes('text-red-500 bg-white')
    bomb_icon.set_class('text-red-700')
    self.show = True

def count_test(request):
    start_num = int(request.query_params.get('num', 10))
    animation = request.query_params.get('animation', 'flip')
    wp = jp.WebPage()
    count_button = jp.Button(text='Start Countdown', classes=button_classes, a=wp, click=count_down)
    count_button.start_num = start_num
    count_button.count_animation = animation
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("count_test",count_test)
