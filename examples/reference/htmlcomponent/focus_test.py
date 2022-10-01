# Justpy Tutorial demo focus_test from docs/reference/htmlcomponent.md
import justpy as jp

# Try not using this event handler and see what happens
def my_blur(self, msg):
        self.set_focus = False

def focus_test():
    wp = jp.WebPage()
    in1 = jp.Input(classes=jp.Styles.input_classes, placeholder='Input 1', a=wp, blur=my_blur)
    in2 = jp.Input(classes=jp.Styles.input_classes, placeholder='Input 2', a=wp, blur=my_blur)
    in3 = jp.Input(classes=jp.Styles.input_classes, placeholder='Input 3', a=wp, blur=my_blur)
    in4 = jp.Input(classes=jp.Styles.input_classes, placeholder='Input 4', a=wp, blur=my_blur)

    # Set focus on third Input element
    in3.set_focus = True

    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("focus_test",focus_test)
