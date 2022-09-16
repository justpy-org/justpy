# Handling Events
In this part of the tutorial you will learn how to deal with user generated events such as a mouse click. JustPy deals with such events by binding a function to an event. When the event occurs, the function is executed. Please run the following program and click on 'Not clicked yet':

## event handling demo
```python
import justpy as jp

def my_click1(self, msg):
    self.text = 'I was clicked'

def event_demo1():
    wp = jp.WebPage()
    d = jp.Div(text='Not clicked yet', a=wp, classes='w-48 text-xl m-2 p-1 bg-blue-500 text-white')
    d.on('click', my_click1)
    return wp

jp.justpy(event_demo1)
```

In `event_demo`, we first create a web page. Then we create a [Div](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/div) element named `d` whose content is the string "Not clicked yet" and add it to the page (we also add some Tailwind classes for formatting). Then, using the `on` method, we bind the function `my_click`, which we defined earlier, to the click event and return the page. When the the element on the page is clicked, JustPy runs the function `my_click`.

!!! info
    Functions that handle events are called "event handlers". `my_click` is an example of such a function.

!!! warning
    In JustPy, event handlers **must** have two arguments.

The first (I recommend calling it `self`), is the object which generated the event. It is an instance of one of the component classes. In the example above it is `d`, an instance of the class `Div`. The second parameter (I recommend calling it `msg`) is a [dictionary](https://github.com/mewwts/addict "addict is a Python module that gives you dictionaries whose values are both gettable and settable using attributes, in addition to standard item-syntax") that contains information about the event. The items in this dictionary can also be accessed using attribute (dot) notation. To get the event type for example we could write either  `msg['event_type']` or `msg.event_type`.

In the program below I have added some print commands to the `my_click` function. Run it and see what is printed to the console.

## event handling demo with printing to console
```python
import justpy as jp

def my_click2(self, msg):
    self.text = 'I was clicked'
    print(msg.event_type)
    print(msg['event_type'])
    print(msg)

def event_demo2():
    wp = jp.WebPage()
    d = jp.P(text='Not clicked yet', a=wp, classes='text-xl m-2 p-2 bg-blue-500 text-white')
    d.on('click', my_click2)
    return wp

jp.justpy(event_demo2)
```

## Additional Event Properties

JustPy does not pass all the JavaScript event properties by default since in most cases they are not needed. If you need additional properties from the JavasScript event, use the `additional_properties` attribute. In the example below, more fields are added to `msg`.

```python
import justpy as jp

def my_click3(self, msg):
    print(msg)
    self.text = 'I was clicked'

def event_demo3():
    wp = jp.WebPage()
    wp.debug = True
    d = jp.Div(text='Not clicked yet', a=wp, classes='w-48 text-xl m-2 p-1 bg-blue-500 text-white')
    d.on('click', my_click3)
    d.additional_properties =['screenX', 'pageY','altKey','which','movementX','button', 'buttons']
    return wp

jp.justpy(event_demo3)
```

## Multiple Events

The same element can handle multiple events. Run the following and move the mouse in and out of the element on the page. Click the element also.

```python
import justpy as jp

def my_click4(self, msg):
    self.text = 'I was clicked'
    self.set_class('bg-blue-500')

def my_mouseenter(self, msg):
    self.text = 'Mouse entered'
    self.set_class('bg-red-500')

def my_mouseleave(self, msg):
    self.text = 'Mouse left'
    self.set_class('bg-teal-500')


def event_demo4():
    wp = jp.WebPage()
    d = jp.Div(text='Not clicked yet', a=wp, classes='w-64 text-2xl m-2 p-2 bg-blue-500 text-white',
             click=my_click4, mouseenter=my_mouseenter, mouseleave=my_mouseleave)
    return wp

jp.justpy(event_demo4)
```

 In the example above, there are three event handlers, one each for the `click`, `mouseenter` and `mouseleave` events. All three are bound to the same element, `d`.

 Another way of binding event handlers is demonstrated here. Instead of using the `on` method, you can bind an event handler using a keyword argument that corresponds to the name of the event. In addition to `click` (or some other event name) you can also use `onclick` or, `on_click`. All three options work in the same way.

The above example also introduces the `set_class` method. This method "knows" which Tailwind classes logically cannot apply together (for example, text color can't be both red and blue at the same time) and removes the appropriate classes while adding the class provided as parameter. In the case above, the background can only be one color so the `set_class` method removes the class bg-blue-500 and adds the class bg-red-500.

## Sharing Event Handlers

### Example 1

In many cases it is convenient to share one event handler among several elements. Please run the example below:

```python
import justpy as jp

def button_click1(self, msg):
    self.num_clicked += 1
    self.message.text = f'{self.text} clicked. Number of clicks: {self.num_clicked}'
    self.set_class('bg-red-500')
    self.set_class('bg-red-700', 'hover')

def event_demo5():
    number_of_buttons = 25
    wp = jp.WebPage()
    button_div = jp.Div(classes='flex m-4 flex-wrap', a=wp)
    button_classes = 'w-32 mr-2 mb-2 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full'
    message = jp.Div(text='No button clicked yet', classes='text-2xl border m-4 p-2', a=wp)
    for i in range(1, number_of_buttons + 1):
        b = jp.Button(text=f'Button {i}', a=button_div, classes=button_classes, click=button_click1)
        b.message = message
        b.num_clicked = 0
    return wp

jp.justpy(event_demo5)
```

This program creates 25 buttons on each page. Under the buttons is a message box that provides information about which button was clicked and how many times it was clicked (try clicking the same button several times and see the change in the message box).

Let's delve into the program in more detail. The program has two functions. The function `event_demo` creates the page and returns it when a page is requested. The function `button_click` will handle the click event of all buttons.
In the first line of `event_demo`, the number of buttons is set (try changing this number and see what happens).  The second line creates a web page. The third line creates a div element (the general purpose HTML container element) named `button_div`. We will use it shortly to contain all the buttons. Notice that using `a=wp` we add `button_div` to the page.

The fourth line defines the classes that will be used to format all the buttons. Don't worry if you don't understand what all the Tailwind classes do at this stage, it is not important. The fifth line creates the `message` element and adds it to the page. This element displays information about the button that is clicked.

On the sixth line  the loop that creates all the buttons starts. For each iteration of the loop, a button is created and added to `button_div`. Since `button_div` was previously added to the web page, the buttons will also be displayed on the page.

A button in JustPy is just an instance of the `Button `class, and therefore we can assign additional attributes to the instance. That is what we do in the next two lines. We assign to the `message` attribute the `message` element and initialize the `num_clicked` attribute to 0 (these attributes will be used in the `button_click` function as we shall see shortly).

After the loop, the web page is returned, and the framework renders it to the user's browser.
It may seem that the loop is erasing previous buttons by redefining the variable `b`. That is not the case because each time through the loop a new button is created and is added to the component list of `button_div` (using the keyword argument notation: `a=button_div`). At the end of the loop, `button_div` has 25 distinct child component instances. You can verify this by adding the following two lines just before the `return` statement of `event_demo` and re-running the program:
```python
print(button_div)
print(button_div.components)
```

The `components` attribute is a list that holds all the child component instances of the element in the order they will be rendered. It is named "components" because it holds the building blocks of the element (though strictly speaking, the list holds elements which are instances of components).  

Let's take a look now at `button_click`, the second function in our program. When any one of the buttons is clicked, this function is executed. The arguments for `button_click` are the same as those for all event handlers in JustPy. The first argument `self`, is the button. In JustPy, as previously discussed, elements on the page are represented by instances of Python classes. The buttons we created are instances of the `Button` class and therefore in this case `self` will be an instance of the Button class.

In the first line of `button_click` we increment the instance attribute that tracks the number of times the specific button was clicked. It was initialized as 0 when we created the button in `event_demo`. The second line changes the text of the message box. Since we conveniently assigned the appropriate div element to the message attribute of all buttons, we know where to find it. It is right there as an attribute of `self`.

**Please skip this paragraph if you are not familiar with JavaScript:** Contrast this with the JavaScript methods of getting elements by id or class or using some more complex DOM query. In most cases we don't need to query the Python representation of the DOM if we anticipate in advance which elements an event handler will require.

The last two lines of `button_click` change the background of the button that was clicked to red and change the background of the button when it is hovered.

### Example 2   

As the program is written now, once a button is clicked, its background will always be red, even if another button is clicked. If we want only the background of the last clicked button to be red, the event handler needs to set the background of all other buttons back to blue. There are many ways that this could be done but I would like to highlight a method that can be generalized to most cases.

The web page itself is an instance of a Python class and therefore can have user specified attributes. We will create a list of all the buttons and assign it to the `button_list` attribute of the page. In the event handler we will loop over this list and change the backgrounds to blue after which we will set the background of the clicked button to red.

!!! info
    We know which page's `button_list` we need to loop over because the page on which the event originated is always provided to the event handler in `msg.page` by JustPy.

The result looks like this:
```python
import justpy as jp

def button_click2(self, msg):
    self.num_clicked += 1
    self.message.text = f'{self.text} clicked. Number of clicks: {self.num_clicked}'
    for button in msg.page.button_list:
        button.set_class('bg-blue-500')
        button.set_class('bg-blue-700', 'hover')
    self.set_class('bg-red-500')
    self.set_class('bg-red-700', 'hover')

def event_demo6():
    number_of_buttons = 25
    wp = jp.WebPage()
    button_div = jp.Div(classes='flex m-4 flex-wrap', a=wp)
    button_classes = 'w-32 mr-2 mb-2 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full'
    message = jp.P(text='No button clicked yet', classes='text-2xl border m-4 p-2', a=wp)
    button_list = []
    for i in range(1, number_of_buttons + 1):
        b = jp.Button(text=f'Button {i}', a=button_div, classes=button_classes, click=button_click2)
        b.message = message
        b.num_clicked = 0
        button_list.append(b)
    wp.button_list = button_list   # The list will now be referenced by the WebPage instance attribute
    return wp

jp.justpy(event_demo6)
```

### Example 3 - Event changes elements on page

Events can also change the elements on the page itself, adding or removing them as necessary. As a concrete example let's change the program above to display a log of buttons that were clicked instead of just one line of information.
```python
import justpy as jp

def button_click3(self, msg):
    self.num_clicked += 1
    # self.message.text = f'{self.text} clicked. Number of clicks: {self.num_clicked}'
    p = jp.P(text=f'{self.text} clicked. Number of clicks: {self.num_clicked}')
    self.message.add_component(p, 0)
    for button in msg.page.button_list:
        button.set_class('bg-blue-500')
        button.set_class('bg-blue-700', 'hover')
    self.set_class('bg-red-500')
    self.set_class('bg-red-700', 'hover')

def event_demo7():
    number_of_buttons = 25
    wp = jp.WebPage()
    button_div = jp.Div(classes='flex m-4 flex-wrap', a=wp)
    button_classes = 'w-32 mr-2 mb-2 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full'
    message = jp.Div(classes='text-lg border m-2 p-2 overflow-auto h-64', a=wp)
    message.add(jp.P(text='No button clicked yet'))
    button_list = []
    for i in range(1, number_of_buttons + 1):
        b = jp.Button(text=f'Button {i}', a=button_div, classes=button_classes, click=button_click3)
        b.message = message
        b.num_clicked = 0
        button_list.append(b)
    wp.button_list = button_list   # The list will now be referenced by the WebPage instance attribute
    return wp

jp.justpy(event_demo7)
```

Instead of just changing the text in `message`, `button_click` creates a `p` element with the text message and adds the element to `message` using the `add_component` method. It is different from `add` because it allows adding a component at any position. Here, we are adding the new log info at the beginning of the `message` div so that most recent messages show up first. Also, in `event_demo` we changed `message` to a div element and added the first message as a p element with text.

## Inline Event Handlers

In a very non-Pythonic manner, JustPy supports inserting inline functions as event handlers when creating an element. I confess to using these functions sometimes for event handlers that are just one or two lines of code.

The function itself is represented as a string, not a real Python function. Statements are separated by the semicolon. The function assumes that the two arguments are `self` and `msg`. The namespace is that of the JustPy package. If you want the function to have access to a variable, assign it to an attribute of `self`.

```python
import justpy as jp


def event_comp_test():
    wp = jp.WebPage()
    d = jp.Div(text='hello1',
            click='self.text="clicked"',
            mouseenter='self.text="entered"; self.set_class("text-5xl"); msg.page.add(Div(text=f"{len(msg.page)} Additional Div"))',
            mouseleave='self.text="left"; self.set_class("text-xl")',
            classes='text-2xl border p-2 m-2', a=wp )
    d = jp.Div(text='hello2', click='self.text="clicked"', mouseenter='self.text="entered"', classes='text-2xl border p-2 m-2', a=wp )
    d = jp.Div(text='hello3', click='self.text="clicked"', mouseenter='self.text="entered"', classes='text-2xl border p-2 m-2', a=wp )
    return wp


jp.justpy(event_comp_test)
```

## The debounce and throttle Event Modifiers

Sometimes you need to debounce or throttle on event. To do this, use the `debounce` and `throttle` keyword arguments of the `on` method. The value is the wait time in milliseconds. If you want the debounce to be leading edge, set the `immediate ` attribute of `on` to `True`.

The example below also uses the `add_event` method. The `mousemove` event is not among the events that are supported by default and needs to be added to the element's allowed events.

```python
import justpy as jp

def mouse_event(self, msg):
    try:
        self.counter += 1
    except:
        self.counter = 1
    msg.page.info_div.add_first(jp.Div(text=f'{self.counter}) {msg.event_type}'))


def debounce_test():
    wp = jp.WebPage()
    d = jp.Div(style='height: 100vh', a=wp)
    d.add_event('mousemove')
    d.on('mousemove', mouse_event, throttle=1000)
    d.on('click', mouse_event, debounce=2000, immediate=False)
    wp.info_div = jp.Div(text='Recent mouse events', classes='m-4 text-lg', a=d)
    return wp

jp.justpy(debounce_test)
```

## The click__out Event

The `click__out` event fires when there is a click outside of an element. This is useful for example in the case of dropdown list you would like closed when there is a click outside of the dropdown element.

!!! info
    Notice the TWO underline characters in `click__out`.


```python
import justpy as jp

def click_out(self, msg):
    self.text = 'click out'
    self.set_classes('text-blue-500')

def click_in(self, msg):
    self.text = 'click in'
    self.set_classes('text-red-500')

def out_test():
    wp = jp.WebPage()
    for i in range(4):
        d = jp.Div(text=f'{i}) Div', a=wp, classes='m-4 p-4 text-xl border w-32')
        d.on('click__out', click_out)
        d.on('click', click_in)
    return wp

jp.justpy(out_test)
```

## Event Handlers Defined in Components

This section reflects changes introduced in version 0.1.0

!!! Note
    You may want to return to this section after having covered the custom components part of the tutorial

In the example below we define a simple component that is a Div that includes 5 buttons and another Div with some information.

If an event handler is defined as a method of a component, the `self` attribute passed to it will be that of the component instance and not of the child instance which originated the event. That child instance can be found in the `msg.target` field.


```python
import justpy as jp

class ButtonDiv(jp.Div):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        for i in range(1,6):
            b = jp.Button(text=f'Button {i}', a=self, classes=' m-2 p-2 border text-blue text-lg')
            b.num = i
            b.on('click', self.button_clicked)
        self.info_div = jp.Div(text='info will go here', classes='m-2 p-2 border', a=self)

    def button_clicked(self, msg):
        print(self)
        print(msg.target)
        self.info_div.text = f'Button {msg.target.num} was clicked'

def target_test():
    wp = jp.WebPage()
    ButtonDiv(a=wp)
    return wp

jp.justpy(target_test)
```
