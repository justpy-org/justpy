# Reactivity in JustPy

## Introduction

A web framework is [reactive](https://lihautan.com/reactivity-in-web-frameworks-the-when/) if it updates the view whenever the some underlying data in the application changes. In practice, what this means for developers is that they do not need to manipulate the DOM when the state of the application changes. The framework takes care of that.

Is JustPy reactive? The answer is yes and this article explains how to use JustPY in a reactive way.

## Static HTML

Before delving into reactive examples, let's see how JustPy can also be used to generate static html that is not reactive.

The following program takes a Python list and generates HTML from it:

```python
import justpy as jp

todos = ["Go shopping", "Learn JustPy", "Do errands"]

def todo_app1():
    wp = jp.WebPage(tailwind=False)
    ol = jp.Ol(a=wp)
    for todo in todos:
        jp.Li(text=todo, a=ol)
    return wp

jp.justpy(todo_app1)

```

If you change the `todos` list in your code, nothing will change in your open browser page. To see change, you need to re-run the program and reload the page.

## First Step to Reactivity

When we use a reactive frontend framework like Vue or React, we can go to the browser console, change a variable, and see the view change in reaction to the variable changing. We cannot do that in JustPy because JustPy programs are Python programs and run on the server, not in the browser.

We can only demonstrate reactivity from within the program. In the example below we let the user add an item to `todos` and change the view.

```python
import justpy as jp


def todo_app2():
    todos = ["Buy groceries", "Learn JustPy", "Do errands"]
    wp = jp.WebPage(tailwind=False)
    ol = jp.Ol(a=wp)
    for todo in todos:
        jp.Li(text=todo, a=ol)
    task = jp.Input(placeholder="Enter task", a=wp)

    def add_task(self, msg):
        todos.append(task.value)
        task.value = ""
        ol.delete_components()
        for todo in todos:
            jp.Li(text=todo, a=ol)

    jp.Button(text="Add Task", a=wp, click=add_task, style="margin-left: 10px")

    return wp

jp.justpy(todo_app2)
```

When the Add Task button is clicked, the add_task event handler deletes the children of `ol` and recreates them based on the new value of `todos`. On the front end, Vue will update the view based on the new values (the WebPage is converted into a Python dictionary which is fed into Vue).

This is still not the full reactivity we are looking for. Yes, the view changes and we are not manipulating the DOM on the frontend, but we are changing instances of objects that represent the DOM on the server side.

To get to full reactivity we need to create our own components.

## Full Reactivity

In the example below we define a component called `TodoList`. JustPy components are Python classes that inherit from more basic components. TodoList inherits from `Ol` which is the JustPy class that represents the HTML `ol` tag.

```python
import justpy as jp


class TodoList(jp.Ol):

    def __init__(self, **kwargs):
        self.todos = []
        super().__init__(**kwargs)

    def react(self, data):
        self.delete_components()
        for todo in self.todos:
            jp.Li(text=todo, a=self)


def todo_app3():
    wp = jp.WebPage(tailwind=False)
    todo_list = TodoList(a=wp, todos=["Buy groceries", "Learn JustPy", "Do errands"])
    task = jp.Input(placeholder="Enter task", a=wp)

    def add_task(self, msg):
        todo_list.todos.append(task.value)
        task.value = ""

    jp.Button(text="Add Task", a=wp, click=add_task, style="margin-left: 10px")

    return wp

jp.justpy(todo_app3)
```

In the component we only modify two methods and inherit all other methods. The `__init__` method is modified to give a default value to the `todos` attribute of the component in case it is not specified as a keyword argument when an instance is created. The second method we modify is the `react` method. This method is run automatically by the framework just before the component is rendered on the server side. Rendering on the server side means converting the object into a Python dictionary that is sent to the frontend in JSON format.

Any changes the event handlers or background task have made to attributes of the object, will be reflected on the page. Therefore, all the `add_task` event handler has to do is modify the `todos `attribute of `todo_list` for the result to be reflected on the page. This is full reactivity.

You can argue that we are sort of manipulating the DOM inside the `react` method. However, that is equivalent to saying that we are manipulating the DOM inside the template section of a Vue component. We need to define the HTML of the component at least once somewhere and that is done in the `react` method.

## Extending TodoList

In the example below the TodoList component is extended to include the input field and the button. They are added to the component in `__init__` and not `react` as they do not need to change when `todos` change.

```python
import justpy as jp


class TodoList(jp.Div):

    def __init__(self, **kwargs):
        self.todos = []
        super().__init__(**kwargs)
        self.ol = jp.Ol(a=self)
        self.task = jp.Input(placeholder="Enter task", a=self)
        jp.Button(
            text="Add Task", a=self, click=self.add_task, style="margin-left: 10px"
        )

    def add_task(self, msg):
        self.todos.append(self.task.value)
        self.task.value = ""

    def react(self, data):
        self.ol.delete_components()
        for todo in self.todos:
            jp.Li(text=todo, a=self.ol)


def todo_app4():
    wp = jp.WebPage(tailwind=False)
    TodoList(a=wp, todos=["Buy groceries", "Learn JustPy", "Do errands"])
    return wp

jp.justpy(todo_app4)
```
