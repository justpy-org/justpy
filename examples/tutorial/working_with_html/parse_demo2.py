# Justpy Tutorial demo parse_demo2 from docs/tutorial/working_with_html.md
import justpy as jp

async def parse_demo2(request):
    wp = jp.WebPage()
    c = jp.parse_html("""
    <div>
    <p class="m-2 p-2 text-red-500 text-xl">Paragraph 1</p>
    <p class="m-2 p-2 text-blue-500 text-xl" name="p2">Paragraph 2</p>
    <p class="m-2 p-2 text-green-500 text-xl">Paragraph 3</p>
    </div>
    """, a=wp)
    p2 = c.name_dict['p2']
    def my_click(self, msg):
        self.text = 'I was clicked!'
    p2.on('click', my_click)
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("parse_demo2",parse_demo2)
