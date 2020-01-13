# Getting Started

In order to take full advantage of this tutorial some knowledge of Python is required including an understanding
of [object oriented programming](https://docs.python.org/3/tutorial/classes.html) in Python. 
In addition, a basic understanding of HTML is required ([HTML - Getting Started](https://developer.mozilla.org/en-US/docs/Learn/HTML/Introduction_to_HTML/Getting_started)). 

?> The examples in this tutorial use [Python f-strings](https://realpython.com/python-f-strings/) which were added in Python 3.6

## Installation

First, make sure that the version of `python3` you have is 3.6 or higher:
`$ python3 --version`

If not, upgrade your Python interpreter.

It is probably best to run the programs in this tutorial in a virtual environment so that your system wide Python interpreter is not affected, though this is not a requirement.
The following commands create a directory for this tutorial, then create a virtual environment named jp and activate it and finally install JustPy:

```
$ mkdir jptutorial
$ cd jptutorial
$ python3 -m venv jp
$ source jp/bin/activate
(jp) $ pip install justpy
```

On Microsoft Windows, the activation command for the virtual environment is `jp\Scripts\activate` instead of the source command above.

Now, using your favorite code editor, create a file in the jptutorial directory called test.py that includes the following code:

```python
import justpy as jp

def hello_world():
    wp = jp.WebPage()
    jp.Hello(a=wp)
    return wp

jp.justpy(hello_world)
```

!> You can easily copy the code by hovering over it and then clicking 'Copy to clipboard' in the upper right corner

## Running the Program

To run the program execute the following command:

```
$ python3 test.py
```

Then, direct your browser to http://localhost:8000/ or http://127.0.0.1:8000  (this refers to port 8000 on the local machine, one of these should work no matter your operating system). You should see 'Hello!' in your browser.  Click it a few times also. It should report the number of times it has been clicked. 

In this tutorial, when asked to "run the program", follow the two steps above (there is no need to name the file "test.py", you can use any name you like). 



# The Basic Concepts

## JustPy Components
JustPy components are classes that instantiate reusable elements that can be be rendered in a browser.
Out of the box, JustPy comes with many components. You can use the available JustPy components
and also build more complex components using other components as building blocks.

In JustPy, components are implemented as Python classes. When you define a new component, you do so by defining a new Python class. 
A JustPy element is an instance of a component class.

```python
import justpy as jp
p = jp.P()
p.text = 'Hello!'
``` 

In the example above, `p` is an instance of the class `P`. Its text attribute is set to 'Hello!'.
The above is equivalent to the HTML element:
```html
<p>Hello!</p>
```

You can set the JustPy element attributes when the element is created (synonym for instantiated) using keyword arguments to make code shorter and clearer:
```python
import justpy as jp
p = jp.P(text='Hello!')
``` 

Just creating an element is not very useful. We need to get it on a web page and into the user's browser tab. We will do this next.

## JustPy Web Pages

In JustPy, web pages are instances of the JustPy class `WebPage`. You create a web page the same way you create any class instance in Python:
```python
import justpy as jp
wp = jp.WebPage()
```  

In the example above we created the web page `wp`. It is an empty web page that does not contain any elements.

Let's create an element and add it to the page:
```python
import justpy as jp
wp = jp.WebPage()
p = jp.P(text='Hello World!')
wp.add(p)  # Same as p.add_to(wp), wp = wp + p, wp += p
```

In the example above, we create a web page. Then we create a `p` element and add it to the page using the `add` method.

Since adding an element to a page is very common, there is a way to do so using the keyword argument `a`: 
```python
import justpy as jp
wp = jp.WebPage()
p = jp.P(text='Hello World!', a=wp)
```

This code snippet has the same functionality as the one above it.

## JustPy Requests

So far we have created a page and added an element to it. We haven't yet loaded the page into the user's browser.

?> In this tutorial, I will call the process of delivering a Web page to a user "**rendering the page**".

When you type a URL into your browser's [Address Bar](https://en.wikipedia.org/wiki/Address_bar) and tell your browser to navigate to that address,
the browser generates a request; it requests data from the server the URL you entered points to. 

When a request comes from a browser, the JustPy framework runs a user defined function. 
This function must return a web page which is then rendered in the browser that sent the request. All that you as a developer needs to do is write the function that takes a request and returns a web page.
The framework takes care of the rest.

## Hello World

Here is a basic example:

```python
import justpy as jp

def hello_world():
    wp = jp.WebPage()
    p = jp.P(text='Hello World!', a=wp)
    return wp

jp.justpy(hello_world)
```

The function `hello_world` creates a web page, adds a paragraph element to it and returns the page.
 
!> **In this tutorial, functions like `hello_world` will be called "request handlers".**

The `jp.justpy(hello_world)` command starts a web server and sends all requests to the function `hello_world`.

Run the program above (as explained in [getting started](tutorial/getting_started.md#Run "Getting Started") ).
You should see 'Hello World!' in your browser.

## More Hello World

Saying hello once isn't enough! We would like to say "hello" ten times. We also want to let the user know how many times we said "hello". More specifically, we would like "Hello World!" to show up ten times on the page and be enumerated. In addition, we would like to use a bigger font each time. 

```python
import justpy as jp

def hello_world():
    wp = jp.WebPage()
    for i in range(1,11):
        jp.P(text=f'{i}) Hello World!', a=wp, style=f'font-size: {10*i}px')
    return wp

jp.justpy(hello_world)
```
 
Run the program above and look at the result in your browser.
 
!> **Don't forget to terminate the previous program first.**  
Two JustPy servers cannot run at the same time on one machine.

The P instances are created inside a loop with the loop index being used to give each paragraph some different text and a different font size.

The `style` attribute in JustPy is the same as the HTML [style](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/style) attribute. It allows using [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS) properties to style the element. 

For example, change the style assignment to:
```python
style=f'color: blue; font-size: {10*i}px' 
```
and see what happens.

## Tailwind and JustPy

Another way to style elements is to use classes.
By default, instances of WebPage support styling using [Tailwind](https://tailwindcss.com/) classes. If you are familiar with CSS, checkout Tailwind. For me, it is a joy to work with.

?> You can also put your own CSS on a page and use your own class definitions by setting the `css` attribute of a page.

Let's use Tailwind classes to style our page:

```python
import justpy as jp

def hello_world():
    wp = jp.WebPage()
    my_paragraph_design = "w-64 bg-blue-500 m-2 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
    for i in range(1,11):
        jp.P(text=f'{i}) Hello World!', a=wp, classes=my_paragraph_design)
    return wp

jp.justpy(hello_world)
```

In this program Tailwind classes are used to make the output a little nicer. The JustPy attribute `classes` is equivalent to the HTML attribute [class](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/class) (which is a reserved word in Python).
 
## Creating Web Pages Once

You may have noticed that since we have been serving the same page to everyone, there is no need to create a new page each time a request is made.
We can create a page one time, and serve the same page for all requests:
```python
import justpy as jp

wp = jp.WebPage(delete_flag=False)
my_paragraph_design = "w-64 bg-blue-500 m-2 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
for i in range(1,11):
    jp.P(text=f'{i}) Hello World!', a=wp, classes=my_paragraph_design)

def hello_world():
    return wp

jp.justpy(hello_world)
```

!> When you define a page that is going to be rendered in more than one browser tab or page, you need to set its `delete_flag` to `False`.

Otherwise, the page (the instance of `WebPage` to be precise) will be deleted when a browser tab or window that renders that page is closed.
The default is for JustPy to remove all references to the page and the elements on it so that the Python garbage collector can reclaim the memory. 

?> When a page's (or element's) `delete_flag` is set to `False`, none of its child elements will be deleted, even if their `delete_flag` is `True`. 

In the next part of the tutorial you will learn how to deal with events such as a mouse click.
 
# Handling Events
In this part of the tutorial you will learn how to deal with user generated events such as a mouse click. JustPy deals with such events by binding a function to an event. When the event occurs, the function is executed. Please run the following program and click on 'Not clicked yet':

```python
import justpy as jp

def my_click(self, msg):
    self.text = 'I was clicked'

def event_demo():
    wp = jp.WebPage()
    d = jp.Div(text='Not clicked yet', a=wp, classes='w-48 text-xl m-2 p-1 bg-blue-500 text-white')
    d.on('click', my_click)
    return wp

jp.justpy(event_demo)
```

In `event_demo`, we first create a web page. Then we create a [Div](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/div) element named `d` whose content is the string "Not clicked yet" and add it to the page (we also add some Tailwind classes for formatting). Then, using the `on` method, we bind the function `my_click`, which we defined earlier, to the click event and return the page. When the the element on the page is clicked, JustPy runs the function `my_click`.

!> Functions that handle events are called "event handlers". `my_click` is an example of such a function.
 
!> In JustPy, event handlers **must** have two arguments. 
 
The first (I recommend calling it `self`), is the object which generated the event. It is an instance of one of the component classes. In the example above it is `d`, an instance of the class `Div`. The second parameter (I recommend calling it `msg`) is a [dictionary](https://github.com/mewwts/addict "addict is a Python module that gives you dictionaries whose values are both gettable and settable using attributes, in addition to standard item-syntax") that contains information about the event. The items in this dictionary can also be accessed using attribute (dot) notation. To get the event type for example we could write either  `msg['event_type']` or `msg.event_type`. 
 
In the program below I have added some print commands to the `my_click` function. Run it and see what is printed to the console.
 
```python
import justpy as jp

def my_click(self, msg):
    self.text = 'I was clicked'
    print(msg.event_type)
    print(msg['event_type'])
    print(msg)

def event_demo():
    wp = jp.WebPage()
    d = jp.P(text='Not clicked yet', a=wp, classes='text-xl m-2 p-2 bg-blue-500 text-white')
    d.on('click', my_click)
    return wp

jp.justpy(event_demo)
```
## Multiple Events

The same element can handle multiple events. Run the following and move the mouse in and out of the element on the page. Click the element also.

```python
import justpy as jp

def my_click(self, msg):
    self.text = 'I was clicked'
    self.set_class('bg-blue-500')

def my_mouseenter(self, msg):
    self.text = 'Mouse entered'
    self.set_class('bg-red-500')

def my_mouseleave(self, msg):
    self.text = 'Mouse left'
    self.set_class('bg-teal-500')


def event_demo():
    wp = jp.WebPage()
    d = jp.Div(text='Not clicked yet', a=wp, classes='w-64 text-2xl m-2 p-2 bg-blue-500 text-white',
             click=my_click, mouseenter=my_mouseenter, mouseleave=my_mouseleave)
    return wp

jp.justpy(event_demo)
```
 
 In the example above, there are three event handlers, one each for the `click`, `mouseenter` and `mouseleave` events. All three are bound to the same element, `d`.
 
 Another way of binding event handlers is demonstrated here. Instead of using the `on` method, you can bind an event handler using a keyword argument that corresponds to the name of the event. In addition to `click` (or some other event name) you can also use `onclick` or, `on_click`. All three options work in the same way. 
 
The above example also introduces the `set_class` method. This method "knows" which Tailwind classes logically cannot apply together (for example, text color can't be both red and blue at the same time) and removes the appropriate classes while adding the class provided as parameter. In the case above, the background can only be one color so the `set_class` method removes the class bg-blue-500 and adds the class bg-red-500.

## Sharing Event Handlers

### Example 1 

In many cases it is convenient to share one event handler among several elements. Please run the example below:

```python
import justpy as jp

def button_click(self, msg):
    self.num_clicked += 1
    self.message.text = f'{self.text} clicked. Number of clicks: {self.num_clicked}'
    self.set_class('bg-red-500')
    self.set_class('bg-red-700', 'hover')

def event_demo():
    number_of_buttons = 25
    wp = jp.WebPage()
    button_div = jp.Div(classes='flex m-4 flex-wrap', a=wp)
    button_classes = 'w-32 mr-2 mb-2 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full'
    message = jp.Div(text='No button clicked yet', classes='text-2xl border m-4 p-2', a=wp)
    for i in range(1, number_of_buttons + 1):
        b = jp.Button(text=f'Button {i}', a=button_div, classes=button_classes, click=button_click)
        b.message = message
        b.num_clicked = 0
    return wp 

jp.justpy(event_demo)
```

This program creates 25 buttons on each page. Under the buttons is a message box that provides information about which button was clicked and how many times it was clicked (try clicking the same button several times and see the change in the message box).
 
Let's delve into the program in more detail. The program has two functions. The function `event_demo` creates the page and returns it when a page is requested. The function `button_click` will handle the click event of all buttons.
In the first line of `event_demo`, the number of buttons is set (try changing this number and see what happens).  The second line creates a web page. The third line creates a div element (the general purpose HTML container element) named `button_div`. We will use it shortly to contain all the buttons. Notice that using `a=wp` we add `button_div` to the page. 

The fourth line defines the classes that will be used to format all the buttons. Don't worry if you don't understand what all the Tailwind classes do at this stage, it is not important. The fifth line creates the `message` element and adds it to the page. This element displays information about the button that is clicked.

On the sixth line  the loop that creates all the buttons starts. For each iteration of the loop, a button is created and added to `button_div`. Since `button_div` was previously added to the web page, the buttons will also be displayed on the page. A button in JustPy is just an instance of the `Button `class, and therefore we can assign additional attributes to the instance. That is what we do in the next two lines. We assign to the `message` attribute the `message` element and initialize the `num_clicked` attribute to 0 (these attributes will be used in the `button_click` function as we shall see shortly).

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

?> We know which page's `button_list` we need to loop over because the page on which the event originated is always provided to the event handler in `msg.page` by JustPy.

The result looks like this:
```python
import justpy as jp

def button_click(self, msg):
    self.num_clicked += 1
    self.message.text = f'{self.text} clicked. Number of clicks: {self.num_clicked}'
    for button in msg.page.button_list:
        button.set_class('bg-blue-500')
        button.set_class('bg-blue-700', 'hover')
    self.set_class('bg-red-500')
    self.set_class('bg-red-700', 'hover')

def event_demo():
    number_of_buttons = 25
    wp = jp.WebPage()
    button_div = jp.Div(classes='flex m-4 flex-wrap', a=wp)
    button_classes = 'w-32 mr-2 mb-2 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full'
    message = jp.P(text='No button clicked yet', classes='text-2xl border m-4 p-2', a=wp)
    button_list = []
    for i in range(1, number_of_buttons + 1):
        b = jp.Button(text=f'Button {i}', a=button_div, classes=button_classes, click=button_click)
        b.message = message
        b.num_clicked = 0
        button_list.append(b)
    wp.button_list = button_list   # The list will now be stored in the WebPage instance
    return wp

jp.justpy(event_demo)
```

### Example 3 - Event changes elements on page

Events can also change the elements on the page itself, adding or removing them as necessary. As a concrete example let's change the program above to display a log of buttons that were clicked instead of just one line of information.
```python
import justpy as jp

def button_click(self, msg):
    self.num_clicked += 1
    # self.message.text = f'{self.text} clicked. Number of clicks: {self.num_clicked}'
    p = jp.P(text=f'{self.text} clicked. Number of clicks: {self.num_clicked}')
    self.message.add_component(p, 0)
    for button in msg.page.button_list:
        button.set_class('bg-blue-500')
        button.set_class('bg-blue-700', 'hover')
    self.set_class('bg-red-500')
    self.set_class('bg-red-700', 'hover')

def event_demo():
    number_of_buttons = 25
    wp = jp.WebPage()
    button_div = jp.Div(classes='flex m-4 flex-wrap', a=wp)
    button_classes = 'w-32 mr-2 mb-2 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full'
    message = jp.Div(classes='text-lg border m-2 p-2 overflow-auto h-64', a=wp)
    message.add(jp.P(text='No button clicked yet'))
    button_list = []
    for i in range(1, number_of_buttons + 1):
        b = jp.Button(text=f'Button {i}', a=button_div, classes=button_classes, click=button_click)
        b.message = message
        b.num_clicked = 0
        button_list.append(b)
    wp.button_list = button_list   # The list will now be stored in the WebPage instance
    return wp

jp.justpy(event_demo)
```

Instead of just changing the text in `message`, `button_click` creates a `p` element with the text message and adds the element to `message` using the `add_component` method. It is different from `add` because it allows adding a component at any position. Here, we are adding the new log info at the beginning of the `message` div so that most recent messages show up first. Also, in `event_demo` we changed `message` to a div element and added the first message as a p element with text. 

## Inline Event Handlers

In a very non-Pythonic manner, JustPy supports inserting inline functions as event handlers when creating an element. I confess using these functions sometimes for one or two line event handlers.

The function itself is represented as a string, not a real Python function. Statements are separated by the semicolon. The function assumes that the two arguments are `self` and `msg`. The namespace is that of the JustPy package. If you want the function to have access to a variable, assign it to an attribute of `self`. 

```python
import justpy as jp


def comp_test():
    wp = jp.WebPage()
    d = jp.Div(text='hello1',
            click='self.text="clicked"',
            mouseenter='self.text="entered"; self.set_class("text-5xl"); msg.page.add(Div(text=f"{len(msg.page)} Additional Div"))',
            mouseleave='self.text="left"; self.set_class("text-xl")',
            classes='text-2xl border p-2 m-2', a=wp )
    d = jp.Div(text='hello2', click='self.text="clicked"', mouseenter='self.text="entered"', classes='text-2xl border p-2 m-2', a=wp )
    d = jp.Div(text='hello3', click='self.text="clicked"', mouseenter='self.text="entered"', classes='text-2xl border p-2 m-2', a=wp )
    return wp


jp.justpy(comp_test)
```# HTMl Components

JustPY supports components corresponding to HTML and SVG tags. The name of the component is the same as the name of the HTML tag with the first letter capitalized. For example, we already saw the `Div` and `P` components that correspond to the the `div` and `p` HTML tags. JustPy supports all tags that put elements on the page and are not deprecated in HTML 5. 

Here is a simple example with three HTML components. 

```python
import justpy as jp

def html_comps():
    wp = jp.WebPage()
    jp.I(text='Text in Italic', a=wp)
    jp.Br(a=wp)
    jp.Strong(text='Text in the Strong element', a=wp)
    return wp

jp.justpy(html_comps)
``` 

* The [i](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/i) HTML tag displays text typically in italics. 
* The [br](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/br) HTML tag produces a line break. 
* The [strong](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/strong) HTML tag is typically rendered in bold type. 

The JustPy function `get_tag`, creates an instance of a component based on the HTML tag. Its first argument is a string with the tag and the rest of the arguments are the identical optional keyword arguments for the class constructor. The program below is equivalent to the one above:

```python
import justpy as jp

def html_comps():
    wp = jp.WebPage()
    jp.get_tag('i', text='Text in Italic', a=wp)
    jp.get_tag('br',a=wp)
    jp.get_tag('strong', text='Text in the Strong element', a=wp)
    return wp

jp.justpy(html_comps)
```

It is also possible to get the same formatting using the the `Div` component with the appropriate Tailwind classes:
```python
import justpy as jp

def html_comps():
    wp = jp.WebPage()
    jp.Div(text='Text in italic', a=wp, classes='italic')
    jp.Div(text='Text in bold', a=wp, classes='font-bold')
    return wp

jp.justpy(html_comps)
```

If you do not need the semantic information the specialized tags provide, it is more convenient to use `Div`, `P`, or `Span` with the appropriate Tailwind classes or style attribute.

## Container Elements

Many HTML elements can have children elements. In JustPy parlance, an element can contain other elements.

```python
import justpy as jp

def html_comps():
    wp = jp.WebPage()
    for i in range(10):
        d = jp.Div(a=wp, classes='m-2')
        for j in range(10):
            jp.Span(text=f'Span #{j+1} in Div #{i+1}', a=d, classes='text-white bg-blue-700 hover:bg-blue-200 ml-1 p-1')
    return wp

jp.justpy(html_comps)
```

In the program above, in each iteration of the outer loop a new `Div` element is created and in the inner loop, ten `Span` elements are added to it. This is done using the `a=d` keyword argument.

Change the element created in the inner loop from a `Span` to a `Div`, `P`, or `I` and see what happens.

## Common Attributes

HTML components have common attributes as well as specific ones. JustPy components support the following [global attributes](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes) for all HTML components:
`contenteditable`, `dir`, `tabindex`, `title`, `accesskey`, `draggable`, `lang`, `hidden`

In this example we use the `contenteditable`, `dir`, and `lang` attributes:

```python
import justpy as jp

def html_comps():
    wp = jp.WebPage()
    for j in range(10):
        p = jp.P(text=f'אני אוהב לתכנת בפייתון', a=wp, contenteditable=True, classes='text-white bg-blue-500 hover:bg-blue-700 ml-1 p-1 w-1/2')
        p.dir = 'rtl'
        p.lang = 'he'
    return wp

jp.justpy(html_comps)
```

The text in each P element is made editable by setting `contenteditable` to `True` (using a keyword argument). We set `dir` to "rtl" (right-to-left) and `lang` to "he" (the language code for Hebrew). We do so by setting the attribute directly though we could have used a keyword argument.

Run the program and try editing some text. You will see also that the Hebrew text is rendered right to left.

## Specific Attributes

Some components have specific attributes. For example [img tag](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/img) has the `src` attribute that specifies the URL for the image.
Run the following program:
```python
import justpy as jp

def html_comps():
    wp = jp.WebPage()
    for degree in range(0, 361, 10):
        image = jp.Img(src='https://www.python.org/static/community_logos/python-powered-h-140x182.png', a=wp)
        image.classes = 'm-4 p-4 inline-block'
        image.style = f'transform: rotate({degree}deg)'
        image.height = 100
        image.width = 100
        image.degree = degree

        def straighten(self, msg):
            self.style = f'transform: rotate(0deg)'

        def rotate_back(self, msg):
            self.style = f'transform: rotate({self.degree}deg)'

        def no_rotate(self, msg):
            self.degree = 0
            self.set_class('bg-red-200')

        image.on('mouseenter', straighten)
        image.on('mouseleave', rotate_back)
        image.on('click', no_rotate)

    return wp

jp.justpy(html_comps)
```

The program renders on the page a progression of images of the **Python Powered** logo each rotated 10 degrees relative to the former image. When the mouse enters an image, it "straightens" and when it leaves, it returns to its original rotation. If you click on an image, it does not rotate anymore.

The images are added inside a loop. In each iteration of the loop, an image is added to the page. The `src` attribute designates where to fetch the image from, in our case the [python.org](https://www.python.org) website. As you see in this example, you can combine Tailwind classes (or any CSS classes) with setting the `style` attribute. Here, the style is set to [rotate](https://developer.mozilla.org/en-US/docs/Web/CSS/transform-function/rotate) the image based on the loop variable. We also set the height and width attributes of the image to 100.

The program then sets the `degree` attribute of the image to the loop variable. It will be used in the event handlers that define the interaction with the mouse. 

!>`degree` is a different kind of attribute than `src`, `height`, and `width`. It is a user defined attribute that is not part of the HTML specification. In the JustPy component definitions, attributes that are part of the HTML specification are explicitly identified and handled accordingly.

The mouse event handlers change the `style` and `class` attributes of the element as needed using the `degree` attribute of the image if required. For clarity, the event handlers are defined inside the loop, but they could be defined just once outside the loop or outside the request handler. We could also set the attributes as keyword arguments and the result is the following:

```python
import justpy as jp

def straighten(self, msg):
    self.style = f'transform: rotate(0deg)'

def rotate_back(self, msg):
    self.style = f'transform: rotate({self.degree}deg)'

def no_rotate(self, msg):
    self.degree = 0
    self.set_class('bg-red-200')

def html_comps():
    wp = jp.WebPage()
    for degree in range(0, 361, 10):
        jp.Img(src='https://www.python.org/static/community_logos/python-powered-h-140x182.png', a=wp,
                classes='m-4 p-4 inline-block', style=f'transform: rotate({degree}deg)', height=100, width=100,
                degree=degree, mouseenter=straighten, mouseleave=rotate_back, click=no_rotate)
    return wp

jp.justpy(html_comps)
```

## HTML Links

In JustPy you create hyperlinks using the `A` component which corresponds to the [`a` HTML tag](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/a).

The `A` component is also named `Link` (in case you want to use a more descriptive name).

```python
import justpy as jp

def link_demo():
    wp = jp.WebPage()
    jp.A(text='Python Org', href='https://python.org', a=wp, classes='m-2 p-2 text-xl text-white bg-blue-500 hover:bg-blue-700')
    return wp

jp.justpy(link_demo)

```

The link above goes to the Python.org web page. If you want the link to open in a new window, set the `target` attribute of the `A` component instance to '_blank' 

If you want to link to an element on the page, use the `bookmark` attribute and assign to it the element you want to link to. If you want to scroll to the element, instead of jumping instantly, set the `scroll` attribute to `True`. 

```python
import justpy as jp

def link_demo():
    wp = jp.WebPage()
    link = jp.A(text='Scroll to target', a=wp, classes='inline-block m-2 p-2 text-xl text-white bg-blue-500 hover:bg-blue-700')
    # jp.Br(a=wp)
    for i in range(50):
        jp.P(text=f'{i+1} Not a target', classes='m-1 p-1 text-white bg-blue-300', a=wp)
    target = jp.A(text=f'This is the target - it is linked to first link, click to jump there', classes='inline-block m-1 p-1 text-white bg-red-500', a=wp)
    link.bookmark = target
    link.scroll = True
    target.bookmark = link
    for i in range(50):
        jp.P(text=f'{i+50} Not a target', classes='m-1 p-1 text-white bg-blue-300', a=wp)
    return wp

jp.justpy(link_demo)
```

## Lists

The [ul tag](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/ul) together with the [li tag](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/ul) can be used to create lists. The corresponding JustPy components are `Ul` and `Li`.
```python
import justpy as jp

def list_demo():
    wp = jp.WebPage()
    my_list = jp.Ul(a=wp, classes='m-2 p-2')
    for i in range (1,11):
        jp.Li(text=f'List one item {i}', a=my_list)
    my_list = jp.Ul(a=wp, classes='m-2 p-2 list-disc list-inside')
    for i in range(1, 11):
        jp.Li(text=f'List two item {i}', a=my_list, classes='hover:bg-gray-200')
    my_list = jp.Ul(a=wp, classes='m-2 p-2 list-decimal list-inside')
    for i in range(1, 11):
        jp.Li(text=f'List three item {i}', a=my_list)
    return wp

jp.justpy(list_demo)
```

The program above creates three lists. Use the [`list-disc` and `list-decimal`](https://tailwindcss.com/docs/list-style-type) Tailwind classes to get bulleted or numeric lists. The [`list-inside`](https://tailwindcss.com/docs/list-style-position) class controls the positions of the markers of the list. If you choose to put them outside, make sure there is enough room to render them.

## Showing and Hiding Elements

All JustPy components use the `show` boolean attribute to determine whether an element should be rendered on the page. If `show` is `False`, the element will not be on the page at all.

If you want the element to be on the page, but be invisible, use the `visible` and `invisible` Tailwind classes (or appropriate `style` values). When an element is invisible, the page structure stays the same.

Run the following program and see the difference by clicking both buttons.

```python
import justpy as jp

button_classes='m-2 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded'

def show_demo():
    wp = jp.WebPage()
    b = jp.Button(text='Click to toggle show', a=wp, classes=button_classes)
    d = jp.Div(text='Toggled by show', classes='m-2 p-2 text-2xl border w-48', a=wp)
    b.d = d
    jp.Div(text='Will always show', classes='m-2', a=wp)

    def toggle_show(self, msg):
        self.d.show = not self.d.show

    b.on('click', toggle_show)

    b = jp.Button(text='Click to toggle visibility', a=wp, classes=button_classes)
    d = jp.Div(text='Toggled by visible', classes='m-2 p-2 text-2xl border w-48', a=wp)
    d.visibility_state = 'visible'
    b.d = d
    jp.Div(text='Will always show', classes='m-2', a=wp)

    def toggle_visible(self, msg):
        if self.d.visibility_state == 'visible':
            self.d.set_class('invisible')
            self.d.visibility_state = 'invisible'
        else:
            self.d.set_class('visible')
            self.d.visibility_state = 'visible'

    b.on('click', toggle_visible)
    return wp

jp.justpy(show_demo)
```


# Routes

In all the examples above, any [URL](https://en.wikipedia.org/wiki/URL) typed into the browser would render the same page. Usually, when we develop a web application, we want different URLs to load different pages. In other words, we want to define different request handlers to handle different URLs. In this part of the tutorial we will show how to do this using JustPy. 

Please run the following program:
```python
import justpy as jp

def hello_function():
    wp = jp.WebPage()
    wp.add(jp.P(text='Hello there!', classes='text-5xl m-2'))
    return wp

jp.Route('/hello', hello_function)

jp.justpy()
```
Unless you go specifically to http://127.0.0.1:8000/hello you will get the 'Page not found' JustPy message. When a request arrives, JustPy checks if the route in the URL matches any of the defined routes. If it does, it runs the appropriate function and if not, it runs the function provided as the argument `justpy.` If no argument is provided to `justpy`, the framework shows the 'Page not found' message. 

Try running the following program:
```python
import justpy as jp

def hello_function():
    wp = jp.WebPage()
    wp.add(jp.P(text='Hello there!', classes='text-5xl m-2'))
    return wp

def bye_function():
    wp = jp.WebPage()
    wp.add(jp.P(text='Goodbye!', classes='text-5xl m-2'))
    return wp

jp.Route('/hello', hello_function)

jp.justpy(bye_function)
```

Type different URLs into the browser and see what happens. Unless the path is exactly '/hello', the `bye_function` will run and 'Goodbye!' will be displayed.
 
!> All paths must start with '/', otherwise an error occurs.

## Using Decorators

It is common in Python web frameworks to use decorators to assign functions to routes because it is quite convenient and makes the code more readable. JustPy also supports assigning routes using decorators:

```python
import justpy as jp

@jp.SetRoute('/hello')
def hello_function():
    wp = jp.WebPage()
    wp.add(jp.P(text='Hello there!', classes='text-5xl m-2'))
    return wp

@jp.SetRoute('/bye')
def bye_function():
    wp = jp.WebPage()
    wp.add(jp.P(text='Goodbye!', classes='text-5xl m-2'))
    return wp


jp.justpy()
```

The SetRoute decorator accepts as a parameter the route and assigns the decorated function to it. The program above defines two routes, '/hello' and '/bye'. URLs that do not include these exact routes, will cause the 'Page not found' message to appear. 
# The Request Object

JustPy request handlers (functions that handle requests) can receive an optional argument, the request object. JustPy checks if the request handler it needs to run is defined with an argument, and if so, executes the request handler with that argument.

## URL Parameters

To start let's look at a concrete example. URLs may include a [query string](https://en.wikipedia.org/wiki/Query_string) with parameters: www.example.com/?num=4&name=Joe
In this example the URL includes two parameters, `num` and `name` with values of 4 and 'Joe'.

The request object includes (among other things) information about the URL parameters. 
Here is a simple program that displays a page with the parameters in the URL:
```python
import justpy as jp

def demo_function(request):
    wp = jp.WebPage()
    if len(request.query_params) > 0:
        for key, value in request.query_params.items():
            jp.P(text=f'{key}: {value}', a=wp, classes='text-xl m-2 p-1')
    else:
        jp.P(text='No URL paramaters present', a=wp, classes='text-xl m-2 p-1')
    return wp

jp.justpy(demo_function)
```

Try entering http://127.0.0.1:8000/?number=5&name=Smith for example. The request object has several attributes. One of them is the Python dictionary `request.query_params` which as its name implies, includes the keys and values of the URL parameters. In the program above we iterate over this dict and add to the page all the keys and their corresponding values.

## Dog Example

Let's do something a little more useful (well, at least more entertaining). The site https://dog.ceo provides pictures of dogs using a simple [API](https://en.wikipedia.org/wiki/Application_programming_interface). Please run the following program and load a browser page without any parameters in the URL:

```python
import justpy as jp

async def dog_pic(request):
    wp = jp.WebPage()
    breed = request.query_params.get('breed', 'papillon' )
    r = await jp.get(f'https://dog.ceo/api/breed/{breed}/images/random')
    img_url = r['message']
    jp.Img(src=img_url, a=wp, classes='m-2 p-2')
    return wp

jp.justpy(dog_pic)
```

After a few seconds, you should see a picture of a [papillon](https://www.akc.org/dog-breeds/papillon/). That is the default dog breed to show (now you know the breed of my two dogs). Each time you reload the page you will get a different picture as we are asking the site for a random image. Try changing the breed of the dogs in the picture by specifying the breed parameter in the URL, for example: http://127.0.0.1:8000/?breed=corgi

Let's examine the program. First, notice how we define `dog_pic` as an `async` function (if you don't know what `async` functions are in Python just skip this paragraph and the next). JustPy uses [starlette.io](https://www.starlette.io/), "a lightweight ASGI framework/toolkit, which is ideal for building high performance asyncio services".  To shield users from the complexities of async programming in Python, JustPy allows both functions that handle requests and functions that handle events to be either `async` or not. The framework checks if a function is a coroutine and runs it accordingly. 

When a request or event handler require I/O operations over the internet (or to access a local database or even file), it is recommended that they be of type `async` and that all I/O and database operations be non-blocking (this means they are run as a coroutine or in another thread). Otherwise, the application will not scale. To help with the simple case of using an API with the HTTP GET method, JustPy provides a helper function conveniently called `get`. The function asynchronously retrieves information which it assumes is in JSON format and converts it to a Python dictionary.
 
In the program above we call the `get` function with the appropriate URL. We are requesting the URL for a random image of dog with a certain breed. That URL can be found under the 'message' key in the dictionary `r`. We then add an image to the page using the `Img` class which corresponds to the HTML img tag. The `src` attribute is then set to the URL of the image. Finally, we return the page which the framework will then render. 

## Dog Example with Image Click

As the program is currently written, to get a new image we need to reload the page. Let's change this so that by clicking on the image, a new one is loaded:

```python
import justpy as jp

async def get_image(self, msg):
    r = await jp.get(f'https://dog.ceo/api/breed/{msg.page.breed}/images/random')
    self.src = r['message']


async def dog_pic(request):
    wp = jp.WebPage()
    breed = request.query_params.get('breed', 'papillon')
    wp.breed = breed
    r = await jp.get(f'https://dog.ceo/api/breed/{breed}/images/random')
    img_url = r['message']
    jp.Img(src=img_url, a=wp, classes='m-2 p-2 cursor-pointer', click=get_image)
    return wp

jp.justpy(dog_pic)
```

We added the function `get_image` and assigned the image's click event to it . We also made a small design change by adding 'cursor-pointer' to the classes of the image. When the mouse cursor enters the image, it will change its shape to indicate that the image can be interacted with. Notice how we also assigned the breed to a page attribute so that `get_image` will have direct access to it via `msg.page.breed`.

## Path Parameters

Thanks to [starlette.io](https://www.starlette.io/), JustPy also supports path parameters in addition to URL query parameters. Let's change the example above so that the breed is determined by the path in the URL:

```python
import justpy as jp

async def get_image(self, msg):
    r = await jp.get(f'https://dog.ceo/api/breed/{msg.page.breed}/images/random')
    self.src = r['message']

@jp.SetRoute('/breed/{breed}')
async def dog_pic(request):
    wp = jp.WebPage()
    breed = request.path_params.get('breed', 'papillon')
    wp.breed = breed
    r = await jp.get(f'https://dog.ceo/api/breed/{breed}/images/random')
    img_url = r['message']
    jp.Img(src=img_url, a=wp, classes='m-2 p-2 cursor-pointer', click=get_image)
    return wp

jp.justpy(dog_pic)
```

Try going to http://127.0.0.1:8000/breed/borzoi or http://127.0.0.1:8000/breed/boxer
 
Path parameters are defined by surrounding them with {} in the path. If JustPy can match the path to the URL, it executes the function and provides the path parameters in the dictionary `request.path_params`. To learn more about the different options with path parameters go to https://www.starlette.io/routing/
# Input Component

## Bssic Use

Many web applications require users to fill forms. HTML forms are based on the [input HTML tag](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input).

The corresponding JustPy component is `Input`.

The following program adds a text input field to a page:
```python
import justpy as jp

input_classes = "m-2 bg-gray-200 border-2 border-gray-200 rounded w-64 py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-purple-500"

async def input_demo(request):
    wp = jp.WebPage()
    in1 = jp.Input(a=wp, classes=input_classes, placeholder='Please type here')
    return wp

jp.justpy(input_demo)
```

## The input event

The program above is quite boring, it does nothing except allow you to type text into the input field. To make it more more interesting, let's have what we type reflected in a paragraph on the page. For this, we need to introduce the `input` event. When you type, each character typed into the input field generates an `input` event (yes, the tag and the event are called the same name, don't blame me). 

Run the following program:

```python
import justpy as jp

input_classes = "m-2 bg-gray-200 border-2 border-gray-200 rounded w-64 py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-purple-500"
p_classes = 'm-2 p-2 h-32 text-xl border-2'

async def my_input(self, msg):
    self.div.text = self.value

async def input_demo(request):
    wp = jp.WebPage()
    in1 = jp.Input(a=wp, classes=input_classes, placeholder='Please type here')
    in1.div = jp.Div(text='What you type will show up here', classes=p_classes, a=wp)
    in1.on('input', my_input)
    return wp

jp.justpy(input_demo)
```

The function input_demo creates a web page and adds an input element called `in1` to it (ignore the classes, they are there just to make the input element look nicer and do not affect the functionality of the program). Notice the `placeholder` attribute of `in1`. Before any text is typed into the input field or when it is emptied, the placeholder text is displayed in the field. We then define a div element that is added to the page (using the `a` keyword argument) and assigned to an attribute of in1. We saw this technique before. It simplifies event handling as we shall see in a second. Next, we bind the input event of `in1` to the function `my_input` (we could have omitted this line by adding `input=my_input` as a keyword argument when we created in1). `my_input` is therefore now the input event handler for `in1`.

The input event occurs each and every time a character is typed into an input element. After every keystroke this function is run, and it updates the text of the div to be the value of the input field.  By assigning the div to an `in1` attribute, we have access to all the variables we need in the event handler.

You may have noticed that there is a delay in the updating of the Div. That is because the component by default sets the `debounce` attribute of the input event to 200ms. This means an input event is generated only after a key has not been pressed for 200ms. Try holding the a key down and have it repeated. Only when you lift your finger will the Div update. You can set the `debounce` attribute to the value you prefer, just make sure to take into account the typing speed of your users and the latency of the connection. In general, a higher debounce value means the server will have to handle less communications and that may be an advantage for applications that need to scale.

## The Type Attribute

### Number Example

The input component can be of different [types](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#%3Cinput%3E_types) such as 'number' or  'password'.

```python
import justpy as jp

input_classes = "m-2 bg-gray-200 border-2 border-gray-200 rounded w-64 py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-purple-500"
p_classes = 'm-2 p-2 h-32 text-xl border-2'

async def my_input(self, msg):
    self.div.text = self.value

async def input_demo(request):
    wp = jp.WebPage()
    in1 = jp.Input(type='number', a=wp, classes=input_classes, placeholder='Please type here')
    in1.div = jp.Div(text='What you type will show up here', classes=p_classes, a=wp)
    in1.on('input', my_input)
    return wp

jp.justpy(input_demo)
```

In the example above the type of `in1` is set to 'number'. Run the program and verify that only numbers can be input into the element.

### Color Example

The Input component also allows you to choose colors.

```python
import justpy as jp

def color_demo(request):
    wp = jp.WebPage()
    in1 = jp.Input(type='color', a=wp, classes='m-2 p-2', style='width: 100px; height: 100px', input=color_change, debounce=30)
    in1.d = jp.Div(text='Click box above to change color of this text', a=wp, classes='border m-2 p-2 text-2xl font-bold')
    return wp

def color_change(self, msg):
    self.d.style=f'color: {self.value}'
    self.d.text = f'The color of this text is: {self.value}'

jp.justpy(color_demo)
```

### Radio Button Example

In the example below we create two sets of [radio buttons](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/radio).

Later in the tutorial we will see how to create a component for radio buttons which is a more intuitive way to use them. 

?> If you plan to use Quasar with JustPy, checkout the [QOptionGroup component](https://quasar.dev/vue-components/option-group)

```python
import justpy as jp

def radio_test():
    wp = jp.WebPage()
    genders = ['male', 'female', 'other']
    ages = [(0, 30), (31, 60), (61, 100)]

    outer_div = jp.Div(classes='border m-2 p-2 w-64', a=wp)

    jp.P(a=outer_div, text='Please select your gender:')
    for gender in genders:
        label = jp.Label(classes='inline-block mb-1 p-1', a=outer_div)
        radio_btn = jp.Input(type='radio', name='gender', value=gender, a=label)
        jp.Span(classes='ml-1', a=label, text=gender.capitalize())

    jp.Div(a=outer_div, classes='m-2')  # Add spacing and line break
    jp.P(a=outer_div, text='Please select your age:')
    for age in ages:
        label = jp.Label(classes='inline-block mb-1 p-1', a=outer_div)
        radio_btn = jp.Input(type='radio', name='age', value=age[0], a=label)
        jp.Span(classes='ml-1', a=label, text=f'{age[0]} - {age[1]}')
        jp.Br(a=outer_div)

    return wp

jp.justpy(radio_test)

```

Radio buttons respond to the 'change' event. When one is checked, JustPy automatically un-checks the other radio buttons in the group.

In the example below, the result of clicking a radio button are shown using the event handler `radio_changed`. Notice that the value of the radio button is always the same. What changes is its `checked` property. The value of a group of radio buttons is the value of the radio button in the group that is checked.

To make all the radio buttons in the group available to the event handler, when we create them, we also create a list that holds all the radio buttons in the group. We assign this list to an attribute of each radio button element (in our case `btn_list`). In the event handler we iterate over this list to report which radio button is pressed.


```python
import justpy as jp


def radio_changed(self, msg):
    self.result_div.text = ''
    d = jp.Div(a=self.result_div, classes='m-2 p-2 border')
    for btn in self.btn_list:
        if btn.checked:
            jp.Span(text=f'{btn.value} is checked', a=d, classes='text-green-500 mr-6')
        else:
            jp.Span(text=f'{btn.value} is NOT checked', a=d, classes='text-red-500 mr-6')


def radio_test():
    wp = jp.WebPage()
    genders = ['male', 'female', 'other']
    ages = [(0, 30), (31, 60), (61, 100)]

    outer_div = jp.Div(classes='border m-2 p-2 w-64', a=wp)
    # Create div to show radio button selection but don't add yet to page. It will be added at the end
    # It is created here so that it could be assigned to the radio button attribute result_div
    result_div = jp.Div(text='Click radio buttons to see results here', classes='m-2 p-2 text-xl')

    jp.P(a=outer_div, text='Please select your gender:')
    gender_list = []
    for gender in genders:
        label = jp.Label(classes='inline-block mb-1 p-1', a=outer_div)
        radio_btn = jp.Input(type='radio', name='gender', value=gender, a=label, btn_list=gender_list,
                             result_div=result_div, change=radio_changed)
        gender_list.append(radio_btn)
        jp.Span(classes='ml-1', a=label, text=gender.capitalize())

    jp.Div(a=outer_div, classes='m-2')  # Add spacing and line break

    jp.P(a=outer_div, text='Please select your age:')
    age_list = []
    for age in ages:
        label = jp.Label(classes='inline-block mb-1 p-1', a=outer_div)
        radio_btn = jp.Input(type='radio', name='age', value=age[0], a=label, btn_list=age_list,
                             result_div=result_div, change=radio_changed)
        age_list.append(radio_btn)
        jp.Span(classes='ml-1', a=label, text=f'{age[0]} - {age[1]}')
        jp.Br(a=outer_div)

    wp.add(result_div)
    return wp

jp.justpy(radio_test)
``` 

### Checkbox Example

Below is an example of a checkbox and a textbox connected using the `model` attribute

```python
import justpy as jp

def check_test():
    wp = jp.WebPage(data={'checked': True})
    label = jp.Label(a=wp, classes='m-2 p-2 inline-block')
    c = jp.Input(type='checkbox', classes='m-2 p-2 form-checkbox', a=label, model=[wp, 'checked'])
    caption = jp.Span(text='Click to get stuff', a=label)

    in1 = jp.Input(model=[wp, 'checked'], a=wp, classes='border block m-2 p-2')
    return wp

jp.justpy(check_test)
```

See what happens when you clear the text input element.

## Your First Component

JustPy allows building your own reusable components. We will have a lot more to say about this later, but just to start easing into the subject, let's suppose we want to encapsulate the functionality above into one component. The program would look like this:

```python
import justpy as jp

class InputWithDiv(jp.Div):

    @staticmethod
    def input_handler(self, msg):
        self.div.text = self.value

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        input_classes = "m-2 bg-gray-200 border-2 border-gray-200 rounded w-64 py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-purple-500"
        self.in1 = jp.Input(a=self, classes=input_classes, placeholder='Please type here', input=self.input_handler)
        self.in1.div = jp.Div(text='What you type will show up here', classes='m-2 p-2 h-32 text-xl border-2', a=self)


async def input_demo(request):
    wp = jp.WebPage()
    for i in range(10):
        InputWithDiv(a=wp)
    return wp

jp.justpy(input_demo)
```

Try running the program. It will put on the page 10 pairs of input and div elements. If you type into the respective input field, the text will show up in the respective div.

JustPy components are Python classes that inherit from JustPy classes. In the example above, we define the class `InputWithDiv` which inherits from the JustPy class `Div`. The class constructor adds an input element and another div to the basic div, with the appropriate functionality. Now, we have a component, `InputWithDiv`, that we can reuse as we please in any project. 

If you don't completely understand what is going on, don't worry. We will revisit this in much more detail later. The take home message at this stage is that the way you build complex applications in JustPy is by building components with isolated functionality. Hopefully, if  JustPy gains popularity, there will be many components that the community will develop and share. 
