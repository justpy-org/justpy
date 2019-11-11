import justpy as jp


def straighten(self, msg):
    self.style = f'transform: rotate(0deg)'

def rotate_back(self, msg):
    self.style = f'transform: rotate({self.degree}deg)'

def no_rotate(self, msg):
    self.degree = 0
    self.set_class('bg-red-200')


def html_comps():
    wp = jp.WebPage()
    for degree in range(0, 361, 10):
        jp.Img(src='https://www.python.org/static/community_logos/python-powered-h-140x182.png', a=wp,
                classes='m-4 p-4 inline-block', style=f'transform: rotate({degree}deg)', height=100, width=100,
                degree=degree, mouseenter=straighten, mouseleave=rotate_back, click=no_rotate)
    return wp

jp.justpy(html_comps)




# f = jp.Iframe(a=wp, src="https://www.openstreetmap.org/export/embed.html?bbox=-0.004017949104309083%2C51.47612752641776%2C0.00030577182769775396%2C51.478569861898606&layer=mapnik", width="300", height="200")
# div, p, span, ul, li, nav, button, input, iframe, a, img, form
# i, strong
# path contenteditable='true', f'Span #{j+1} in Div #{i+1}'