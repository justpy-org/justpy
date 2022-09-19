# Justpy Tutorial demo commands_demo2 from docs/tutorial/working_with_html.md
import justpy as jp

def commands_demo2():
    wp = jp.WebPage()
    root = jp.Div(a=wp)
    c1 = jp.Div(a=root)
    c2 = jp.P(classes='m-2 p-2 text-red-500 text-xl', a=c1, text='Paragraph 1')
    c3 = jp.P(classes='m-2 p-2 text-blue-500 text-xl', a=c1, text='Paragraph 2')
    c4 = jp.P(classes='m-2 p-2 text-green-500 text-xl', a=c1, text='Paragraph 3')
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("commands_demo2",commands_demo2)
