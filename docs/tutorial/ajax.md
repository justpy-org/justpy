# Using Ajax instead of WebSockets

## Using Ajax to Handle Events
[Using Ajax to Handle Events live demo]({{demo_url}}/hello_test)

By default, JustPy uses [WebSockets](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API) as the communication protocol between the frontend and the backend. The advantage of WebSockets is that it allows the server to "push" data to the browser. 

There may be applications where either you do not want to or cannot use WebSockets (due to hosting limitations for example). In the `justpy` command if the `websockets` keyword argument is set to `False`, web pages will not attempt to establish a WebSockets connection with the server. Instead, events and pertinent data will be sent to the backend using Ajax. Your program will still be able to respond to UI events in the browser but will not be able to push data to browsers (you will not be able to implement chat like applications for example).

```python
import justpy as jp

def hello_test():
    wp = jp.WebPage()
    for i in range(10):
        jp.Hello(a=wp)
    return wp

jp.justpy(hello_test, websockets=False)
``` 

The program above will use Ajax to handle clicks on the Hello elements. You van verify this by using the debugging tools of your browser (in Chrome press CTRL+Shift+I and go to the "Network" tab)

!!! note
    In most cases, users will not notice any difference in the performance of the application if you use Ajax instead of WebSockets. If your hosting solution does not support WebSockets, give the Ajax option a try.

## Ajax Page Reload
[Ajax Page Reload live demo]({{demo_url}}/reload_demo)

There may be cases where you do not want to use WebSockets but still want the content on the users' pages to refresh periodically. This is done in JustPy by setting the `reload_interval` attribute of the page to the number of seconds between each reload. The page does not reload in the strictest sense of that word, it just refreshes its content using an Ajax call to the server as you would do in a single page application. 

For example, this feature is useful for implementing dashboards. Below is a very simple dashboard that includes just one element that is updated by a background task every second while users' browser tabs poll the updated content every 2.5 seconds. 

```python
import justpy as jp
import asyncio

wp = jp.WebPage(delete_flag=False)
wp.reload_interval = 2.5
count_div = jp.Div(a=wp, classes='text-center m-4 p-4 text-white bg-blue-500', style='font-size: 200px')

async def increment_counter(start):
    count_div.counter = start
    while True:
        count_div.counter += 1
        count_div.text = str(count_div.counter)
        await asyncio.sleep(1)

def start_counting():
    jp.run_task(increment_counter(500))

def reload_demo():
    return wp

jp.justpy(reload_demo, startup=start_counting, websockets=False)
```


