# Input

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

## Example

This program is quite boring, it does nothing except allow you to type text into the input field. To make it more more interesting, let's have what we type reflected in a paragraph on the page. For this, we need to introduce the `input` event. When you type, each character typed into the input field generates an `input` event (yes, the tag and the event are called the same name, don't blame me). 

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

## The Type Attribute

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
