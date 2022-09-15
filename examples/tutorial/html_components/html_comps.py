# Justpy Tutorial demo html_comps from docs/tutorial/html_components.md
import justpy as jp

def straighten2(self, msg):
    self.style = f'transform: rotate(0deg)'

def rotate_back2(self, msg):
    self.style = f'transform: rotate({self.degree}deg)'

def no_rotate2(self, msg):
    self.degree = 0
    self.set_class('bg-red-200')

def html_comps():
    wp = jp.WebPage()
    for degree in range(0, 361, 10):
        jp.Img(src='https://www.python.org/static/community_logos/python-powered-h-140x182.png', a=wp,
                classes='m-4 p-4 inline-block', style=f'transform: rotate({degree}deg)', height=100, width=100,
                degree=degree, mouseenter=straighten2, mouseleave=rotate_back2, click=no_rotate2)
    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("html_comps",html_comps)
