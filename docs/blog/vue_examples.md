# JustPy Implementation of Vue.js Examples

## Base Example from Vue Guide

[Example in Vue.js Guide](https://vuejs.org/v2/guide/components.html#Base-Example)

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


async def button_counter_demo():
    wp = jp.WebPage(tailwind=False)
    for i in range(5):
        ButtonCounter(a=wp, count=i, style='margin: 10px')
    return wp

jp.justpy(button_counter_demo)
```

## Vue.js Introductory Video Example

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


def product_app():
    wp = jp.WebPage(tailwind=False)
    Products(a=wp)
    return wp

jp.justpy(product_app)

```

## Todo List Example

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


def todo_app_vue1():
    wp = jp.WebPage(tailwind=False)
    TodoList(a=wp, todos=['Buy groceries', 'Learn JustPy', 'Do errands'])
    return wp

jp.justpy(todo_app_vue1)
```
