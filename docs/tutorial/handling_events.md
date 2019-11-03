# Handling Events
In this part of the tutorial we will learn how to deal with user generated events such as a mouse click. JustPy deals with such events by binding a function to an event occurrence on the object. Please run the following program and click on 'Not clicked yet':

```python
import justpy as jp

def my_click(self, msg):
    self.text = 'I was clicked'

def event_demo():
    wp = jp.WebPage()
    d = jp.Div(text='Not clicked yet', classes='w-48 text-xl m-2 p-1 bg-blue-500 text-white', a=wp)
    d.on('click', my_click)
    return wp

jp.justpy(event_demo)
```

In `event_demo`, we first create a web page. Then we create a [Div](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/div) element named `d` whose content is the string 'Not clicked yet' (we also add some Tailwind classes for formatting). Then, using the `on` method, we bind the function `my_click`, which we defined earlier, to the click event and return the page. When the the element on the page is clicked, JustPy runs the function `my_click`.

Functions that deal with events such as `my_click`, must have two arguments. The first (self in our case), is the object for which the event occurred, in our case the object d, an instance of the class Div. The second parameter (msg in our case) is a dictionary that contains information about the event. The items in this dictionary can also be accessed using attribute (dot) notation. To get the event type for example we could write either  `msg['event_type']` or `msg.event_type`. In the program below I have added some print commands to the my_click function. Run it and see what is printed to the console.
```python
import justpy as jp

def my_click(self, msg):
    self.text = 'I was clicked'
    print(msg.event_type)
    print(msg['event_type'])
    print(msg)

def event_demo():
    wp = jp.WebPage()
    d = jp.P(text='Not clicked yet', classes='text-xl m-2 p-2 bg-blue-500 text-white', a=wp)
    d.on('click', my_click)
    return wp

jp.justpy(event_demo)
```

It could get a little verbose and may make the code less readable when you need to define a function for just a small number of lines of code. JustPy provides 'syntactic sugar' that allows writing the above with less lines of code and without needing to define my_click explicitly:

import justpy as jp

def event_demo():
    wp = jp.WebPage()
    jp.P(text='Not clicked yet', classes='text-xl m-2 p-2 bg-blue-500 text-white', a=wp,
         click="self.text = 'I was clicked'; print(msg.event_type); print(msg['event_type']); print(msg)")
    return wp

jp.justpy(event_demo)

The click keyword argument can either be a string like in the example above in which case it is taken to be a string of python commands in a function that has received two arguments: self and msg. That function is then bound to the click event. If the parameter is a function, that function is bound to the click event. In the previous example we could have written click=my_click and saved ourselves the d.on('click', my_click) line. Instead of click you can use onclick or, on_click. All three options work.
Of course, events other than click are also supported. Here is an example that includes the mouseenter and mouseleave events:
import justpy as jp

def event_demo():
    wp = jp.WebPage()
    jp.P(text='Not clicked yet', classes='w-64 text-xl text-center m-2 p-2 bg-blue-500 text-white', a=wp,
         click="self.text = 'I was clicked'; self.set_class('bg-red-500')",
         mouseenter="self.text = 'Mouse In!'",
         mouseleave="self.text = 'Mouse Out!'")
    return wp

jp.justpy(event_demo)

The above example also introduces the set_class method. This method knows which Tailwind classes logically cannot co-exist and removes the appropriate classes while adding the class provided as parameter. In the case above, the background can only be one color so the set_class method removes the class bg-blue-500 and adds the class bg-red-500.
In many cases it is convenient to share an event function among several elements. Please run the example below:
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

This program creates 25 buttons on each page. Under the buttons is a message box that provides information about which button was clicked and how many times it was clicked (try clicking the same button several times and see the change in the message box). 
Let's delve into the program in more detail. The program has two functions. The function event_demo creates the page and returns it when a page is requested. The function button_click will be bound to the click event of all the buttons.
In the first line of event_demo, the number of buttons is set (try changing this number and see what happens).  The second line creates a web page. The third line creates a div element (the general purpose HTML container element) named button_div. We will use it shortly to contain all the buttons. Notice that using a=wp we add button_div to the page. The fourth line defines the classes that will be used to format all the buttons. Don't worry if you don't understand what all the Tailwind classes do at this stage, it is not important. The fifth line creates the message element and adds it to the page.
On the sixth line  the loop that creates all the buttons starts. For each iteration of the loop, a button is created and added to button_div. Since button_div was previously added to the web page, the buttons will also be displayed on the page. A button in JustPy is just an instance of the Button class, and therefore we can assign user defined attributes to the instance. That is what we do in the next two lines. We assign to the message attribute the message element and initialize the num_clicked attribute to 0 (these attributes will be used in the button_click function as we shall see shortly).
After the loop, the web page is returned, and the framework renders it to the user's browser.
It may seem that the loop is erasing previous buttons by redefining the variable b. That is not the case because each time through the loop a new button is created and is added to the component list of button_div. At the end of the loop, button_div has 25 distinct child components. You can verify this by adding the following two line just before the return statement of event_demo and re-running the program:
print(button_div)
print(button_div.components)

Let's take a look now at button_click, the second function in our program. When any one of the buttons is clicked, this is the function that is executed. The arguments for button_click are the same as those for all event handlers in JustPy. The first argument self, is the button. In JustPy, elements on the page are represented by instances of Python classes. The buttons we created are instances of the Button class and therefore in our case self will be an instance of the Button class. 
In the first line of button_click we increment the instance attribute that tracks the number of times the specific button was clicked. It was initialized as 0 when we created the button in event_demo. The second line changes the text of the message box. Since we conveniently assigned the appropriate div element to the message attribute of all buttons, we know where to find it. It is right there as an attribute of self.
Please skip this paragraph if you are not familiar with JavaScript: Contrast this with the JavaScript methods of getting elements by id or class or using some sophisticated DOM query. Because Python classes are much more versatile than HTML elements, in most cases we don't need to query the DOM or its Python representation if we anticipate in advance which elements an event handler needs.
The last two lines of button_click change the background of the button that was clicked to red and change the background of the button when it is hovered.  
As the program is written now, once a button is clicked its background will always be red, even if another button is clicked. What needs to be done if we want only the background of the last clicked button to be red? The event handler needs to set the background of all other buttons back to blue. There are many ways that this could be done but I would like to highlight a method that can be generalized to most cases. The web page itself is an instance of a Python class and therefore can have user specified attributes. We will create a list of all the buttons and assign it to the button_list attribute of the page. In the event handler we will loop over this list and change the backgrounds to blue after which we will set the background of the clicked button to red. We know which page's button_list we need to loop over because the page on which the event originated is provided to the event handler by the msg.page field.
The result looks like this:
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

Events can also change the elements on the page itself, adding or removing them as necessary. As a concrete example let's change the program above to display a log of buttons that were clicked instead of just a one line of information.
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

Instead of just changing the text in message, button_click creates a p element with the text message and adds the element to message using add_component which we are introducing here. It is different from add because it allows adding a component at any position. Here, we are adding the new log info at the beginning of the message div so that most recent messages show up first. Also, in event_demo we changed message to a div element and added the first message as a p element with text. 

