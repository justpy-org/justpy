import justpy as jp
import asyncio

button_classes = 'm-2 p-2 text-orange-700 bg-white hover:bg-orange-200 hover:text-orange-500 border focus:border-orange-500 focus:outline-none'

async def count_down(self, msg):
    self.show = False
    msg.page.add(jp.Br())
    d = jp.Span(classes='m-4 p-4 text-6xl text-white bg-blue-500 animate bounce', a=msg.page)
    for i in range(self.start_num, 0 , -1):
        d.text = str(i)
        await msg.page.update()
        await asyncio.sleep(1)
    d.text = 'Boom!'
    d.set_classes('text-red-500 bg-white')
    self.show = True

def count_test(request):
    start_num = request.query_params.get('num', 10)
    wp = jp.WebPage()
    count_button = jp.Button(text='Start Countdown', classes=button_classes, a=wp, click=count_down)
    count_button.start_num = start_num
    return wp

jp.justpy(count_test)