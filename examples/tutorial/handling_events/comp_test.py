# Justpy Tutorial demo comp_test from docs/tutorial/handling_events.md
import justpy as jp


def comp_test():
    wp = jp.WebPage()
    d = jp.Div(
        text="hello1",
        click='self.text="clicked"',
        mouseenter='self.text="entered"; self.set_class("text-5xl"); msg.page.add(Div(text=f"{len(msg.page)} Additional Div"))',
        mouseleave='self.text="left"; self.set_class("text-xl")',
        classes="text-2xl border p-2 m-2",
        a=wp,
    )
    d = jp.Div(
        text="hello2",
        click='self.text="clicked"',
        mouseenter='self.text="entered"',
        classes="text-2xl border p-2 m-2",
        a=wp,
    )
    d = jp.Div(
        text="hello3",
        click='self.text="clicked"',
        mouseenter='self.text="entered"',
        classes="text-2xl border p-2 m-2",
        a=wp,
    )
    return wp


# initialize the demo
from examples.basedemo import Demo

Demo("comp_test", comp_test)
