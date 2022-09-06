# How to use the Select HTML Tag

The [select](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/select) tag needs to be used together with the option tag. In JustPy these correspond to Select and Option elements.

The program below creates a select element that whose value changes the background color of a Div.


```python
import justpy as jp


def change_color(self, msg):
    self.color_div.set_class(f'bg-{self.value}-600')


def select_comp_test():
    wp = jp.WebPage()
    colors = ['red', 'green', 'blue', 'pink', 'yellow', 'teal', 'purple']
    select = jp.Select(classes='w-32 text-xl m-4 p-2 bg-white  border rounded', a=wp, value='red',
                  change=change_color)
    for color in colors:
        select.add(jp.Option(value=color, text=color, classes=f'bg-{color}-600'))
    select.color_div = jp.Div(classes='bg-red-600 w-32 h-16 m-4',a=wp)
    return wp

jp.justpy(select_comp_test)
```
