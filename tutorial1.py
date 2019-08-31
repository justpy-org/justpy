import asyncio
import justpy as jp

my_html = """
    <div>
    <p class="m-2 p-2 text-red-500 text-xl">Paragraph 1</p>
    <p class="m-2 p-2 text-blue-500 text-xl">Paragraph 2</p>
    <p class="m-2 p-2 text-green-500 text-xl">Paragraph 3</p>
    </div>
    """

def inner_demo():
    wp = jp.WebPage()
    d = jp.Div(a=wp, classes='m-4 p-4 text-3xl')
    d.inner_html = '<pre>Hello there. \n How are you?</pre>'
    jp.Div(a=wp, inner_html=my_html)
    for color in ['red', 'green', 'blue', 'pink', 'yellow', 'teal', 'purple']:
        jp.Div(a=wp, inner_html=f'<p class="ml-2 text-{color}-500 text-3xl">{color}</p>')
    return wp

jp.justpy(inner_demo)
# wp = jp.WebPage()
# wp.reload_interval = 2.5
# count_div = jp.Span(a=wp, classes='text-center inline-block m-4 p-4 text-white bg-blue-500', style='font-size: 200px')

async def increment_counter(start):
    count_div.counter = start
    while True:
        count_div.counter += 1
        count_div.text = str(count_div.counter)
        await asyncio.sleep(1)

def start_counting():
    jp.run_task(increment_counter(500))

def reload_demo():
    return wp

# jp.justpy(reload_demo, startup=start_counting, websockets=False)
# button_classes = 'm-2 p-2 text-orange-700 bg-white hover:bg-orange-200 hover:text-orange-500 border focus:border-orange-500 focus:outline-none'
# bomb_icon = jp.Icon(icon='bomb', classes='inline-block', temp=True)

async def count_down(self, msg):
    self.show = False
    # msg.page.add(jp.Br())
    if hasattr(msg.page, 'd'):
        msg.page.remove(msg.page.d)
    msg.page.add(bomb_icon)
    d = jp.Div(classes='text-center m-4 p-4 text-6xl text-red-600 bg-blue-500 faster', a=msg.page, animation=self.count_animation)
    msg.page.d = d
    for i in range(self.start_num, 0 , -1):
        d.text = str(i)
        await msg.page.update()
        await asyncio.sleep(1)
    d.text = 'Boom!'
    d.set_classes('text-red-500 bg-white')
    self.show = True

def count_test(request):
    start_num = int(request.query_params.get('num', 10))
    animation = request.query_params.get('animation', 'flip')
    wp = jp.WebPage()
    count_button = jp.Button(text='Start Countdown', classes=button_classes, a=wp, click=count_down)
    count_button.start_num = start_num
    count_button.count_animation = animation
    return wp

# jp.justpy(count_test)