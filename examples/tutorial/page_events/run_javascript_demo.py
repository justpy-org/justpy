# Justpy Tutorial demo run_javascript_demo from docs/tutorial/page_events.md
import justpy as jp

js_code = """
var a = 3;
var b = 5;
var c = a * b;
var d = {r: c, appName: navigator.appName, appVersion: navigator.appVersion};
(d)
"""

class JavaScriptDemo:
    """
    a demo for running JavaScript code
    """
    def __init__(self):
        """
        constructor
        """
        self.wp = jp.WebPage()
        self.wp.on("page_ready", self.page_ready)
        self.wp.on("result_ready", self.result_ready)
        self.result_div = jp.Div(text="Result will go here", classes="m-4 p-2 text-xl", a=self.wp)
        jp.Pre(text=js_code, a=self.wp, classes="m-2 p-2 border")
        

    async def page_ready(self, _msg):
        """
        callback when page is ready
        """
        jp.run_task(self.wp.run_javascript(js_code))


    async def result_ready(self, msg):
        """
        call back when result is ready
        """
        self.result_div.text = f"The result is: {msg.result}"


def run_javascript_demo():
    """
	show how to run javascript code
    """
    javascript_demo=JavaScriptDemo()
    return javascript_demo.wp

# initialize the demo
from examples.basedemo import Demo
Demo("run_javascript_demo", run_javascript_demo)
