
def parse_line(s):
    print(s)
    code_lines = [x.strip() for x in s.split(';')]
    print(code_lines)
    ident = '\n '
    fn_string = 'def click():'
    for code_line in code_lines:
        fn_string = f'{fn_string}{ident}{code_line}'
    print(fn_string)
    print('-------------------')
    exec(fn_string)
    print(locals())
    print('-------------------')
    locals()['click']()



from justpy import *

def oneliner_test(request):
    wp = WebPage()
    d = Div(text="The Div", classes='m-1 p-1 text-xl bg-blue-700 text-white hover:bg-yellow-700', a=wp)
    def my_click(self, msg):
        self.div.text = 'I was clicked'
    # b = Button(text="The Button", classes='m-1 p-1 text-xl bg-blue-700 text-white hover:bg-yellow-300', a=wp, onclick=my_click)
    b = Button(text="The Button", classes='m-1 p-1 text-xl bg-blue-700 text-white hover:bg-yellow-300', a=wp, click="self.div.text = f'I was really clicked {self.counter*2}'; print('in click'); self.counter += 1")
    b.div = d
    b.counter = 0
    print(globals())
    return wp

justpy(oneliner_test)

def test1(self, msg):
    print(self); print(msg)   ; print('hello')

# test1(1,2)