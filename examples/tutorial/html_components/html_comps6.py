# Justpy Tutorial demo html_comps6 from docs/tutorial/html_components.md
import justpy as jp

def html_comps6():
    wp = jp.WebPage()
    for degree in range(0, 361, 10):
        image = jp.Img(src='https://www.python.org/static/community_logos/python-powered-h-140x182.png', a=wp)
        image.classes = 'm-4 p-4 inline-block'
        image.style = f'transform: rotate({degree}deg)'
        image.height = 100
        image.width = 100
        image.degree = degree

        def straighten1(self, msg):
            self.style = f'transform: rotate(0deg)'

        def rotate_back1(self, msg):
            self.style = f'transform: rotate({self.degree}deg)'

        def no_rotate1(self, msg):
            self.degree = 0
            self.set_class('bg-red-200')

        image.on('mouseenter', straighten1)
        image.on('mouseleave', rotate_back1)
        image.on('click', no_rotate1)

    return wp

# initialize the demo
from  examples.basedemo import Demo
Demo ("html_comps6",html_comps6)
