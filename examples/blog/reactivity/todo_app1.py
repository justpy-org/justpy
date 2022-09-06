# Justpy Tutorial demo todo_app1 from docs/blog/reactivity.md
import justpy as jp

todos = ["Go shopping", "Learn JustPy", "Do errands"]


def todo_app1():
    wp = jp.WebPage(tailwind=False)
    ol = jp.Ol(a=wp)
    for todo in todos:
        jp.Li(text=todo, a=ol)
    return wp


# initialize the demo
from examples.basedemo import Demo

Demo("todo_app1", todo_app1)
