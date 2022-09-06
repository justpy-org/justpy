# Justpy Tutorial demo event_demo1 from docs/tutorial/handling_events.md
import justpy as jp


def my_click1(self, msg):
    self.text = "I was clicked"


def event_demo1():
    wp = jp.WebPage()
    d = jp.Div(
        text="Not clicked yet",
        a=wp,
        classes="w-48 text-xl m-2 p-1 bg-blue-500 text-white",
    )
    d.on("click", my_click1)
    return wp


# initialize the demo
from examples.basedemo import Demo

Demo("event_demo1", event_demo1)
