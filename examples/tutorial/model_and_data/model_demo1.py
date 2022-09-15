# Justpy Tutorial demo model_demo1 from docs/tutorial/model_and_data.md
import justpy as jp

corner_classes = 'p-3 absolute bg-gray-200 '

def model_demo1():
    wp = jp.WebPage()
    d = jp.Div(classes='relative h-screen bg-gray-600', a=wp, data={'text': ''})
    for v_pos in ['top', 'bottom']:
        for h_pos in ['left', 'right']:
            corner_div = jp.Div(classes=corner_classes + f'{v_pos}-0 {h_pos}-0', a=d)
            jp.Div(text=f'{v_pos} {h_pos}', a=corner_div)
            jp.Div(text=f'typing will go here', a=corner_div, model=[d, 'text'])
    middle_input = jp.Input(text='middle', classes='absolute text-xl border-2 border-red-600',
                            placeholder='Type here', style='top: 50%; left: 40%', model=[d, 'text'], a=d)
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("model_demo1",model_demo1)
