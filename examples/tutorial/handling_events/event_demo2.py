# Justpy Tutorial demo event_demo2 from docs/tutorial/handling_events.md
import justpy as jp


def my_click2(self, msg):
    self.text = "I was clicked"
    print(msg.event_type)
    print(msg["event_type"])
    print(msg)


def event_demo2():
    wp = jp.WebPage()
    d = jp.P(
        text="Not clicked yet", a=wp, classes="text-xl m-2 p-2 bg-blue-500 text-white"
    )
    d.on("click", my_click2)
    return wp


# initialize the demo
from examples.basedemo import Demo

Demo("event_demo2", event_demo2)
