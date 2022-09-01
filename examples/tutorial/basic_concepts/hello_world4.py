# Justpy Tutorial demo hello_world4 from docs/tutorial/basic_concepts.md
import justpy as jp

wp = jp.WebPage(delete_flag=False)
my_paragraph_design = "w-64 bg-blue-500 m-2 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
for i in range(1,11):
    jp.P(text=f'{i}) Hello World!', a=wp, classes=my_paragraph_design)

def hello_world4():
    return wp

    You can also put your own CSS on a page and use your own class definitions by setting the `css` attribute of a page.
# initialize the demo
from  examples.basedemo import Demo
Demo ("hello_world4",hello_world4)
