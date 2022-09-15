# Justpy Tutorial demo text_colors from docs/tutorial/tailwind.md
import justpy as jp

def text_colors():
    wp = jp.WebPage()
    d = jp.Div(classes='flex flex-wrap m-2', a=wp)
    for color in jp.Tailwind.tw_dict['text_color']:
        jp.Div(text=color, classes=f'{color} font-mono p-1 text-lg bg-blue-100 hover:bg-red-500 w-48', a=d)
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("text_colors",text_colors)
