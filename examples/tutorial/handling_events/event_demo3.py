# Justpy Tutorial demo event_demo3 from docs/tutorial/handling_events.md
import justpy as jp


def my_click3(self, msg):
    print(msg)
    self.text = "I was clicked"


def event_demo3():
    wp = jp.WebPage()
    wp.debug = True
    d = jp.Div(
        text="Not clicked yet",
        a=wp,
        classes="w-48 text-xl m-2 p-1 bg-blue-500 text-white",
    )
    d.on("click", my_click3)
    d.additional_properties = [
        "screenX",
        "pageY",
        "altKey",
        "which",
        "movementX",
        "button",
        "buttons",
    ]
    return wp


# initialize the demo
from examples.basedemo import Demo

Demo("event_demo3", event_demo3)
