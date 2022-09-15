# Justpy Tutorial demo link_demo2 from docs/tutorial/html_components.md
import justpy as jp

def link_demo2():
    wp = jp.WebPage()
    link = jp.A(text='Scroll to target', a=wp, classes='inline-block m-2 p-2 text-xl text-white bg-blue-500 hover:bg-blue-700')
    # jp.Br(a=wp)
    for i in range(50):
        jp.P(text=f'{i+1} Not a target', classes='m-1 p-1 text-white bg-blue-300', a=wp)
    target = jp.A(text=f'This is the target - it is linked to first link, click to jump there', classes='inline-block m-1 p-1 text-white bg-red-500', a=wp)
    link.bookmark = target
    link.scroll = True
    target.bookmark = link
    for i in range(50):
        jp.P(text=f'{i+50} Not a target', classes='m-1 p-1 text-white bg-blue-300', a=wp)
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("link_demo2",link_demo2)
