# https://www.divio.com/blog/documentation/    tutorials how-to guides explanation reference

import justpy as jp
from datetime import datetime

input_classes = 'm-2 bg-gray-200 font-mono appearance-none border-2 border-gray-200 rounded py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-orange-500'
button_classes = 'm-2 p-2 text-orange-700 bg-white hover:bg-orange-200 hover:text-orange-500 border focus:border-orange-500 focus:outline-none'
message_classes = 'ml-4 p-2 text-lg bg-orange-500 text-white overflow-auto font-mono rounded-lg'

shared_div = jp.Div(classes='m-2 h-1/2 border overflow-auto')
header = jp.Div(text='Simple Message Board', classes='bg-orange-100 border-l-4 border-orange-500 text-orange-700 p-4 text-3xl')
button_icon = jp.Icon(icon='paper-plane', classes='text-2xl')
button_text = jp.Div(text='Send', classes='text-sm')
message_icon = jp.Icon(icon='comments', classes='text-2xl text-green-600')

def message_initialize():
    d = jp.Div(a=shared_div, classes='flex m-2 border')
    time_stamp = jp.P(text=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), classes='text-xs ml-2 flex-shrink-0')
    p = jp.Pre(text='Welcome to the simple message board!', classes=message_classes)
    d.add(message_icon, time_stamp, p)

async def send_message(self, msg):
    if self.message.value:
        d = jp.Div(classes='flex m-2 border')
        time_stamp = jp.P(text=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), classes='text-xs ml-2 flex-shrink-0')
        p = jp.Pre(text=self.message.value, classes=message_classes)
        d.add(message_icon, time_stamp, p)
        shared_div.add_component(d, 0)
        self.message.value = ''     # Clear message box after message is sent
        await shared_div.update()

def message_demo():
    wp = jp.WebPage()
    outer_div = jp.Div(classes='flex flex-col h-screen', a=wp)
    outer_div.add(header)
    d = jp.Div(classes='flex', a=outer_div)
    message = jp.TextArea(placeholder='Enter message here', a=d, classes=input_classes)
    send_button = jp.Button(a=d, click=send_message, classes=button_classes)
    send_button.add(button_icon, button_text)
    outer_div.add(shared_div)
    shared_div.pages.append(wp)
    send_button.message = message
    return wp

jp.justpy(message_demo, startup=message_initialize)

# jp.template_options['tailwind'] = False
# wp = jp.WebPage()
# e = jp.EditorJP(a=wp)

def edit_test(request):
    return wp

# jp.justpy(edit_test)

import time
import asyncio

# wp = jp.WebPage()
# clock_div = jp.Span(text='loading...', classes='text-5xl m-1 p-1 bg-gray-300 font-mono', a=wp)

async def clock_counter():
    while True:
        clock_div.text = time.strftime("%a, %d %b %Y, %H:%M:%S", time.localtime())
        jp.run_task(wp.update())
        await asyncio.sleep(1)

async def clock_init():
    jp.run_task(clock_counter())

async def clock_test():
    print(jp.TAILWIND)
    return wp

# jp.justpy(clock_test, startup=clock_init)

async def parse_demo(request):
    wp = jp.WebPage()
    c = jp.parse_html("""
    <div>
    <p class="m-2 p-2 text-red-500 text-xl">Paragraph 1</p>
    <p class="m-2 p-2 text-blue-500 text-xl" name="p2">Paragraph 2</p>
    <p class="m-2 p-2 text-green-500 text-xl">Paragraph 3</p>
    </div>
    """, a=wp)
    p2 = c.name_dict['p2']
    def my_click(self, msg):
        self.text = 'I was clicked!'
        print(c.to_html(0, 4))
    p2.on('click', my_click)
    print(c.to_html(0, 4))
    return wp



def button_click(self, msg):
    self.num_clicked += 1
    # self.message.text = f'{self.text} clicked. Number of clicks: {self.num_clicked}'
    p = jp.P(text=f'{self.text} clicked. Number of clicks: {self.num_clicked}')
    self.message.add_component(p, 0)
    for button in msg.page.button_list:
        button.set_class('bg-blue-500')
        button.set_class('bg-blue-700', 'hover')
    self.set_class('bg-red-500')
    self.set_class('bg-red-700', 'hover')

def event_demo():
    number_of_buttons = 25
    wp = jp.WebPage()
    button_div = jp.Div(classes='flex m-4 flex-wrap', a=wp)
    button_classes = 'w-32 mr-2 mb-2 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full'
    message = jp.Div(classes='text-lg border m-2 p-2 overflow-auto h-64', a=wp)
    message.add(jp.P(text='No button clicked yet'))
    button_list = []
    for i in range(1, number_of_buttons + 1):
        b = jp.Button(text=f'Button {i}', a=button_div, classes=button_classes, click=button_click)
        b.message = message
        b.num_clicked = 0
        button_list.append(b)
    wp.button_list = button_list   # The list will now be stored in the WebPage instance
    return wp

jp.justpy(event_demo)


def hello_world1():
    wp = jp.WebPage()
    p = jp.P(text='Hello World!', a=wp)
    return wp


def hello_world2():
    wp = jp.WebPage()
    for i in range(1,11):
        jp.P(text=f'{i}) Hello World!', a=wp, style=f'color: blue; font-size: {10*i}px' , click='self.text = "I was clicked"')
    return wp

def hello_world3():
    wp = jp.WebPage()
    my_paragraph_design = 'cursor-pointer m-2 w-1/3 bg-blue-500 hover:bg-blue-400 text-white font-bold py-2 px-4' \
                          ' border-b-4 border-blue-700 hover:border-blue-500 rounded'
    for i in range(1,11):
        jp.P(text=f'{i}) Hello World!', a=wp, classes=my_paragraph_design)
    return wp

def my_click1(self, msg):
    self.text = 'I was clicked'
    print(msg.event_type)
    print(msg['event_type'])
    print(msg)

def event_demo1():
    wp = jp.WebPage()
    d = jp.P(text='Not clicked yet', classes='text-xl m-2 p-2 bg-blue-500 text-white', a=wp)
    d.on('click', my_click)
    return wp

def event_demo2():
    wp = jp.WebPage()
    jp.P(text='Not clicked yet', classes='text-xl m-2 p-2 bg-blue-500 text-white', a=wp,
         click="self.text = 'I was clicked'; print(msg.event_type); print(msg['event_type']); print(msg)")
    return wp

def event_demo3():
    wp = jp.WebPage()
    jp.P(text='Not clicked yet', classes='w-64 text-xl text-center m-2 p-2 bg-blue-500 text-white', a=wp,
         click="self.text = 'I was clicked'; self.set_class('bg-red-500')",
         mouseenter="self.text = 'Mouse In!'",
         mouseleave="self.text = 'Mouse Out!'")
    return wp