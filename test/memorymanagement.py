import justpy as jp
from datetime import datetime
import sys
import gc



input_classes = 'm-2 bg-gray-200 font-mono appearance-none border-2 border-gray-200 rounded py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-orange-500'
button_classes = 'm-2 p-2 text-orange-700 bg-white hover:bg-orange-200 hover:text-orange-500 border focus:border-orange-500 focus:outline-none'
message_classes = 'ml-4 p-2 text-lg bg-orange-500 text-white overflow-auto font-mono rounded-lg'

shared_div = jp.Div(classes='m-2 h-1/2 border overflow-auto')
header = jp.Div(text='Simple Message Board', classes='bg-orange-100 border-l-4 border-orange-500 text-orange-700 p-4 text-3xl')
button_icon = jp.Icon(icon='paper-plane', classes='text-2xl')
button_text = jp.Div(text='Send', classes='text-sm')
message_icon = jp.Icon(icon='comments', classes='text-2xl text-green-600')

def print_ref_count(c):
    print(sys.getrefcount(c), c)
    for sub_c in c.components:
       if shared_div.id != sub_c.id:
        print_ref_count(sub_c)

class MyPage(jp.WebPage):

    async def on_disconnect(self, websocket):
        shared_div.remove_page_from_pages(self)
        self.remove_page()
        for c in self.components:
            c.delete()
        del self
        print('Number of not temp components:', len(jp.JustpyBaseComponent.instances))
        print('Collected:', gc.collect())

def message_initialize():
    d = jp.Div(a=shared_div, classes='flex m-2 border')
    time_stamp = jp.P(text=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), classes='text-xs ml-2 flex-shrink-0')
    p = jp.Pre(text='Welcome to the simple message board!', classes=message_classes)
    d.add(message_icon, time_stamp, p)

async def send_message(self, msg):
    if self.message.value:
        d = jp.Div(classes='flex m-2 border', temp=True)
        time_stamp = jp.P(text=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), classes='text-xs ml-2 flex-shrink-0', temp=True)
        p = jp.Pre(text=self.message.value, classes=message_classes, temp=True)
        d.add(message_icon, time_stamp, p)
        shared_div.add_component(d, 0)
        self.message.value = ''     # Clear message box after message is sent
        await shared_div.update()

def message_demo():
    wp = MyPage()
    print(wp.instances)
    outer_div = jp.Div(classes='flex flex-col h-screen', a=wp, temp=True)
    outer_div.add(header)
    d = jp.Div(classes='flex', a=outer_div, temp=True)
    message = jp.TextArea(placeholder='Enter message here', a=d, classes=input_classes)
    send_button = jp.Button(a=d, click=send_message, classes=button_classes)
    send_button.add(button_icon, button_text)
    outer_div.add(shared_div)
    outer_div.add(shared_div)
    # shared_div.pages.append(wp)
    # shared_div.pages[wp.page_id] = wp
    shared_div.add_page_to_pages(wp)
    send_button.message = message
    wp.gc_list = [message, send_button]
    return wp

jp.justpy(message_demo, startup=message_initialize)

