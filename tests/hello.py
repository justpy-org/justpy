import justpy as jp

def my_click(self, msg):
    self.text = 'I was clicked'

def event_demo():
    wp = jp.WebPage()
    d = jp.Div(text='Not clicked yet', classes='w-48 text-xl m-2 p-1 bg-blue-500 text-white', a=wp)
    d.on('click', my_click)
    return wp

jp.justpy(event_demo)
