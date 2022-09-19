# Justpy Tutorial demo commands_demo1 from docs/tutorial/working_with_html.md
import justpy as jp

def commands_demo1():
    wp = jp.WebPage()
    c = jp.parse_html("""
        <div>
        <p class="m-2 p-2 text-red-500 text-xl">Paragraph 1</p>
        <p class="m-2 p-2 text-blue-500 text-xl">Paragraph 2</p>
        <p class="m-2 p-2 text-green-500 text-xl">Paragraph 3</p>
        </div>
        """, a=wp)
    for i in c.commands:
        print(i)
        jp.Div(text=i, classes='font-mono ml-2', a=wp)
    print()
    c = jp.parse_html("""
            <div>
            <p class="m-2 p-2 text-red-500 text-xl">Paragraph 1</p>
            <p class="m-2 p-2 text-blue-500 text-xl">Paragraph 2</p>
            <p class="m-2 p-2 text-green-500 text-xl">Paragraph 3</p>
            </div>
            """, a=wp, command_prefix='justpy.')
    for i in c.commands:
        print(i)
        jp.Div(text=i, classes='font-mono ml-2', a=wp)
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("commands_demo1",commands_demo1)
