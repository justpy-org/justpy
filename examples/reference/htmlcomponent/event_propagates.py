# Justpy Tutorial demo event_propagates from docs/reference/htmlcomponent.md
import justpy as jp

def event_propagates():
    wp = jp.WebPage()
    main_div = jp.Div(classes='flex flex-wrap m-2 p-2 ', a=wp, click='self.text="main div clicked"')
    for i in range(1,10):
        jp.Div(text=f'Div {i}', a=main_div, classes='m-2 p-2 text-xl text-white bg-blue-500', click='self.text="clicked"')
    return wp

@jp.SetRoute('/no_propagation')
def event_does_not_propagate():
    wp = jp.WebPage()
    main_div = jp.Div(classes='flex flex-wrap m-2 p-2 ', a=wp, click='self.text="main div clicked"')
    for i in range(1,10):
        jp.Div(text=f'Div {i}', a=main_div, classes='m-2 p-2 text-xl text-white bg-blue-500',
               event_propagation=False, click='self.text="clicked"')
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("event_propagates",event_propagates)
