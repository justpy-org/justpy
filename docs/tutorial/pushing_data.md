# Pushing Data to Web Pages



> The WebSocket API is an advanced technology that makes it possible to open a two-way interactive communication session between the user's browser and a server. With this API, you can send messages to a server and receive event-driven responses without having to poll the server for a reply.  
 <span>-</span> [Mozilla.org](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)

JustPy uses this technology in order allow the server to "push" data to web pages. 
Here is an example of a program that implements a clock. Every second, the server pushes the updated time to all open web pages.

## Clock
```python
import justpy as jp
import time
import asyncio

wp = jp.WebPage(delete_flag=False)
clock_div = jp.Span(text='Loading...', classes='text-5xl m-1 p-1 bg-gray-300 font-mono', a=wp)

async def clock_counter():
    while True:
        clock_div.text = time.strftime("%a, %d %b %Y, %H:%M:%S", time.localtime())
        jp.run_task(wp.update())
        await asyncio.sleep(1)

async def clock_init():
    jp.run_task(clock_counter())

async def clock_test():
    return wp

jp.justpy(clock_test, startup=clock_init)
```

The program first creates a WebPage instance called `wp` and `Span `instance called `clock_div` which is added to `wp`. Then we define a function called `clock_counter`. This function implements an infinite loop that changes the text of `clock_div` to the current time, updates `wp` and sleeps (in a non-blocking way) for one second. Every second, this loop is repeated. 

The `WebPage` instance `wp` is updated using the method `update()`. 
In order to understand what is happening, we need to make several distinctions.

1.	`wp` is an instance of the Python class `WebPage`
2.	`wp` can be the `WebPage` instance returned by several different requests, and in fact in our case, `wp` is always returned. All users get sent the same `wp`. This makes sense since the time is the same for everybody locally and we want to update it for everyone.
3.	However, each user has their own browser tab open. Also, the same user may have several browser tabs and windows open.
4.	There is therefore a one to many relation between `wp` and browser tabs and windows. `wp` may be rendered in many different tabs and windows (this is true for any instance of the class `WebPage`).
5.	Each time an instance of `WebPage` is rendered in a browser tab, JustPy creates a websocket connection (channel) between the tab and the sever. Therefore, an instance of `WebPage`, such as `wp`, may have many different websockets associated with it, one for every open tab that has `wp` rendered in it. JustPy keeps track of all open websockets
6.	The `update()` method when applied to the page, retrieves all open websockets associated with the specific WebPage instance and uses them to change the specific browser tab they connect with.  `wp.update()` updates all browser tabs that were rendered using `wp`.

In JustPy, all the above is done by the framework without any need for developer intervention. What you need to remember is simply this: If requests from any number of users were returned the same instance of `WebPage`, any update to this instance will change the content for all these users.

In our case, calling `wp.update()` will update all users since all requests result in wp being rendered (the function clock_test always returns `wp`).  

It is important to remember that the update method is a coroutine and must run in the asyncio loop that the server runs on and therefore user functions that await this method must also be coroutines and defined using async. Once `justpy` has been called, the loop the server is running on can be accessed via `JustPy.loop` in case you need to do something more complex. Also `asyncio.get_event_loop()` will work if you haven’t initiated other loops.

If the previous paragraph reads like gibberish to you, I apologize. Explaining Python's asyncio is beyond the scope of this tutorial. If you don't need to develop applications that scale, don't worry about it. Just use the examples as templates. 

Let's review the program in detail. First, we create `wp` and `clock_div` as global variables.
Then we define the coroutine `clock_counter`. It runs an infinite loop. The first line of the loop sets the text attribute of `clock_div` to be the current time and date (formatted to look a little nicer). The second line uses the JustPy helper utility `run_task` to run the coroutine update (it in fact schedules the coroutine to run as soon as possible). The third line causes `clock_counter` to suspend running for 1 second in a non-blocking way (all other coroutines can run while `clock_counter` sleeps).

Next, we define the coroutine `clock_init` (it could be just a regular function since it does not await any coroutine in this specific case). We will see in a second how this function will be used. All it does is run `clock_counter` once the server loop is up and running.

The last coroutine we define is `clock_test`. This is the function that handles all web requests. It just returns `wp` (it doesn’t need to be a coroutine in this case, it would work as a regular function since it does not await any coroutines). 

The last line is the call to `justpy`. The keyword parameter `startup` allows us to designate a function to run once the server loop has been initiated. We cannot designate `clock_counter` as the startup function because the server is locked until the startup function terminates and `clock_counter` never terminates. 

!!! note
    When a JustPy event handler finishes running and returns `None`, JustPy calls the `update` method of the WebPage instance in which the event occurred. That is the reason that content in browser tabs gets updated after events automatically. If you don't want the page to update, return `True` or anything except for `None`. 

## Collaborative Editor

Run the following program:

```python
import justpy as jp

wp = jp.QuasarPage(delete_flag=False)
editor = jp.QEditor(a=wp, kitchen_sink=True, height='94vh')

def joint_edit():
    return wp

jp.justpy(joint_edit)
```

This program allows joint editing of a document. Open several browser tabs or different browsers on your local machine and start editing the document. Any change you make in one browser tab, is reflected immediately in all others. 

The program uses the component QEditor. This JustPy component was built using the [Quasar QEditor Component](https://quasar.dev/vue-components/editor) (Quasar based JustPy components are described [here](/quasar_tutorial/introduction)).  
 
Since the program renders `wp`, the same WebPage instance to all pages, they all share the same QEditor instance. QEditor supports the input event and therefore the keys pressed are sent to the server which in turn sets the value of the QEditor instance (`editor` in our case) and then updates `wp` using the update method. Since `wp` is rendered in all browser tabs, they are all updated by JustPy.

## Simple Message Board

JustPy allows updating just specific elements on the page and not the whole page. Here is an implementation of a simple message board in which just the Div with the messages is shared and updated. Load pages in different browser tabs and see the functionality (a message sent from one tab will show up in all the others).

```python

import justpy as jp
from datetime import datetime

input_classes = 'm-2 bg-gray-200 font-mono appearance-none border-2 border-gray-200 rounded py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-red-500'
button_classes = 'm-2 p-2 text-red-700 bg-white hover:bg-red-200 hover:text-red-500 border focus:border-red-500 focus:outline-none'
message_classes = 'ml-4 p-2 text-lg bg-red-500 text-white overflow-auto font-mono rounded-lg'

shared_div = jp.Div(classes='m-2 h-1/2 border overflow-auto', delete_flag=False)
header = jp.Div(text='Simple Message Board', classes='bg-red-100 border-l-4 border-red-500 text-red-700 p-4 text-3xl', delete_flag=False)
button_icon = jp.Icon(icon='paper-plane', classes='text-2xl', delete_flag=False)
button_text = jp.Div(text='Send', classes='text-sm', delete_flag=False)
message_icon = jp.Icon(icon='comments', classes='text-2xl text-green-600', delete_flag=False)

def message_initialize():
    # Called once on startup
    d = jp.Div(a=shared_div, classes='flex m-2 border')
    time_stamp = jp.P(text=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), classes='text-xs ml-2 flex-shrink-0')
    p = jp.Pre(text='Welcome to the simple message board!', classes=message_classes)
    d.add(message_icon, time_stamp, p)

async def send_message(self, msg):
    if self.message.value:
        d = jp.Div(classes='flex m-2 border')
        time_stamp = jp.P(text=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), classes='text-xs ml-2 flex-shrink-0')
        p = jp.Pre(text=self.message.value, classes=message_classes)
        d.add(message_icon, time_stamp, p)
        shared_div.add_component(d, 0) 
        self.message.value = ''     # Clear message box after message is sent
        await shared_div.update()

def message_demo():
    wp = jp.WebPage()
    outer_div = jp.Div(classes='flex flex-col h-screen', a=wp)
    outer_div.add(header)
    d = jp.Div(classes='flex', a=outer_div)
    message = jp.Textarea(placeholder='Enter message here', a=d, classes=input_classes, debounce=500)
    send_button = jp.Button(a=d, click=send_message, classes=button_classes)
    send_button.add(button_icon, button_text)
    outer_div.add(shared_div)
    shared_div.add_page(wp)
    send_button.message = message
    return wp

jp.justpy(message_demo, startup=message_initialize)


```

At the top of the program we define combinations of Tailwind classes to make our UI a little nicer. This technique, of defining classes in a global manner can be used to create templates for JustPy applications. Next, we create global components that will be shared by all web pages. We introduce the `Icon` component which is used to display icons from the free [Fontawesome](https://fontawesome.com/) collection. 

Take a look at `message_demo`, the third function we define. All requests will be handled by this function. Each time it is called, it creates a new `WebPage` instance, `wp`. It adds a Div to it (`outer_div`). To this Div we add the predefined `header` Div and another Div which holds the message box and the button used to send messages. The button itself has two child components, the plane icon and the Div with the 'Send' text. We then add the shared message div to `outer_div`.

The next line, `shared_div.add_page(wp)`, is important. We need to add `wp` to the dictionary of pages `shared_div` is on. When we call the `update` method of `shared_div`, it will use this dictionary to update the appropriate browser tabs. 

!!! note
    JustPy does not keep track automatically of which page an element is on. This would have introduced a lot of overhead since often, as in our case also, an element is indirectly added to a page by being added to an element that has been or will be added to a page.

Let's take a closer look at `send_message`, the event handler that gets called when `send_button` is clicked. If the message box is not empty, the function creates a Div to which it adds an icon, a time stamp and the text of the message. It then adds the Div as the first element in `shared_div`.  It clears the message box and then awaits the `update` method of `shared_div`. Only `shared_div` will be updated in all the WebPages it is on. All the other elements on the page will not be updated.

Notice the `send_message` is a coroutine defined using the `async` keyword. This is the case because we need to await `update` from within `send_message`.  

## The Final Countdown

It is often required to call update several times within one event handler. For example, you may want to display a loading method while information is being retrieved from a database. Here is an exaggerated example:

```python
import justpy as jp
import asyncio

button_classes = 'm-2 p-2 text-red-700 bg-white hover:bg-red-200 hover:text-red-500 border focus:border-red-500 focus:outline-none'

async def count_down(self, msg):
    self.show = False
    if hasattr(msg.page, 'd'):
        msg.page.remove(msg.page.d)
    bomb_icon = jp.Icon(icon='bomb', classes='inline-block text-5xl ml-1 mt-1', a=msg.page)
    d = jp.Div(classes='text-center m-4 p-4 text-6xl text-red-600 bg-blue-500 faster', a=msg.page, animation=self.count_animation)
    msg.page.d = d
    for i in range(self.start_num, 0 , -1):
        d.text = str(i)
        await msg.page.update()
        await asyncio.sleep(1)
    d.text = 'Boom!'
    d.animation = 'zoomIn'
    d.set_classes('text-red-500 bg-white')
    bomb_icon.set_class('text-red-700')
    self.show = True

def count_test(request):
    start_num = int(request.query_params.get('num', 10))
    animation = request.query_params.get('animation', 'flip')
    wp = jp.WebPage()
    count_button = jp.Button(text='Start Countdown', classes=button_classes, a=wp, click=count_down)
    count_button.start_num = start_num
    count_button.count_animation = animation
    return wp

jp.justpy(count_test)
```

When you press the countdown button, a countdown begins and the page is updated every second. 

Every JustPy component has a `show` attribute. If it is set to `False`, the component is not rendered. The first line in the `count_down` event handler sets the button's `show` attribute to `False` and it is not rendered during the countdown (in this way the user cannot accidentally initiate another countdown while one is going on). Then we remove from the page the `Div` with the current countdown (we check if the `Div` is stored on the page to handle the first countdown ). We create the `Div` and add it to the page and also store a reference to it under the `d` attribute of the page so we can later have easy access to it for removal.

Then we loop from the countdown start number down to zero. In each loop iteration we set the text of `d`, update the page, and sleep 1 second using the asyncio library so as not to block countdowns on other pages. You can verify this by loading the page in different tabs or browsers.

After the countdown loop has ended, we set the text of `d` to 'Boom!', change some of `d`'s classes and make the button visible again. Remember, that if an event handler returns `None` as in our case (the default in Python when no return statement is encountered), the framework updates the page. Therefore when count_down terminates the page is updated again and that is why we see the button and 'Boom!'.

JustPy supports animation using the [animate.css](https://daneden.github.io/animate.css/) library. Just set the animation attribute of any component to a valid animation name. The default animation we use above is 'flip'. Try `http://127.0.0.1:8000/?animation=bounceIn` for example. You can test different animations using query parameters. You can set the animation speed by adding one of the classes slow, slower, fast, faster to the classes of the component. In this case we used 'faster' so that the animation takes less than 1 second. 

