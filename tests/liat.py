import gzip

fn = 'd:/ppmi.feb.1.2015.vcf.gz'

def read_lines(start, n):
    with gzip.open(fn, 'rt') as f:
        for i in range(start + n):
            l = f.readline()
            if i>start:
                print(l)


def create_file(start, n):
    f_out = open("d:/liat1.txt", "w")
    with gzip.open(fn, 'rt') as f:
        for i in range(start + n):
            l = f.readline()
            if i>start:
                print(i, l)
                f_out.write(l)
    f_out.close()

# read_lines(0, 100)
# create_file(0, 10000)

import justpy as jp

corner_classes = 'p-3 absolute bg-gray-200 '

class MyDiv(jp.Div):

    def model_update(self):
        # [wp, 'text-data'] for example
        if self.model[0].data[self.model[1]]:
            self.text = (str(self.model[0].data[self.model[1]]) + ' ')*self.repeat
        else:
            self.text = self.initial_text


import random

def model_demo():
    wp = jp.QuasarPage()
    p = jp.parse_html('<div><span>hello</span></div>', a=wp)
    for i in range(1,10):
        jp.QBtn(label=f'Button {i}', a=wp) #, click='self.label = "clicked"')
    for i in range (1,111):
        jp.Div(a=wp, text=f'Div {i}')
    # random.shuffle(wp.components)
    return wp

jp.justpy(model_demo)


#"msg.page.display_url=self.value;msg.page.title=self.value "