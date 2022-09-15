# Justpy Tutorial demo html_comps4 from docs/tutorial/html_components.md
import justpy as jp

def html_comps4():
    wp = jp.WebPage()
    for i in range(10):
        d = jp.Div(a=wp, classes='m-2')
        for j in range(10):
            jp.Span(text=f'Span #{j+1} in Div #{i+1}', a=d, classes='text-white bg-blue-700 hover:bg-blue-200 ml-1 p-1')
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("html_comps4",html_comps4)
