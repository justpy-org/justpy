# Justpy Tutorial demo out_test from docs/tutorial/handling_events.md
import justpy as jp


def click_out(self, msg):
    self.text = "click out"
    self.set_classes("text-blue-500")


def click_in(self, msg):
    self.text = "click in"
    self.set_classes("text-red-500")


def out_test():
    wp = jp.WebPage()
    for i in range(4):
        d = jp.Div(text=f"{i}) Div", a=wp, classes="m-4 p-4 text-xl border w-32")
        d.on("click__out", click_out)
        d.on("click", click_in)
    return wp


# initialize the demo
from examples.basedemo import Demo

Demo("out_test", out_test)
