# Justpy Tutorial demo download_test1 from docs/tutorial/uploading_files.md
import justpy as jp
from datetime import datetime

def change_link_text(self, msg):
    self.set_classes('text-yellow-500')

def download_test1():
    wp = jp.WebPage()
    download_link = jp.A(text='Download File', href='/create_file', download='text_file.txt', a=wp,
             classes='inline-block m-2 p-2 text-white bg-blue-500 text-2xl')
    download_link.on('click', change_link_text)
    return wp

@jp.SetRoute('/create_file')
def create_file():
    wp = jp.WebPage()
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    wp.html = f'This text file was generated on {now}'
    return wp

# initialize the demo
from examples.basedemo import Demo
Demo("download_test1", download_test1)
