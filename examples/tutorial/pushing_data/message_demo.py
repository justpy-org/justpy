# Justpy Tutorial demo message_demo from docs/tutorial/pushing_data.md

import justpy as jp
from datetime import datetime

input_classes = 'm-2 bg-gray-200 font-mono appearance-none border-2 border-gray-200 rounded py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-red-500'
button_classes = 'm-2 p-2 text-red-700 bg-white hover:bg-red-200 hover:text-red-500 border focus:border-red-500 focus:outline-none'
message_classes = 'ml-4 p-2 text-lg bg-red-500 text-white overflow-auto font-mono rounded-lg'

shared_div = jp.Div(classes='m-2 h-1/2 border overflow-auto', delete_flag=False)
header = jp.Div(text='Simple Message Board', classes='bg-red-100 border-l-4 border-red-500 text-red-700 p-4 text-3xl', delete_flag=False)
button_icon = jp.Icon(icon='paper-plane', classes='text-2xl', delete_flag=False)
button_text = jp.Div(text='Send', classes='text-sm', delete_flag=False)
message_icon = jp.Icon(icon='comments', classes='text-2xl text-green-600', delete_flag=False)

def message_initialize():
    # Called once on startup
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
    message = jp.Textarea(placeholder='Enter message here', a=d, classes=input_classes, debounce=500)
    send_button = jp.Button(a=d, click=send_message, classes=button_classes)
    send_button.add(button_icon, button_text)
    outer_div.add(shared_div)
    shared_div.add_page(wp)
    send_button.message = message
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("message_demo",message_demo, startup=message_initialize)
