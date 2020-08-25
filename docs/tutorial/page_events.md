# Page Events

As of version 0.1.2 pages support three events:

* click - fires when page is clicked
* [visibilitychange](https://developer.mozilla.org/en-US/docs/Web/API/Document/visibilitychange_event) - fires when the page gains or loses visibility 
* page_ready - fires after a page is ready with an established websocket connection

Added in version 0.1.3:

* result_ready: fires when a result from the [`run_javascript`](/reference/webpage/#async-def-run_javascriptself-javascript_string-request_id-sendtrue) method is available.

In the first example below, `page_ready` is used to load a page with 3,000 Div elements in a staggered manner in order to improve the user experience. 

Try the '/stagger' route and see how it compares to the default.


```python
import justpy as jp
import asyncio


async def page_ready_div(self, msg):
    for i in range(1,3001):
        jp.Div(text=f'Div {i}', a=self.d, classes='border m-2 p-2 text-xs')
        if i % 100 == 0:
            await self.update()
            await asyncio.sleep(0.25)


@jp.SetRoute('/stagger')
def loading_page_stagger_test():
    wp = jp.WebPage()
    wp.on('page_ready', page_ready_div)
    wp.d = jp.Div(classes='flex flex-wrap', a=wp)
    return wp


def loading_page_no_stagger():
    wp = jp.WebPage()
    wp.d = jp.Div(classes='flex flex-wrap', a=wp)
    for i in range(1, 3001):
        jp.Div(text=f'Div {i}', a=wp.d, classes='border m-2 p-2 text-xs')
    return wp

jp.justpy(loading_page_no_stagger)
```

In the following example the result of running JavaScript in the browser is obtained:

```python
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
    msg.page.result_div.text = f'The result is: {msg.result}'

def result_test():
    wp = jp.WebPage()
    wp.on('page_ready', page_ready)
    wp.on('result_ready', result_ready)
    wp.result_div = jp.Div(text='Result will go here', classes='m-4 p-2 text-xl', a=wp)
    jp.Pre(text=js_string, a=wp, classes='m-2 p-2 border')
    return wp

jp.justpy(result_test)
```