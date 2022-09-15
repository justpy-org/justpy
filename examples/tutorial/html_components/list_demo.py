# Justpy Tutorial demo list_demo from docs/tutorial/html_components.md
import justpy as jp

def list_demo():
    wp = jp.WebPage()
    my_list = jp.Ul(a=wp, classes='m-2 p-2')
    for i in range (1,11):
        jp.Li(text=f'List one item {i}', a=my_list)
    my_list = jp.Ul(a=wp, classes='m-2 p-2 list-disc list-inside')
    for i in range(1, 11):
        jp.Li(text=f'List two item {i}', a=my_list, classes='hover:bg-gray-200')
    my_list = jp.Ul(a=wp, classes='m-2 p-2 list-decimal list-inside')
    for i in range(1, 11):
        jp.Li(text=f'List three item {i}', a=my_list)
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("list_demo",list_demo)
