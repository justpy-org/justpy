# Justpy Tutorial demo download_test2 from docs/tutorial/uploading_files.md
import justpy as jp

def download_test2():
    wp = jp.WebPage()
    in1 = jp.Input(type='file', classes=jp.Styles.input_classes, a=wp, multiple=True, change=file_input)
    in1.file_div = jp.Div(a=wp)
    return wp

def file_input(self, msg):
    self.file_div.delete_components()
    for f in msg.files:
        jp.Div(text=f'{f.name} | {f.size} | {f.type} | {f.lastModified}', a=self.file_div, classes='font-mono m-1 p-2')


# initialize the demo
from examples.basedemo import Demo
Demo("download_test2", download_test2)
