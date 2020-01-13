import justpy as jp

input_classes = "m-2 bg-gray-200 border-2 border-gray-200 rounded w-64 py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-purple-500"
p_classes = 'm-2 p-2 h-32 text-xl border-2'

async def my_click(self, msg):
    print(self.in1.value)
    self.div.text = self.in1.value

async def input_demo(request):
    wp = jp.WebPage()
    in1 = jp.Input(a=wp, classes=input_classes, placeholder='Please type here', no_events=True, value='hhhh')
    b = jp.Button(text='Update Div', classes=jp.Styles.button_simple, a=wp, click=my_click)
    b.in1 = in1
    b.div = jp.Div(text='What you type will show up here', classes=p_classes, a=wp)
    return wp

jp.justpy(input_demo)