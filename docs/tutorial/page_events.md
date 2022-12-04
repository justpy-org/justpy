# Page Events

As of version 0.1.2 pages support three events:

* click - fires when page is clicked
* [visibilitychange](https://developer.mozilla.org/en-US/docs/Web/API/Document/visibilitychange_event) - fires when the page gains or loses visibility
* page_ready - fires after a page is ready with an established websocket connection

Added in version 0.1.3:

* result_ready: fires when a result from the [`run_javascript`](/reference/webpage/#async-def-run_javascriptself-javascript_string-request_id-sendtrue) method is available.

In the first example below, `page_ready` is used to load a page with 3,000 Div elements in a staggered manner in order to improve the user experience.

Click the button to toggle between staggered and default to compare them. You can increase the number of divs on page by increasing/decreasing the slider by a factor of 200

### loading hundreds of div elements in a staggered manner
[loading hundreds of div elements in a staggered manner live demo]({{demo_url}}/loading_page_staggered_demo)

```python
import justpy as jp
import asyncio
import time

class StaggerDemo:
    """
    Demo for staggered or no staggered loading
    """
    
    def __init__(self,div_count:int=3000,staggered:bool=False):
        """
        constructor
        """
        self.div_count=div_count
        self.staggered=staggered
        self.wp = jp.QuasarPage(tailwind=True, title="Staggered Loading demo")
        self.top_div=jp.Div(a=self.wp)
        # QSlider seems to need some room above it
        self.slider_label=jp.Span(
            text="Number of divs to load:",a=self.top_div)
        self.slider_top_margin_div=jp.Div(a=self.top_div,classes="h-10")
        margins="margin-left: 10px;margin-right: 10px;"
        jp.QSlider(a=self.top_div,  
                   classes="w-64",
                   style=margins,
                   min=200,
                   value=self.div_count,
                   max=1000,
                   label=True,
                   label_always=True,
                   markers=True,
                   step=200,
                   snap=True,
                   color="blue",
                   change=self.on_change_div_count)
        self.timer_span=jp.Span(text=f'', a=self.top_div,style=margins)
        self.button=jp.Button(text="?", a=self.top_div, click=self.on_toggle_mode, classes=jp.Styles.button_simple)
        self.main_div = jp.Div(a=self.wp,classes="flex flex-wrap")
        self.set_mode()       
        
    def set_mode(self):
        """
        set the button text according to the staggered mode
        """
        staggered_text="" if self.staggered else "Non"
        self.mode=f"{staggered_text } staggered loading"
        button_text=f"Try {self.mode}" 
        self.button.text=button_text
        
    async def on_change_div_count(self,msg):
        """
        change the div count
        """
        self.div_count=int(msg["value"])
        pass
         
    async def on_toggle_mode(self,_msg={}):
        """
        show the different staggered behavior modes
        """
        # quickly remove main div content
        self.main_div.delete_components()
        await self.wp.update()
       
        # populate according to staggered mode
        await self.populate()
        # toggle the staggered mode
        self.staggered=not self.staggered
        # set my button text accordingly
        self.set_mode()
        await self.wp.update()
        
    async def populate(self, _msg={}):
        """
        populate the screen with self.div_count divs
        in a staggered/non staggered way depending on the self.stagger state
        """
        starttime = time.time()
        for i in range(self.div_count):
            jp.Div(text=f"Div {i+1:04d}", a=self.main_div, classes="border m-2 p-2 text-xs")
            if self.staggered:
                if i % 100 == 0:
                    await self.wp.update()
                    await asyncio.sleep(0.25)
        elapsed = time.time() - starttime
        self.timer_span.text=f"{self.mode} of {self.div_count} divs took {elapsed:5.3f} s"
    
async def loading_page_staggered_demo():
    """
    show staggered/non staggered loading
    """
    stagger_demo=StaggerDemo(400)
    await stagger_demo.on_toggle_mode()
    return stagger_demo.wp    

jp.justpy(loading_page_staggered_demo)
```

In the following example the result of running JavaScript in the browser is obtained:

### run_javascript example
[run javascript example live demo]({{demo_url}}/run_javascript_demo)


```python
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
    
jp.justpy(run_javascript_demo)
```
