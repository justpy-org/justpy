# Justpy Tutorial demo shuffle_test from docs/reference/htmlcomponent.md
import justpy as jp
import random

def shuffle_test():
    wp = jp.WebPage()
    main_div = jp.Div(classes='flex flex-wrap m-2 p-2 ', a=wp)
    for i in range(1,101,1):
        jp.Div(text=f'Div {i}', a=main_div, classes='m-2 p-2 text-xl text-white bg-blue-500')
    random.shuffle(main_div.components)
    return wp


# initialize the demo
from  examples.basedemo import Demo
Demo ("shuffle_test",shuffle_test)
