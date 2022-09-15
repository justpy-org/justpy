# Justpy Tutorial demo check_test from docs/tutorial/input.md
import justpy as jp

def check_test():
    wp = jp.WebPage(data={'checked': True})
    label = jp.Label(a=wp, classes='m-2 p-2 inline-block')
    c = jp.Input(type='checkbox', classes='m-2 p-2 form-checkbox', a=label, model=[wp, 'checked'])
    caption = jp.Span(text='Click to get stuff', a=label)

    in1 = jp.Input(model=[wp, 'checked'], a=wp, classes='border block m-2 p-2')
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("check_test",check_test)
