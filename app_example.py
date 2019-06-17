import justpy as jp

async def test1():
    print('my init function')

def hello_world(request):
    wp = jp.WebPage()
    jp.Hello(a=wp)
    return wp


jp.justpy(hello_world,startup=test1)

