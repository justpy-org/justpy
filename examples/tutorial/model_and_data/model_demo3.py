# Justpy Tutorial demo model_demo3 from docs/tutorial/model_and_data.md
import justpy as jp

corner_classes = 'p-3 absolute bg-gray-200 '

class MyDiv(jp.Div):

    def model_update3(self):
        # [wp, 'text-data'] for example
        if self.model[0].data[self.model[1]]:
            self.text = (str(self.model[0].data[self.model[1]]) + ' ')*self.repeat
        else:
            self.text = self.initial_text


def model_demo3():
    wp = jp.WebPage()
    d = jp.Div(classes='relative h-screen bg-gray-600', a=wp, data={'text': ''})
    repeat = 1
    for v_pos in ['top', 'bottom']:
        for h_pos in ['left', 'right']:
            corner_div = jp.Div(classes=corner_classes + f'{v_pos}-0 {h_pos}-0', a=d)
            jp.Div(text=f'{v_pos} {h_pos}', a=corner_div)
            MyDiv(text=f'typing will go here', a=corner_div, model=[d, 'text'], repeat=repeat, initial_text = 'Yada Yada')
            repeat += 1
    middle_input = jp.Input(text='middle', classes='absolute text-xl border-2 border-red-600',
                            placeholder='Type here', style='top: 50%; left: 40%', model=[d, 'text'], a=d)
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("model_demo3",model_demo3)
