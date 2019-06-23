import justpy as jp
import time
import asyncio

wp = jp.WebPage()
clock_div = jp.Span(text='loading...', classes='text-5xl m-1 p-1 bg-gray-300 font-mono', a=wp)

async def clock_counter():
    while True:
        clock_div.text = time.strftime("%a, %d %b %Y, %H:%M:%S", time.localtime())
    # jp.JustPy.loop.create_task(wp.update())
        jp.run_task(wp.update())
        await asyncio.sleep(1)
    # jp.JustPy.loop.create_task(clock_counter())
    # jp.run_task(clock_counter())


async def clock_test(request):
    jp.print_request(request)
    return wp


async def clock_init():
    jp.JustPy.loop.create_task(clock_counter())


async def ajax_clock_counter():
    clock_div.text = time.strftime("%a, %d %b %Y, %H:%M:%S", time.localtime())
    await asyncio.sleep(1)
    jp.JustPy.loop.create_task(ajax_clock_counter())


async def ajax_clock_test(request):
    wp.reload_interval = 0.5
    return wp


async def ajax_clock_init():
    jp.JustPy.loop.create_task(ajax_clock_counter())

# jp.justpy(ajax_clock_test, startup=ajax_clock_init, websockets=False)



import justpy as jp

session_dict = {}

def session_test(request):
    wp = jp.WebPage()
    print('session ',jp.SESSIONS)
    if request.session_id in session_dict:
        session_data = session_dict[request.session_id]
    else:
        session_dict[request.session_id] = {'visits': 0, 'events': 0}
        session_data = session_dict[request.session_id]
    session_data['visits'] += 1
    jp.Div(text=f'My session id: {request.session_id}', classes='m-2 p-1 text-xl', a=wp)
    visits = session_data['visits']
    visits_div = jp.Div(text=f'Number of visits: {visits}', classes='m-2 p-1 text-xl', a=wp)
    events = session_data['events']
    b = jp.Button(text=f'Number of Click Events: {events}', classes='m-1 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full', a=wp)
    b.visits_div = visits_div

    def click(self, msg):
        session_data = session_dict[msg.session_id]
        session_data['events'] += 1
        events = session_data['events']
        self.text =f'Number of Click Events: {events}'
        visits = session_data['visits']
        self.visits_div.text = f'Number of visits: {visits}'

    b.on('click', click)
    return wp



# jp.justpy(session_test)
# jp.justpy(clock_test)
# Click on button to add events and open page in another tab or browser to add visits


jp.justpy(clock_test, startup=clock_init)
# jp.justpy(clock_test, startup=clock_init, host='198.199.81.28', port=80, websockets=True)
