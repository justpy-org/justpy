# Using Markdown

The `Markdown` component allows adding [markdown](https://www.markdownguide.org/basic-syntax/) formatted text to a web page.

The component uses [Python-Markdown](https://python-markdown.github.io/) and is only available if Python-Markdown is [installed](https://python-markdown.github.io/install/).

The component has three attributes:

- `markdown` -  The markdown annotated text
- `extensions` - A list of [extensions](https://python-markdown.github.io/extensions/) to use
- `all_extensions` -  A boolean value that defaults to `True` in which case all extensions included with  Python-Markdown are used. If `extensions` is not empty, its value is used instead of all extensions  

# WebPage `write` Method

You can use the `write` method to put markdown directly on a page. The method accepts one argument, a markdown formatted string. The method returns the component that is added to the page.

```python
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


jp.justpy(md_test)
```