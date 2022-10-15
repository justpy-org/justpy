# Justpy Tutorial demo md_test from docs/tutorial/markdown.md
import justpy as jp



def add_item_to_list(self, msg):
    wp = msg.page
    wp.list_item_num += 1
    wp.md.markdown = f'{wp.md.markdown}\n* *Item* **{wp.list_item_num}**'


def md_test():
    wp = jp.WebPage()
    jp.Button(text='Add Item to List', classes=jp.Styles.button_bordered + ' m-4 p-2', click=add_item_to_list, a=wp)
    wp.md = jp.Markdown(markdown='# My List', a=wp, classes='m-2')
    wp.list_item_num = 0
    return wp


@jp.SetRoute('/hello')
def md_write_test():
    wp = jp.WebPage()
    wp.write('# Hello world!')
    return wp


# initialize the demo
from  examples.basedemo import Demo
Demo ("md_test",md_test)
