# Justpy Tutorial demo result_test from docs/tutorial/page_events.md
import justpy as jp

js_string = """
a = 3;
b = 5;
c = a * b;
d = {r: c, appName: navigator.appName, appVersion: navigator.appVersion}

"""


async def page_ready(self, msg):
    jp.run_task(self.run_javascript(js_string))


async def result_ready(self, msg):
    msg.page.result_div.text = f"The result is: {msg.result}"


def result_test():
    wp = jp.WebPage()
    wp.on("page_ready", page_ready)
    wp.on("result_ready", result_ready)
    wp.result_div = jp.Div(text="Result will go here", classes="m-4 p-2 text-xl", a=wp)
    jp.Pre(text=js_string, a=wp, classes="m-2 p-2 border")
    return wp


# initialize the demo
from examples.basedemo import Demo

Demo("result_test", result_test)
