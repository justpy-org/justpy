# Justpy Tutorial demo demo_function from docs/tutorial/request_object.md
import justpy as jp

def demo_function(request):
    wp = jp.WebPage()
    if len(request.query_params) > 0:
        for key, value in request.query_params.items():
            jp.P(text=f'{key}: {value}', a=wp, classes='text-xl m-2 p-1')
    else:
        jp.P(text='No URL paramaters present', a=wp, classes='text-xl m-2 p-1')
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("demo_function",demo_function)
