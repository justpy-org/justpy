# Justpy Tutorial demo input_demo_quasar1 from docs/quasar_tutorial/quasar_components.md
import justpy as jp

def my_blur(self, msg):
    """
    event handler for loosing the focus
    """
    self.div.text = self.value

def input_demo_quasar1(request):
    """
    show how the blue event works
    """
    wp = jp.QuasarPage()
    c1 = jp.Div(classes='q-pa-md', a=wp)
    c2 = jp.Div(classes='q-gutter-md', style='max-width: 300px', a=c1)
    in1 = jp.QInputBlur(a=c2,placeholder='Please type here', label='QInputBlur')
    in1.div = jp.Div(text='What you type will show up here only when Input element loses focus',
                      classes='text-h6', a=c2)
    in1.on('blur', my_blur)
    return wp

# initialize the demo
from examples.basedemo import Demo
Demo("input_demo_quasar1", input_demo_quasar1)
