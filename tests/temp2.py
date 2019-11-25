import justpy as jp
import asyncio

def h_test():
    wp = jp.QuasarPage()
    wp.add(jp.Hello())
    b = jp.Button(text='click me', a=wp, classes="m-2 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded", click=my_click)
    b.counter = 0
    return wp

async def my_click(self, msg):
    self.counter += 1
    self.text = f'I was clicked {self.counter} times'
    msg.page.display_url = f'/{self.counter}/{self.counter}'
    for i in range(4):
        msg.page.open = 'http://example.com'
        await asyncio.sleep(0.5)
        await msg.page.update()
    return True


@jp.SetRoute('/test')
def change_page():
    wp = jp.WebPage()
    b = jp.Button(text='Page Change', a=wp,
                  classes="m-2 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded")
    b.counter = 0
    return wp

jp.justpy(h_test)

