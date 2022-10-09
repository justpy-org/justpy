# Justpy Tutorial demo transition_test from docs/tutorial/transitions.md
import justpy as jp

def toggle_hidden(self, msg):
    for d in self.div_list:
        if d.has_class('hidden'):
            d.remove_class('hidden')
        else:
            d.set_class('hidden')


def transition_test():
    wp = jp.WebPage()
    tran = jp.Dict()
    tran.load = "transition ease-out duration-1000"
    tran.load_start = 'opacity-0 transform scale-0'
    tran.load_end = 'opacity-100 transform scale-100'
    tran.enter = 'transition ease-out duration-1000'
    tran.enter_start = 'opacity-0 transform scale-0'
    tran.enter_end = 'opacity-100 transform scale-1000'
    tran.leave = "transition ease-out duration-1000"
    tran.leave_start = 'opacity-100 transform scale-1000'
    tran.leave_end = 'opacity-0 transform scale-0'
    div_list = []
    flex_div = jp.Div(classes='flex flex-wrap', a=wp)
    for i in range(10):
        d = jp.Div(a=flex_div, text='hello', style='height: 150px; width:200px')
        jp.Pre(text=' test', a=d)
        d.transition = tran
        d.classes = 'border text-xl m-2 h-16 w-16 bg-blue-500'
        div_list.append(d)
    b = jp.Button(text='Click here', classes=jp.Styles.button_simple + ' m-2', a=wp, click=toggle_hidden)
    b.div_list = div_list
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("transition_test",transition_test)
