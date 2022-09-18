# Justpy Tutorial demo inner_demo from docs/tutorial/working_with_html.md
import justpy as jp

my_html = """
    <div>
    <p class="m-2 p-2 text-red-500 text-xl">Paragraph 1</p>
    <p class="m-2 p-2 text-blue-500 text-xl">Paragraph 2</p>
    <p class="m-2 p-2 text-green-500 text-xl">Paragraph 3</p>
    </div>
    """

def inner_demo():
    wp = jp.WebPage()
    d = jp.Div(a=wp, classes='m-4 p-4 text-3xl')
    d.inner_html = '<pre>Hello there. \n How are you?</pre>'
    jp.Div(a=wp, inner_html=my_html)
    for color in ['red', 'green', 'blue', 'pink', 'yellow', 'teal', 'purple']:
        jp.Div(a=wp, inner_html=f'<p class="ml-2 text-{color}-500 text-3xl">{color}</p>')
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("inner_demo",inner_demo)
