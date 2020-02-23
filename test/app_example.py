import justpy as jp

@jp.SetRoute('/simple')
def simple_demo(request):
    print(request)
    wp = jp.WebPage()
    d = jp.Div(text='Hello', add_to=wp)
    b = jp.Button(text='Please click me', add_to=wp)
    def my_click(self, msg):
        d.text += ' Click!'
    b.on('click', my_click)
    return wp



async def test1():
    print('my init function')

def hello_world(request):
    print(request)
    wp = jp.WebPage()
    jp.Hello(a=wp)
    return wp



# jp.justpy(hello_world,startup=test1)
def span_test():
    wp = jp.WebPage()
    for _ in range(20):
        s = jp.Span(text='hello, I am a SPAN', a=wp, classes='m-1 p-1 text-red-500 bg-gray-300')
        print(s.attributes)
        b = jp.Button(text='Button is ME', a=wp, classes='m-1 p-1 text-red-500 bg-gray-300', click='self.s.text = "I was clicked"')
        print(b.attributes)
        b.s = s
        jp.Br(a=wp)
    return wp

jp.justpy(span_test)
