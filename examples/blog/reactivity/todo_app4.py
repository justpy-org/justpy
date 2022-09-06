# Justpy Tutorial demo todo_app4 from docs/blog/reactivity.md
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


# initialize the demo
from examples.basedemo import Demo

Demo("todo_app4", todo_app4)
