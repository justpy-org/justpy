# Justpy Tutorial demo todo_app2 from docs/blog/reactivity.md
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


# initialize the demo
from examples.basedemo import Demo

Demo("todo_app2", todo_app2)
