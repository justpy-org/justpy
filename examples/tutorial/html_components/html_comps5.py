# Justpy Tutorial demo html_comps5 from docs/tutorial/html_components.md
import justpy as jp

def html_comps5():
    wp = jp.WebPage()
    for j in range(10):
        p = jp.P(text=f'אני אוהב לתכנת בפייתון', a=wp, contenteditable=True, classes='text-white bg-blue-500 hover:bg-blue-700 ml-1 p-1 w-1/2')
        p.dir = 'rtl'
        p.lang = 'he'
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("html_comps5",html_comps5)
