# Comparing Vue.js to JustPy

# Example from Vue Guide
https://vuejs.org/v2/guide/components.html#Base-Example

```python
import justpy as jp

class ButtonCounter(jp.Button):

    def __init__(self, **kwargs):
        self.count = 0
        super().__init__(**kwargs)
        self.on('click', self.button_clicked)

    def button_clicked(self, msg):
        self.count += 1

    def react1(self, data):
        self.text = f'You clicked me {self.count} times.'


async def button_counter_demo_c():
    wp = jp.WebPage(tailwind=False)
    for i in range(5):
        ButtonCounter(a=wp, count=i, style='margin: 10px')
    return wp

jp.justpy(button_counter_demo_c)
```

# Vue video example

```python
import justpy as jp

products = [
            {'id': 1, 'quantity': 1, 'name': 'Compass'},
            {'id': 2, 'quantity': 0, 'name': 'Jacket'},
            {'id': 3, 'quantity': 5, 'name': 'Hiking Socks'},
            {'id': 4, 'quantity': 2, 'name': 'Suntan Lotion'},
            ]


class Products(jp.Div):

    def __init__(self, **kwargs):
        self.products = products
        super().__init__(**kwargs)
        self.ul = jp.Ul(a=self)
        self.total_inventory = jp.H2(text='Totals', a=self)

    def total_products(self):
        total = 0
        for product in self.products:
            total += product["quantity"]
        return total

    def react2(self, data):
        self.ul.delete_components()
        for product in self.products:
            item = jp.Li(a=self.ul)
            jp.Input(type='number', product=product, a=item, value=product["quantity"], input='self.product["quantity"] = self.value')
            jp.Span(text=f'{product["quantity"]} {product["name"]}', a=item, style='margin-left: 10px')
            if product["quantity"] == 0:
                jp.Span(text=' - OUT OF STOCK', a=item)
            jp.Button(text='Add', a=item, product=product, click='self.product["quantity"] += 1', style='margin-left: 10px')
        self.total_inventory.text = f'Total Inventory: {self.total_products()}'


def product_app_c():
    wp = jp.WebPage(tailwind=False)
    Products(a=wp)
    return wp

jp.justpy(product_app_c)

```
## Todo list example

```python
import justpy as jp


class TodoList(jp.Div):

    def __init__(self, **kwargs):
        self.todos = []
        super().__init__(**kwargs)
        self.ol = jp.Ol(a=self)
        self.task = jp.Input(placeholder='Enter task', a=self)
        jp.Button(text='Add Task', a=self, click=self.add_task, style='margin-left: 10px')

    def add_task(self, msg):
        self.todos.append(self.task.value)
        self.task.value = ''

    def react3(self, data):
        self.ol.delete_components()
        for todo in self.todos:
            jp.Li(text=todo, a=self.ol)


def todo_app():
    wp = jp.WebPage(tailwind=False)
    TodoList(a=wp, todos=['Buy groceries', 'Learn JustPy', 'Do errands'])
    return wp

jp.justpy(todo_app)
```


First things first: JustPY uses Vue on the front end. Without Vue there is no JustPy.

It is important to understand how JustPy uses Vue to understand the differences between the two. In JustPy, web pages as well as HTML components are represented as instances of classes. The HTML div element is represented by the JustPy class Div.

You add a div to web page in JustPY by adding a Div instance to a WebPage instance like so:

```python
import justpy as jp

wp = jp.WebPage()
my_div = jp.Div(text='hello')
wp.add(my_div)

```

All JustPy elements have a method called `convert_object_to_dict` that do just that.

```python
import justpy as jp

my_div = jp.Div(text='hello')
my_div.add(jp.Span(text='span text', style='margin: 5px'))
print(my_div.convert_object_to_dict())
```

would give the following result:

```python
{'attrs': {}, 'id': None, 'vue_type': 'html_component', 'show': True, 'events': [], 'event_modifiers': {}, 'classes': '', 'style': '', 'set_focus': False, 'html_tag': 'div', 'class_name': 'Div', 'event_propagation': True, 'inner_html': '', 'animation': False, 'debug': False, 'directives': {}, 'scoped_slots': {}, 'object_props': [{'attrs': {}, 'id': None, 'vue_type': 'html_component', 'show': True, 'events': [], 'event_modifiers': {}, 'classes': '', 'style': 'margin: 5px', 'set_focus': False, 'html_tag': 'span', 'class_name': 'Span', 'event_propagation': True, 'inner_html': '', 'animation': False, 'debug': False, 'directives': {}, 'scoped_slots': {}, 'object_props': [], 'text': 'span text'}], 'text': 'hello'}

```

This dictionary is converted to JSON and sent to the browser. It is then used as the props for the Vue component that renders the element on the page.

To recap, JustPy creates a JSON object representing the page, and that object is fed into the Vue app which renders the page.

Creating the dictionary on the server side is very cheap computationally. All the rendering heavy lifting is done by Vue. If as a consequence of an event handler a page changes, a new dictionary is sent to the page and again fed to the Vue app which re-renders the required elements.

When

JustPy renders a page in a browser tab using the following steps:
1) For all instances on the page, a Python dictionary that describes their attributes is generated. T


explain how vue is used

This comparison is meant to help people familiar with Vue understand JustPy better.

JustPy is not a backend or frontend framework. When working with JustPy there is no distinction between the backend and the frontend.
The reason you would use JustPy instead of Vue is if you are interested working predominantly in Python

This comparison is not meant to convince you to use one or the other

In vue there is distinction between html and javascript (render function means you don't need html). In JustPY it is all python (but you can use html if you like parse_html).

Main difference is reactivity. How to solve this? Example with react function. But how to automate. Show how to make reactive list based on object.

You need to do this with components. A component that is a list. You can make it reactive. Show example of for without component and then with component.

## List Rendering (v-for)

The Vue.js examples are [here](https://vuejs.org/v2/guide/list.html).

### Example of rendering a simple list

 ```python
import justpy as jp

def for_example1():
    wp = jp.WebPage(tailwind=False)  
    items = [{'message': 'Foo'},
             {'message': 'Bar'}]
    ul = jp.Ul(a=wp)
    for item in items:
        jp.Li(text=f'{item["message"]}', a=ul)
    return wp

jp.justpy(for_example1)
```

### Second example of rendering a list with index

```python
import justpy as jp

def for_example2():
    wp = jp.WebPage(tailwind=False)
    ul = jp.Ul(a=wp)
    ul.items = [{'message': 'Foo'},
             {'message': 'Bar'}]
    ul.parent_message = 'Parent'
    for index, item in enumerate(ul.items):
        jp.Li(text=f'{ul.parent_message}-{index}-{item["message"]}', a=ul)
    return wp

jp.justpy(for_example2)
```
Note that the HTML elements are Python class instances and therefore we can assign values to their attributes.


### Rendering an object

https://vuejs.org/v2/guide/list.html#v-for-with-an-Object
Rendering keys and values of an object:

```python
import justpy as jp


def for_example3():
    wp = jp.WebPage(tailwind=False)
    ul = jp.Ul(a=wp)
    object = {
      'title': 'How to do lists in Vue',
      'author': 'Jane Doe',
      'publishedAt': '2016-04-10'
    }
    for name, value in object.items():
        jp.Li(text=f'{name}: {value}', a=ul)
    return wp

jp.justpy(for_example3)

```
### Rendering an object with index


```python
import justpy as jp


def for_example4():
    wp = jp.WebPage(tailwind=False)
    object = {
      'title': 'How to do lists in Vue',
      'author': 'Jane Doe',
      'publishedAt': '2016-04-10'
    }
    for index, (name, value) in enumerate(object.items()):
        jp.Div(text=f'{index}. {name}: {value}', a=wp)
    return wp

jp.justpy(for_example4)

```

### Displaying Filtered/Sorted Results
https://vuejs.org/v2/guide/list.html#Displaying-Filtered-Sorted-Results



### Reactivity

JustPy is not reactive in the sense that if you change the value of an object, the rendered view will change automatically.
This manifests itself when items are added or deleted, not when their property changes like text



## x-for

```angular2html
<template x-for="(item, index) in items" :key="index">
    <!-- You can also reference "index" inside the iteration if you need. -->
    <div x-text="index"></div>
</template>
```

```python
from justpy import WebPage, Div, SetRoute

SetRoute('/for')
def for_example5():
    wp = WebPage()
    items = ['car', 'plane', 'train']
    for index, item in enumerate(items):
        Div(text=f'Item: {item}, Index: {index}', a=wp)
    return wp
```

Only applicable part:
```python
items = ['car', 'plane', 'train']
for index, item in enumerate(items):
    Div(text=f'Item: {item}, Index: {index}', a=some_container)
```

Nesting:

```python
from justpy import WebPage, Div, SetRoute

SetRoute('/nested_for')
def for_example6():
    wp = WebPage()
    items = {'car': ['Ford', 'Toyota', 'GM'], 'plane': ['Boeing', 'Airbus'], 'train': ['Amtrak', 'NJ Transit']}
    for index, item in enumerate(items):
        for sub_item in items[item]:
            Div(text=f'Item: {item}, Sub Item: {sub_item}', a=wp)
    return wp
```


## x-data vs class

https://github.com/alpinejs/alpine#use

```python
import justpy as jp

class SimpleDropdown(jp.Div):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        b = jp.Button(text='Open Dropdown', a=self, click='self.u.show = not self.u.show')
        b.u = jp.Ul(a=self, text='Drop Down Body', show=False, click__out='self.show = False')

def alpine_test():
    wp =jp.WebPage()
    SimpleDropdown(a=wp)
    return wp

jp.justpy(alpine_test)
```
