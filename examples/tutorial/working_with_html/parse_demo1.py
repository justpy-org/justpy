# Justpy Tutorial demo parse_demo1 from docs/tutorial/working_with_html.md
import justpy as jp

async def parse_demo1(request):
    wp = jp.WebPage()
    c = jp.parse_html("""
    <div>
    <p class="m-2 p-2 text-red-500 text-xl">Paragraph 1</p>
    <p class="m-2 p-2 text-blue-500 text-xl">Paragraph 2</p>
    <p class="m-2 p-2 text-green-500 text-xl">Paragraph 3</p>
    </div>
    """, a=wp)
    print(c)
    print(c.components)
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("parse_demo1",parse_demo1)
