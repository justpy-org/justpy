# Creating Your Own Components

The idea behind component programming is simple and compelling: Build a component once, and then reuse it either in the same application or in different applications.

In JustPy, components are Python classes and so are custom components. Creating a component in JustPy means in most cases declaring a new Python class. In some cases, developing complex JustPy components requires also developing a [Vue.js](https://vuejs.org/) component. For example, the `HighCharts` charting component required developing a Vue.js component. For JustPy to support [Quasar](https://quasar.dev/) components, a Vue.js component was also required. It turns out that all Quasar components can be supported with one Vue.js component and that simplified matters considerably.

However, let's start with the basics. Most components require only writing a Python class and no knowledge of Vue.js or JavaScript is required.

Some components described here have features that are covered in other parts of the tutorial. Don't feel the need to finish this section in one go. If you find you need to go to other sections and return later, please do so.

## Pill Button Component

Our first component is a very simple one. It is a Button that is formatted to look like a [pill](https://tailwindcss.com/components/buttons#pill).

### Custom Component PillButton - Button looking like a pill
[PillButton live demo]({{demo_url}}/custom_comp_test1)

```python
import justpy as jp

class PillButton(jp.Button):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_classes('bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-full')


def custom_comp_test1():
    wp = jp.WebPage()
    for i in range(5):
        PillButton(text='Pill Button', click='self.text="I was clicked"', a=wp, classes='m-2')
    return wp

jp.justpy(custom_comp_test1)
```

Our new component, PillButton, inherits from Button and therefore will have all the attributes and functionality of Button.

The only change we make is to redefine `__init__`, the method that is called when an instance is created. In this case the method calls the `__init__` of the super class (Button in our case) and then sets the classes that format the button.

!!! warning
    The line `super().__init__(**kwargs)` is a **MUST** in component's `__init__`  
Without it, the instances of the components will not be created correctly. In most cases, only default values for keyword arguments should precede it.

Let's add a custom attribute to the component that will determine the background color of the button.

### Custom Component PillButton  with background color attribute
[PillButton with color live demo]({{demo_url}}/custom_comp_test2)

```python
import justpy as jp

class PillButton(jp.Button):

    def __init__(self, **kwargs):
        self.bg_color = 'blue'
        super().__init__(**kwargs)
        self.set_classes(f'bg-{self.bg_color}-500 hover:bg-{self.bg_color}-700 text-white font-bold py-2 px-4 rounded-full')

def custom_comp_test2():
    wp = jp.WebPage()
    for color in ['blue', 'red', 'yellow', 'pink']:
        PillButton(bg_color=color, text='Pill Button', click='self.text="I was clicked"', a=wp, classes='m-2')
    return wp

jp.justpy(custom_comp_test2)
```

When we create the PillButton instances we set the attribute `bg_color`. Each of the four PillButton instances will have a different background color.

Notice that the default for `bg_color` is 'blue' and it is set before the line `super().__init__(**kwargs)`. This allows it to be overwritten by the keyword arguments. Try moving the line setting the default after the line calling the super and see what happens.

Instead of setting the defaults for your attributes in `__init__` you can set a class attribute like so:
```python
class PillButton(jp.Button):

    bg_color = 'blue'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_classes(f'bg-{self.bg_color}-500 hover:bg-{self.bg_color}-700 text-white font-bold py-2 px-4 rounded-full')

```

Both methods work the same as Python uses the class attribute if it does not find an instance attribute.


## Alert Component
[Alert Component live demo]({{demo_url}}/alert_test1)

This component is based on this [example](https://tailwindcss.com/components/alerts/#top-accent-border) from the Tailwind documentation.

The HTML the component is based on looks like this:
```python
html_string = """
<div class="bg-teal-100 border-t-4 border-teal-500 rounded-b text-teal-900 px-4 py-3 shadow-md" role="alert">
  <div class="flex">
    <div class="py-1">
    <svg class="fill-current h-6 w-6 text-teal-500 mr-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
    <path d="M2.93 17.07A10 10 0 1 1 17.07 2.93 10 10 0 0 1 2.93 17.07zm12.73-1.41A8 8 0 1 0 4.34 4.34a8 8 0 0 0 11.32 11.32zM9 11V9h2v6H9v-4zm0-6h2v2H9V5z"/></svg>
    </div>
    <div>
      <p class="font-bold">Our privacy policy has changed</p>
      <p class="text-sm">Make sure you know how these changes affect you.</p>
    </div>
  </div>
</div>
"""
```

We will use [`parse_html`](../working_with_html?id=the-parse_html-function) to easily convert this to JustPy commands.

Run the following program. As it does not start a web server, there is no need to load a web page. We will be interested only in the printout.

```python
import justpy as jp

# Example based on https://tailwindcss.com/components/alerts/#top-accent-border
html_string = """
<div class="bg-teal-100 border-t-4 border-teal-500 rounded-b text-teal-900 px-4 py-3 shadow-md" role="alert">
  <div class="flex">
    <div class="py-1">
    <svg class="fill-current h-6 w-6 text-teal-500 mr-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
    <path d="M2.93 17.07A10 10 0 1 1 17.07 2.93 10 10 0 0 1 2.93 17.07zm12.73-1.41A8 8 0 1 0 4.34 4.34a8 8 0 0 0 11.32 11.32zM9 11V9h2v6H9v-4zm0-6h2v2H9V5z"/></svg>
    </div>
    <div>
      <p class="font-bold">Our privacy policy has changed</p>
      <p class="text-sm">Make sure you know how these changes affect you.</p>
    </div>
  </div>
</div>
"""

d = jp.parse_html(html_string)
for c in d.commands:
    print(c)
```

The printout is the following:
```python
root = jp.Div(name='root')
c1 = jp.Div(classes='bg-teal-100 border-t-4 border-teal-500 rounded-b text-teal-900 px-4 py-3 shadow-md', role='alert', a=root)
c2 = jp.Div(classes='flex', a=c1)
c3 = jp.Div(classes='py-1', a=c2)
c4 = jp.Svg(classes='fill-current h-6 w-6 text-teal-500 mr-4', xmlns='http://www.w3.org/2000/svg', viewBox='0 0 20 20', a=c3)
c5 = jp.Path(d='M2.93 17.07A10 10 0 1 1 17.07 2.93 10 10 0 0 1 2.93 17.07zm12.73-1.41A8 8 0 1 0 4.34 4.34a8 8 0 0 0 11.32 11.32zM9 11V9h2v6H9v-4zm0-6h2v2H9V5z', a=c4)
c6 = jp.Div(a=c2)
c7 = jp.P(classes='font-bold', a=c6, text='Our privacy policy has changed')
c8 = jp.P(classes='text-sm', a=c6, text='Make sure you know how these changes affect you.')
```

These are the JustPy commands required to duplicate the elements defined in the HTML. We are now are ready to define our component. We will call it `MyAlert`.

```python
import justpy as jp

class MyAlert(jp.Div):

    def __init__(self, **kwargs):
        self.title_text = 'This is the title'
        self.body_text = 'This is the body'
        super().__init__(**kwargs) # Important! see below
        root = self
        c1 = jp.Div(classes='bg-teal-100 border-t-4 border-teal-500 rounded-b text-teal-900 px-4 py-3 shadow-md',
                    role='alert', a=root)
        c2 = jp.Div(classes='flex', a=c1)
        c3 = jp.Div(classes='py-1', a=c2)
        c4 = jp.Svg(classes='fill-current h-6 w-6 text-teal-500 mr-4', xmlns='http://www.w3.org/2000/svg',
                    viewBox='0 0 20 20', a=c3)
        c5 = jp.Path(
            d='M2.93 17.07A10 10 0 1 1 17.07 2.93 10 10 0 0 1 2.93 17.07zm12.73-1.41A8 8 0 1 0 4.34 4.34a8 8 0 0 0 11.32 11.32zM9 11V9h2v6H9v-4zm0-6h2v2H9V5z',
            a=c4)
        c6 = jp.Div(a=c2)
        c7 = jp.P(classes='font-bold text-lg', a=c6, text=self.title_text)
        c8 = jp.P(classes='text-sm', a=c6, text=self.body_text)

def alert_test1():
    wp = jp.WebPage()
    d = MyAlert(a=wp, classes='m-2 w-1/4', title_text='hello', body_text='How is everybody?')
    d.title_text = 'Shalom'
    return wp

jp.justpy(alert_test1)
```

!!! warning
    The line `super().__init__(**kwargs)` is a **MUST** in custom component's `__init__`  
Without it, the instances of the components will not be created correctly. Only default values for keyword arguments should precede it.

When you run the program above, notice that the title of the MyAlert instance is rendered as 'Hello' instead of 'Shalom' even though the line `d.title_text = 'Shalom'` is executed after it is created (this problem also exists with the PillButton component we defined above). To fix this bug we need to assign the attributes `title_text` and `body_text` to the text of the appropriate elements when the instance is rendered, not when it is created.

!!! note
    As part of the rendering process, JustPy converts class instances to a Python dictionary representation that will later be sent as JSON to the web page and will be the input to the Vue.js frontend. This is done using the `convert_object_to_dict` method that each component class has.

## The react Method
[The React Method live demo]({{demo_url}}/alert_test2)

Every JustPy component supports the `react` method. It is run just just before a class instance is converted to a dictionary. It receives two arguments, the instance and the `data` attribute of its parent element or that of the `WebPage` if it has no parent. In base JustPy elements, `react` does nothing. It is there to be overridden in user defined components.

The modified program looks like this:

```python
import justpy as jp

class MyAlert(jp.Div):

    def __init__(self, **kwargs):
        self.title_text = 'This is the title'
        self.body_text = 'This is the body'
        super().__init__(**kwargs)
        root = self
        c1 = jp.Div(classes='bg-teal-100 border-t-4 border-teal-500 rounded-b text-teal-900 px-4 py-3 shadow-md',
                    role='alert', a=root)
        c2 = jp.Div(classes='flex', a=c1)
        c3 = jp.Div(classes='py-1', a=c2)
        c4 = jp.Svg(classes='fill-current h-6 w-6 text-teal-500 mr-4', xmlns='http://www.w3.org/2000/svg',
                    viewBox='0 0 20 20', a=c3)
        c5 = jp.Path(
            d='M2.93 17.07A10 10 0 1 1 17.07 2.93 10 10 0 0 1 2.93 17.07zm12.73-1.41A8 8 0 1 0 4.34 4.34a8 8 0 0 0 11.32 11.32zM9 11V9h2v6H9v-4zm0-6h2v2H9V5z',
            a=c4)
        c6 = jp.Div(a=c2)
        c7 = jp.P(classes='font-bold text-lg', a=c6, text=self.title_text)
        c8 = jp.P(classes='text-sm', a=c6, text=self.body_text)
        self.title_p = c7
        self.body_p = c8

    def react(self, data):
        self.title_p.text = self.title_text
        self.body_p.text = self.body_text
        self.text = ''


greetings = ['Bonjour', 'Hola', 'Zdravstvuyte', 'Nǐn hǎo', 'Salve', 'Konnichiwa', 'Guten Tag', 'Olá', 'Anyoung haseyo',
             'Asalaam alaikum', 'Goddag', 'Shikamoo', 'Goedendag', 'Yassas', 'Dzień dobry', 'Selamat siang', 'Namaste',
             'Merhaba', 'Shalom', ' God dag']


def translate(self, msg):
    self.title_text = 'Hello'

def alert_test2():
    wp = jp.WebPage()
    for greeting in greetings:
        d = MyAlert(a=wp, classes='m-2 w-1/4', title_text='hello', body_text='How is everybody?')
        d.on('click', translate)
        d.title_text = greeting
    return wp


jp.justpy(alert_test2)
```

At the end of `__init__` we added the two lines:
```python
self.title_p = c7
self.body_p = c8
```

These two attributes now hold the paragraphs where the title and body will be placed.
In the `react` method, the `text` attributes of the paragraphs are set. Just as a precaution, the `text` attribute of the parent element is set to the empty string (if it is not empty, the text will be rendered and the result will not be what we want).

In the request handler, `alert_test`, we use the new component to render alerts with greetings in different languages. We also added an event handler for the mouse click that changes the title to "Hello".

We now have a component, `MyAlert` that we can reuse as we please in any project (and of course share with our fellow programmers).

## Date Card Component
[Date Card Component live demo]({{demo_url}}/custom_comp_test3)

Here is an example of a simple date card component based on [this](https://tailwindcomponents.com/component/calendar-date) design.

### CalendarDate custom component
```python
import justpy as jp

class CalendarDate(jp.Div):

    def __init__(self, **kwargs):
        self.month = 'Jan'
        self.year = '2010'
        self.weekday = 'Sun'
        self.day = '1'
        self.color = 'red'
        super().__init__(**kwargs)
        self.inner_html = f"""
        <div class="w-24 rounded-t overflow-hidden bg-white text-center m-2 cursor-default">
            <div class="bg-{self.color}-500 text-white py-1">
                {self.month}
            </div>
            <div class="pt-1 border-l border-r">
                <span class="text-4xl font-bold">{self.day}</span>
            </div>
            <div class="pb-2 px-2 border-l border-r border-b rounded-b flex justify-between">
                <span class="text-xs font-bold">{self.weekday}</span>
                <span class="text-xs font-bold">{self.year}</span>
            </div>
        </div>
        """

def custom_comp_test3():
    wp = jp.WebPage()
    year = 2019
    month = 'Feb'
    d = jp.Div(classes='flex flex-wrap', a=wp)
    for day in range(1,11):
        CalendarDate(day=day, month=month, year=year, color='teal', a=d, animation='bounceIn')
    d = jp.Div(classes='flex flex-wrap', a=wp)
    for day in range(5, 26):
        CalendarDate(day=day, month='Jul', year='2005', color='yellow', a=d)
    return wp

jp.justpy(custom_comp_test3)
```

In this custom component we are using the template like behavior of Python f-strings to create a date card with some features that can be changed. This simple component inherits from the component `Div`. It changes only the `__init__` method and inherits all the others.

Notice the `super().__init__(**kwargs)` line in `__init__`. It is required to take care of all the plumbing that goes along with a JustPy component. This line executes the `__init__` of `Div`.  We define the defaults for the component specific attributes before this line so as not to overwrite keyword arguments that the user has provided and are assigned to attributes in the superclass `__init__`.

This component works well enough but has a flaw. The `inner_html` attribute is set in `__init__` when the instance is created. If for example, the instance's `day` attribute is changed after `__init__` has run, it would not be reflected in the inner html and the component will not be rendered correctly.

To solve this problem, we need to move setting `inner_html` from the time the instance was created to the time it is rendered. Every JustPy component has a method called `react` that is called each time before the object is converted to a dict. The example above can therefore be written as follows:

### CalendarDate custom component using react
[CalendarDate custom component live demo]({{demo_url}}/custom_comp_test4)

```python
import justpy as jp

class CalendarDate(jp.Div):

    def __init__(self, **kwargs):
        self.month = 'Jan'
        self.year = '2010'
        self.weekday = 'Sun'
        self.day = '1'
        self.color = 'red'
        super().__init__(**kwargs)

    def react(self, data):
        self.inner_html = f"""
                        <div class="w-24 rounded-t overflow-hidden bg-white text-center m-2 cursor-default">
                            <div class="bg-{self.color}-500 text-white py-1">
                                {self.month}
                            </div>
                            <div class="pt-1 border-l border-r">
                                <span class="text-4xl font-bold">{self.day}</span>
                            </div>
                            <div class="pb-2 px-2 border-l border-r border-b rounded-b flex justify-between">
                                <span class="text-xs font-bold">{self.weekday}</span>
                                <span class="text-xs font-bold">{self.year}</span>
                            </div>
                        </div>
                        """


def custom_comp_test4():
    wp = jp.WebPage()
    year = 2019
    month = 'Feb'
    d = jp.Div(classes='flex flex-wrap', a=wp)
    for day in range(1,11):
        CalendarDate(day=day, month=month, year=year, color='teal', a=d, animation='bounceIn')
    d = jp.Div(classes='flex flex-wrap', a=wp)
    for day in range(5, 26):
        c = CalendarDate(day=day, month='Jul', year='2005', color='yellow', a=d)
        c.day += 1    # Notice how the date starts from 6 and not from 5.
    return wp

jp.justpy(custom_comp_test4)
```

The `react` method accepts an additional argument to self. The argument `data` is the `data` attribute of the element's direct parent. If the element has no parent, it is the `data` attribute of the page. Using `react` we can have child elements change their behavior when rendered based on the `data` attribute of their parent or the page they are on.

For example, let's make the color of the component dependent on the `data` attribute of their parent container.
### CalendarDate custom component color dependent on data attribute of parent container
[Color dependent CalendarDate custom component live demo]({{demo_url}}/custom_comp_test5)

```python
import justpy as jp

class CalendarDate(jp.Div):

    def __init__(self, **kwargs):
        self.month = 'Jan'
        self.year = '2010'
        self.weekday = 'Sun'
        self.day = '1'
        self.color = 'red'
        super().__init__(**kwargs)

    def react(self, data):
        self.inner_html = f"""
                        <div class="w-24 rounded-t overflow-hidden bg-white text-center m-2 cursor-default">
                            <div class="bg-{data['color']}-500 text-white py-1">
                                {self.month}
                            </div>
                            <div class="pt-1 border-l border-r">
                                <span class="text-4xl font-bold">{self.day}</span>
                            </div>
                            <div class="pb-2 px-2 border-l border-r border-b rounded-b flex justify-between">
                                <span class="text-xs font-bold">{self.weekday}</span>
                                <span class="text-xs font-bold">{self.year}</span>
                            </div>
                        </div>
                        """


def change_color(self, msg):
    self.d.data["color"] = self.value

def custom_comp_test5():
    wp = jp.WebPage()
    year = 2019
    month = 'Feb'
    d = jp.Div(classes='flex flex-wrap', a=wp, data={'color': 'purple'})
    for day in range(1,11):
        CalendarDate(day=day, month=month, year=year, color='teal', a=d)
    d = jp.Div(classes='flex flex-wrap', a=wp, data={'color': 'red'})
    for day in range(5, 26):
        c = CalendarDate(day=day, month='Jul', year='2005', color='yellow', a=d)
        c.day += 1    # Notice how the date starts from 6 and not from 5.
    colors = ['red', 'green', 'blue', 'pink', 'yellow', 'teal', 'purple']
    s = jp.Select(classes='w-32 text-xl m-2 p-2 bg-white  border rounded-full', a=wp, value='red',
                  change=change_color)
    s.d = d
    for color in colors:
        s.add(jp.Option(value=color, text=color, classes=f'bg-{color}-600'))
    return wp

jp.justpy(custom_comp_test5)
```

This example is a little more complex as we have added a [Select](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/select) component at the bottom of the page. Try changing the selected color. The color of the `CalendarDate` instances in the second group changes because in the event handler, `change_color` we change the `data` attribute of the parent Div, `d`.

The function `change_color` sets the value of the 'color' key in the data dictionary of the Div that holds the CalendarDate instances to the new value of the `Select` element. In this example, we changed the `react` function so it uses this value instead of `self.color` (which was used in the previous example) to set the color to display.

A few more words about Select: A Select component includes Option components. In this example we add them to the Select using a predefined list of colors. When a specific option is selected, its value attribute becomes the value attribute of the Select. The change in value is acted upon by binding a method to the change event of the Select instance.

## Hello Component
[Hello component live demo]({{demo_url}}/hello_test1)

JustPy comes with a simple Hello component, which we will now examine.

First run the following short program.

### 5 x times jp.Hello
```python
import justpy as jp

def hello_test1():
    wp = jp.WebPage()
    h = jp.Hello()
    for i in range(5):
        wp.add(h)
    return wp

jp.justpy(hello_test1)
```

The program puts five Hello elements on the page. Click any one of them. All five will show the number of times any element was clicked because each time through the loop, we add the same element to the page. There may be 5 rendered elements on the page, but for JustPy, these are the same element.

If we would like there to be independent components on the page, we would write the program in the following way:
### 5 x times jp.Hello as independent elements
[live demo]({{demo_url}}/hello_test2)

```python
import justpy as jp

def hello_test2():
    wp = jp.WebPage()
    for i in range(5):
        wp.add(jp.Hello()) # or jp.Hello(a=wp)
    return wp

jp.justpy(hello_test2)
```
In this program, each time thorough the loop we create a new Hello element and add it to the page. When any element is clicked, no other element on the page is affected.

Let's look more closely at the `Hello` component. This is the way it is defined:
```python
class Hello(Div):

    def __init__(self, **kwargs):
        self.counter = 1
        super().__init__(**kwargs)
        self.classes = 'm-1 p-1 text-2xl text-center text-white bg-blue-500 hover:bg-blue-800 cursor-pointer'
        self.text = 'Hello! (click me)'

        def click(self, msg):
            self.text = f'Hello! I was clicked {self.counter} times'
            self.counter += 1

        self.on('click', click)
```

Again, JustPy components are Python classes. In our case, `Hello` inherits from `Div` and only changes `Div`'s `__init__`.

In `__init__` we first initialize a counter for the instance. This is a new attribute that is not initialized by `Div`. Then we call the super class `__init__`, in our case the `__init__` of Div. This call provides `Hello` with the initializations required to work correctly inside the JustPy framework. Since we are calling the super class `__init__` after having provided a default value to the counter attribute, we can overwrite it with a keyword argument. Try running the following:

### 5 x times jp.Hello with a default counter value
[live demo]({{demo_url}}/hello_test3)

```python
import justpy as jp

def hello_test3():
    wp = jp.WebPage()
    for i in range(5):
        jp.Hello(a=wp, counter=100)
    return wp

jp.justpy(hello_test3)
```


Since `counter` is initialized to 100, the components will start counting from 100. The call to the super class `__init__` takes care of assigning the keyword arguments. If we had put the initialization of `counter` after the call to the super class `__init__`, the keyword argument would have had no effect.

Next, in the definition of `Hello`, we set the classes of the component to give it some basic design and we set the text. Then we define the click event handler and assign it to the instance. That's it.

Let's say we are not pleased with the Hello message and its colors and want to define a better Hello component. This is how we would do it:

### 5 x times customized MyHello based on jp.Hello
[live demo]({{demo_url}}/hello_test4)

```python
import justpy as jp

class MyHello(jp.Hello):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.classes = 'm-1 p-1 text-6xl text-center text-red-500 bg-yellow-500 hover:bg-yellow-800 cursor-pointer'
        self.text = 'Much Better Hello! (click me)'

def hello_test4():
    wp = jp.WebPage()
    for i in range(5):
        MyHello(a=wp, counter=100)
    return wp

jp.justpy(hello_test4)
```

We define a new component called `MyHello` which inherits from `Hello`. By running the super class `__init__` in the `__init__` of `MyHello`, we get all the functionality of `Hello`. We then just modify the classes and text.


## Calculator Component

### Base component
[live demo]({{demo_url}}/calculator_test1)

We will build a calculator component in stages. First, we will create a component that does not handle events or the model attribute. Please run the following example.
```python
import justpy as jp
from justpy import Div, Input, Button, WebPage, justpy

class Calculator(Div):

    btn_classes = 'w-1/4 text-xl font-bold p-2 m-1 border bg-gray-200 hover:bg-gray-700 shadow'
    layout_text = [['7', '8', '9', '*'], ['4', '5', '6', '-'], ['1', '2', '3', '+'], ['C', '0', '.', '=']]

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.value = 0
        self.tape = Input(classes='block p-2 m-2  border text-right text-sm bg-gray-200', a=self, readonly=True, value=' ', style='width: 90%')
        self.result = Input(classes='block p-2 m-2 border text-2xl text-right', a=self, readonly=True, value='0', style='width: 90%')
        for line in self.__class__.layout_text:
            d = Div(classes='flex w-auto m-2', a=self)
            for b in line:
                b1 = Button(text=b, a=d, classes=self.__class__.btn_classes, click=self.calculator_click)
                b1.calc = self

    @staticmethod
    def calculator_click(self, msg):
        calc = self.calc
        if self.text == 'C':
            calc.result.value = '0'
            calc.tape.value = ' '
            calc.value = 0
        elif self.text == '=':
            calc.result.value = str(eval(calc.tape.value))
            calc.value = eval(calc.tape.value)
            calc.tape.value = calc.result.value
        else:
            if calc.tape.value[-1] in '*+-/' or self.text in '*+-/':
                calc.tape.value += ' ' + self.text
            else:
                calc.tape.value += self.text
            try:
                calc.result.value = str(eval(calc.tape.value))
                calc.value = eval(calc.tape.value)
            except:
                pass


def calculator_test1():
    wp = WebPage()
    for i in range(10):
        c = Calculator(a=wp, classes='m-1 border inline-block', style='width: 250px')
    return wp

jp.justpy(calculator_test1)
```

First let's look at the function `calculator_test1`. This function creates a WebPage and adds ten instances of the Calculator component to it. Try changing the number of calculators on the page by changing the argument to range. Once a JustPy component has been defined, it is simple to reuse it. The Calculator component can be used now in multiple projects.

JustPy components are Python classes. The Calculator component is therefore a Python class. The Calculator class inherits from Div so Calculator is endowed from the start will all the features and capabilities of the Div component. These features are used in  `__init__`, in order to add the other components needed to implement the calculator.

The class `__init__` first calls the class `__init__` of the super class (in this case Div). If a class inherits from another JustPy component, you must run the `__init__` of the super class. It then sets the value attribute to 0 and adds two Input components, one for the tape and one for the result. The two Inputs are assigned to instance attributes for future reference and added to self (which is a Div and therefore other components can be added to it). The Inputs are also designated readonly so that the user cannot type in them.

After the two Input elements are added to the instance, two nested loops are used to add the calculator buttons based on the layout list which is a list of lists. Each child list represents a line of buttons. Each button is assigned the same click event handler, `self.calculator_click` which is a static method of the Calculator class (we could have defined the event handler inside the `__init__ `function instead). We also assign to the button `calc` attribute a reference to the Calculator instance of which the button is part of. This is used in the click event handler to set the value of the Calculator instance.

In this example, for the sake of brevity, we implemented a very simple state machine for the calculator that is not perfect (for example, it does not handle 0 in front of a number), but for our purposes, it will do. The state machine is inside the `calculator_click` event handler. All buttons on the calculator use the same event handler but it differentiates between the buttons based on `self.text` which is unique for each button.

### Handling the change event
[live demo]({{demo_url}}/calculator_test2)

As it is currently defined, Calculator does not support any useful events. We would like to add a meaningful change event to it. This event will fire when the value of the Calculator instance changes. We do this by modifying the click event handler of the buttons. The value of the Calculator instance does not change unless some button is clicked. We therefore check if the specific button click changed the value and if that is the case, we run the change event handler of the Calculator instance. This is how the result looks like:

```python
from justpy import Div, Input, Button, WebPage, justpy
import justpy as jp

class Calculator(Div):

    btn_classes = 'w-1/4 text-xl font-bold p-2 m-1 border bg-gray-200 hover:bg-gray-700 shadow'
    layout_text = [['7', '8', '9', '*'], ['4', '5', '6', '-'], ['1', '2', '3', '+'], ['C', '0', '.', '=']]

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.value = 0
        self.tape = Input(classes='block p-2 m-2  border text-right text-sm bg-gray-200', a=self, readonly=True, value=' ', style='width: 90%')
        self.result = Input(classes='block p-2 m-2 border text-2xl text-right', a=self, readonly=True, value='0', style='width: 90%')
        for line in type(self).layout_text:
            d = Div(classes='flex w-auto m-2', a=self)
            for b in line:
                b1 = Button(text=b, a=d, classes=type(self).btn_classes, click=self.calculator_click)
                b1.calc = self

    @staticmethod
    async def calculator_click(self, msg):
        calc = self.calc
        try:
            tape_value = eval(calc.tape.value)
        except:
            tape_value = 0
        changed = False
        if self.text == 'C':
            calc.result.value = '0'
            calc.tape.value = ' '
            if calc.value != 0:
                calc.value = 0
                changed = True
        elif self.text == '=':
            if calc.value != tape_value:
                calc.value = tape_value
                changed = True
            calc.result.value = str(tape_value)
            calc.tape.value = str(tape_value)
        else:
            if calc.tape.value[-1] in '*+-/' or self.text in '*+-/':
                calc.tape.value += ' ' + self.text
            else:
                calc.tape.value += self.text
            try:
                tape_value = eval(calc.tape.value)
                calc.result.value = str(tape_value)
                if calc.value != tape_value:
                    calc.value = tape_value
                    changed = True
            except:
                pass
        if changed:
            if calc.has_event_function('change'):
                calc_msg = msg
                calc_msg.event_type = 'change'
                calc_msg.id = calc.id
                calc_msg.button_text = self.text
                calc_msg.value = calc.value
                calc_msg.class_name = calc.__class__.__name__
                return await calc.run_event_function('change', calc_msg)


def calc_change(self, msg):
    print('In change')
    print(msg)
    self.d.text = self.value

def calculator_test2():
    wp = WebPage()
    c = Calculator(a=wp, classes='m-1 border inline-block', style='width: 250px', change=calc_change)
    d = Div(classes='border m-2 p-1 w-64 text-xl', text='0', a=wp)
    c.d = d
    return wp

jp.justpy(calculator_test2)
```

Run the program above. You will see that the value of the calculator is reflected in the Div below it since that is what we defined the change event handler to do.

In the click event handler we use a flag called `changed` that is set to `True` by the state machine logic if an operation that changes the value of the calculator occurs.

At the end of the event handler, we check if `changed` is `True`. If it is, we check whether the instance has a change event handler. We do this by using the method `has_event_function` which is a basic method of all JustPy components.

If there is a change event handler, we run the event handler using the `run_event_function` method which is also a basic method of all JustPy components.

This method takes two arguments in addition to `self`. The first is the event type. The second, is the dictionary we want passed as the second positional argument to the event handler. This is what we usually designate as `msg` in our event handlers.

 Before calling `run_event_function` we modify some values in `msg` to make it more informative. In general, you would create the appropriate `msg` for how you believe the component will be used. In our case we have added the `button_text` key which stores the text of the last button that was clicked and that generated the change event.

!!! note
    Please note that `run_event_function` is an async method and therefore since `calculator_click` awaits it, it needs to be a coroutine also and is defined using async.

### Adding a model attribute
[live demo]({{demo_url}}/calculator_test3)

To make Calculator complete, we will also add handling of the `model` attribute to it. This is quite simple in our case. First, we need to remember that Calculator inherits from Div and is a derived (child) class of Div. The Div model_update method sets the Div instance's text attribute to the model. Therefore, we need to override it to do nothing so we don't see the value as text at the top of the calculator. Try removing the `model_update` method from the example below and see what happens.

```python
from justpy import Div, Input, Button, WebPage, justpy
import justpy as jp

class Calculator(Div):

    btn_classes = 'w-1/4 text-xl font-bold p-2 m-1 border bg-gray-200 hover:bg-gray-700 shadow'
    layout_text = [['7', '8', '9', '*'], ['4', '5', '6', '-'], ['1', '2', '3', '+'], ['C', '0', '.', '=']]

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.value = 0
        self.tape = Input(classes='block p-2 m-2  border text-right text-sm bg-gray-200', a=self, readonly=True, value=' ', style='width: 90%')
        self.result = Input(classes='block p-2 m-2 border text-2xl text-right', a=self, readonly=True, value='0', style='width: 90%')
        for line in type(self).layout_text:
            d = Div(classes='flex w-auto m-2', a=self)
            for b in line:
                b1 = Button(text=b, a=d, classes=type(self).btn_classes, click=self.calculator_click)
                b1.calc = self

    @staticmethod
    async def calculator_click(self, msg):
        calc = self.calc
        try:
            tape_value = eval(calc.tape.value)
        except:
            tape_value = 0
        changed = False
        if self.text == 'C':
            calc.result.value = '0'
            calc.tape.value = ' '
            if calc.value != 0:
                calc.value = 0
                changed = True
        elif self.text == '=':
            if calc.value != tape_value:
                calc.value = tape_value
                changed = True
            calc.result.value = str(tape_value)
            calc.tape.value = str(tape_value)
        else:
            if calc.tape.value[-1] in '*+-/' or self.text in '*+-/':
                calc.tape.value += ' ' + self.text
            else:
                calc.tape.value += self.text
            try:
                tape_value = eval(calc.tape.value)
                calc.result.value = str(tape_value)
                if calc.value != tape_value:
                    calc.value = tape_value
                    changed = True
            except:
                pass
        if changed:
            calc.set_model(calc.value)  #******************** updates model
            if calc.has_event_function('change'):
                calc_msg = msg
                calc_msg.event_type = 'change'
                calc_msg.id = calc.id
                calc_msg.button_text = self.text
                calc_msg.value = calc.value
                calc_msg.class_name = calc.__class__.__name__
                return await calc.run_event_function('change', calc_msg)

    def model_update(self):
        pass

def calculator_test3():
    wp = WebPage(data={'value': 0})
    Calculator(a=wp, classes='m-1 border inline-block', style='width: 250px', model=[wp, 'value'])
    for i in range(5):
        Div(classes='border m-2 p-1 w-64 text-xl', text='0', a=wp, model=[wp, 'value'])
    return wp

jp.justpy(calculator_test3)
```

Notice that we have added a call to the method `set_model` in the click event handler. This method checks if the component has a model attribute and if so, sets it to the method's argument.  

The `set_model` method is defined as follows:

```python
def set_model(self, value):
    if hasattr(self, 'model'):
        self.model[0].data[self.model[1]] = value
```

The `model` attribute, as we defined it above is one directional. The component only sets `model` value but does not change any of its other attribute values based on changes in `model`.

## Tab Group Component
[live demo]({{demo_url}}/tab_comp_test1)

This component allows inserting content in tabs and displaying it based on the tab selected.

If the `animation` attribute is set to `True`, the transition between tabs is animated. The type of animation and its speed can also be set.

A tab is added by calling the `add_tab` method. This method accepts three arguments (in addition to self). The first is the id of the tab. When the tab is selected, its value will become the id of the tab selected. Converesely, when the `value` attribute is set, if a tab with a corresponding id exists, it will be shown.

The second argument is the label to display for the tab's selection.

The third argument is the content of the tab.  Typically it would be a container element such as a Div instance that contains other elements.

In this component, the method `convert_object_to_dict`, is overridden. This is the method that executes each time an instance of the component is rendered. It is simpler in this case than using the `react` method that is called by the super class `convert_object_to_dict`. It also allows the flexibility of overriding the `react` method in components that inherit from the Tabs component.

Below we also define another component, TabPills, that inherits from Tabs and just changes the appearance of the tabs label line. It does so by just changing a few class variables.

!!! tip
    When creating custom components, it makes sense to make the design a function of class variables. This simplifies creating new components with a different design.

 In the example below we use three tab components to display charts and pictures.

```python
from justpy import Div, WebPage, Ul, Li, HighCharts, A, justpy
import justpy as jp


class Tabs(Div):

    tab_label_classes = 'overflow-hidden cursor-pointer bg-white inline-block py-2 px-4 text-blue-500 hover:text-blue-800 font-semibold'
    tab_label_classes_selected = 'overflow-hidden cursor-pointer bg-white inline-block border-l border-t border-r rounded-t py-2 px-4 text-blue-700 font-semibold'
    item_classes = 'flex-shrink mr-1'
    item_classes_selected = 'flex-shrink -mb-px mr-1'
    wrapper_style = 'display: flex; position: absolute; width: 100%; height: 100%;  align-items: center; justify-content: center; background-color: #fff;'

    def __init__(self, **kwargs):

        self.tabs = []  # list of {'id': id, 'label': label, 'content': content}
        self.value = None  # The value of the tabs component is the id of the selected tab
        self.content_height = 500
        self.last_rendered_value = None
        self.animation = False
        self.animation_next = 'slideInRight'
        self.animation_prev = 'slideOutLeft'
        self.animation_speed = 'faster'  # '' | 'slow' | 'slower' | 'fast'  | 'faster'

        super().__init__(**kwargs)

        self.tab_list = Ul(classes="flex flex-wrap border-b", a=self)
        self.content_div = Div(a=self)
        self.delete_list = []


    def __setattr__(self, key, value):
        if key == 'value':
            try:
                self.previous_value = self.value
            except:
                pass
        self.__dict__[key] = value

    def add_tab(self, id, label, content):
        self.tabs.append({'id': id, 'label': label, 'content': content})
        if not self.value:
            self.value = id

    def get_tab_by_id(self, id):
        for tab in self.tabs:
            if tab['id'] == id:
                return tab
        return None

    def set_content_div(self, tab):
        self.content_div.add(tab['content'])
        self.content_div.set_classes('relative overflow-hidden border')
        self.content_div.style = f'height: {self.content_height}px'

    def set_content_animate(self, tab):
        self.wrapper_div_classes = self.animation_speed  # Component in this will be centered

        if self.previous_value:
            self.wrapper_div = Div(classes=self.wrapper_div_classes, animation=self.animation_next, temp=True,
                                   style=f'{self.wrapper_style} z-index: 50;', a=self.content_div)
            self.wrapper_div.add(tab['content'])
            self.wrapper_div = Div(classes=self.wrapper_div_classes, animation=self.animation_prev, temp=True,
                                   style=f'{self.wrapper_style} z-index: 0;', a=self.content_div)
            self.wrapper_div.add(self.get_tab_by_id(self.previous_value)['content'])
        else:
            self.wrapper_div = Div(classes=self.wrapper_div_classes, temp=True, a=self.content_div,
                                   style=self.wrapper_style)
            self.wrapper_div.add(tab['content'])

        self.content_div.set_classes('relative overflow-hidden border')
        self.content_div.style = f'height: {self.content_height}px'


    def model_update(self):
        val = self.model[0].data[self.model[1]]
        if self.get_tab_by_id(val):
            self.value = val

    def delete(self):
        for c in self.delete_list:
            c.delete_flag = True
            c.delete()
            c.needs_deletion = False

        if self.delete_flag:
            for tab in self.tabs:
                tab['content'].delete()
                tab['content'] = None
        super().delete()

    @staticmethod
    async def tab_click(self, msg):
        if self.tabs.value != self.tab_id:
            previous_tab = self.tabs.value
            self.tabs.value = self.tab_id
            if hasattr(self.tabs, 'model'):
                self.tabs.model[0].data[self.tabs.model[1]] = self.tabs.value
            # Run change if it exists
            if self.tabs.has_event_function('change'):
                msg.previous_tab = previous_tab
                msg.new_tab = self.tabs.value
                msg.id = self.tabs.id
                msg.value = self.tabs.value
                msg.class_name = self.tabs.__class__.__name__
                return await self.tabs.run_event_function('change', msg)
        else:
            return True  # No need to update page

    def convert_object_to_dict(self):
        if hasattr(self, 'model'):
            self.model_update()
        self.set_classes('flex flex-col')
        self.tab_list.delete_components()
        self.content_div.components = []
        for tab in self.tabs:
            if tab['id'] != self.value:
                tab_li = Li(a=self.tab_list, classes=self.item_classes)
                li_item = A(text=tab['label'], classes=self.tab_label_classes, a=tab_li, delete_flag=False)
                self.delete_list.append(li_item)
            else:
                tab_li = Li(a=self.tab_list, classes=self.item_classes_selected)
                li_item = A(text=tab['label'], classes=self.tab_label_classes_selected, a=tab_li, delete_flag=False)
                self.delete_list.append(li_item)
                if self.animation and (self.value != self.last_rendered_value):
                    self.set_content_animate(tab)
                else:
                    self.set_content_div(tab)
            li_item.tab_id = tab['id']
            li_item.tabs = self
            li_item.on('click', self.tab_click)
        self.last_rendered_value = self.value
        d = super().convert_object_to_dict()

        return d


class TabsPills(Tabs):
    tab_label_classes = 'cursor-pointer inline-block border border-white rounded hover:border-gray-200 text-blue-500 hover:bg-gray-200 py-1 px-3'
    tab_label_classes_selected = 'cursor-pointer inline-block border border-blue-500 rounded py-1 px-3 bg-blue-500 text-white'
    item_classes = 'flex-shrink mr-3'
    item_classes_selected = 'flex-shrink -mb-px mr-3'


my_chart_def = """
{
        chart: {
            type: 'bar'
        },
        title: {
            text: 'Fruit Consumption'
        },
        xAxis: {
            categories: ['Apples', 'Bananas', 'Oranges']
        },
        yAxis: {
            title: {
                text: 'Fruit eaten'
            }
        },
        series: [{
            name: 'Jane',
            data: [1, 0, 4],
            animation: false
        }, {
            name: 'John',
            data: [5, 7, 3],
            animation: false
        }]
}
"""
# https://dog.ceo/api/breed/papillon/images/random
pics_french_bulldogs = ['5458', '7806', '5667', '4860']
pics_papillons = ['5037', '2556', '7606', '8241']

def tab_change(self, msg):
    print('in change', msg)

def tab_comp_test1():
    wp = jp.WebPage(data={'tab': 'id2556'})

    t = Tabs(a=wp, classes='w-3/4 m-4', style='', animation=True, content_height=550)
    for chart_type in ['bar', 'column', 'line', 'spline']:
        d = jp.Div(style=Tabs.wrapper_style, delete_flag=True)
        my_chart = jp.HighCharts(a=d, classes='m-2 p-2 border', style='width: 1000px;', options=my_chart_def, use_cache=False)
        my_chart.options.chart.type = chart_type
        my_chart.options.title.text = f'Chart of Type {chart_type.capitalize()}'
        my_chart.options.subtitle.text = f'Subtitle {chart_type.capitalize()}'
        t.add_tab(f'id{chart_type}', f'{chart_type}', d)

    d_flex = Div(classes='flex', a=wp)  # Container for the two dog pictures tabs

    t = Tabs(a=d_flex, classes=' w-1/2 m-4', animation=True, content_height=550, model=[wp, 'tab'], change=tab_change)
    for pic_id in pics_papillons:
        d = jp.Div(style=Tabs.wrapper_style)
        jp.Img(src=f'https://images.dog.ceo/breeds/papillon/n02086910_{pic_id}.jpg', a=d)
        t.add_tab(f'id{pic_id}', f'Pic {pic_id}', d)

    t = TabsPills(a=d_flex, classes='w-1/2 m-4', animation=True, content_height=550, change=tab_change)
    for pic_id in pics_french_bulldogs:
        d = jp.Div(style=Tabs.wrapper_style)
        jp.Img(src=f'https://images.dog.ceo/breeds/bulldog-french/n02108915_{pic_id}.jpg', a=d)
        t.add_tab(f'id{pic_id}', f'Pic {pic_id}', d)

    input_classes = "w-1/3 m-2 bg-gray-200 border-2 border-gray-200 rounded w-64 py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-purple-500"

    in1 = jp.Input(classes=input_classes, model=[wp, 'tab'], a=wp)

    return wp


jp.justpy(tab_comp_test1)
```

## Table Component
[live demo]({{demo_url}}/table_test)

The AutoTable component takes a list of lists and formats it into a nice looking table. The first list is used as the headers for the table.

In the example below, we read a CSV file into a pandas frame, convert it to a list of lists and add the column names as the first list and then use the component.

!!! note
    You need pandas installed to run the example below.

```python
import justpy as jp
import pandas as pd


class AutoTable(jp.Table):

    td_classes = 'border px-4 py-2 text-center'
    tr_even_classes = 'bg-gray-100 '
    tr_odd_classes = ''
    th_classes = 'px-4 py-2'

    def __init__(self, **kwargs):
        self.values = []
        super().__init__(**kwargs)


    def react(self,data):
        self.set_class('table-auto')
        #First row of values is header
        if self.values:
            headers = self.values[0]
            thead = jp.Thead(a=self)
            tr = jp.Tr(a=thead)
            for item in headers:
                jp.Th(text=item, classes=self.th_classes, a=tr)
            tbody = jp.Tbody(a=self)
            for i, row in enumerate(self.values[1:]):
                if i % 2 == 1:
                    tr = jp.Tr(classes=self.tr_even_classes, a=tbody)
                else:
                    tr = jp.Tr(classes=self.tr_odd_classes, a=tbody)
                for item in row:
                    jp.Td(text=item, classes=self.td_classes, a=tr)


wm_df = pd.read_csv('https://elimintz.github.io/women_majors.csv').round(2)
wm_df['Year'] = wm_df['Year'].astype('str')
headers = list(wm_df.columns)
table_data = wm_df.to_numpy().tolist()
table_data.insert(0, headers)

def table_test():
    wp = jp.WebPage()
    d = jp.Div(classes='w-7/8 m-2 p-3 border rounded-lg ', a=wp)
    AutoTable(values=table_data, a=d, classes='block p-4 overflow-auto', style='height: 90vh')
    return wp

jp.justpy(table_test)
```

## Quasar QInput Component with Integrated QDate and QTime
[live demo]({{demo_url}}/input_test)

```python
import justpy as jp

# https://quasar.dev/vue-components/date#With-QInput

class QInputDateTime(jp.QInput):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        date_slot = jp.QIcon(name='event', classes='cursor-pointer')
        c2 = jp.QPopupProxy(transition_show='scale', transition_hide='scale', a=date_slot)
        self.date = jp.QDate(mask='YYYY-MM-DD HH:mm', name='date', a=c2)

        time_slot = jp.QIcon(name='access_time', classes='cursor-pointer')
        c2 = jp.QPopupProxy(transition_show='scale', transition_hide='scale', a=time_slot)
        self.time = jp.QTime(mask='YYYY-MM-DD HH:mm', format24h=True, name='time', a=c2)

        self.date.parent = self
        self.time.parent = self
        self.date.value = self.value
        self.time.value = self.value
        self.prepend_slot = date_slot
        self.append_slot = time_slot
        self.date.on('input', self.date_time_change)
        self.time.on('input', self.date_time_change)
        self.on('input', self.input_change)

    @staticmethod
    def date_time_change(self, msg):
        self.parent.value = self.value
        self.parent.date.value = self.value
        self.parent.time.value = self.value

    @staticmethod
    def input_change(self, msg):
        self.date.value = self.value
        self.time.value = self.value


def input_test():
    wp = jp.QuasarPage()
    QInputDateTime(filled=True, style='width: 600px', a=wp, classes="q-pa-md", value='')
    QInputDateTime(filled=True, style='width: 600px', a=wp, classes="q-pa-md", value='2020-03-01 12:44')
    QInputDateTime(filled=True, style='width: 600px', a=wp, classes="q-pa-md", value='2021-04-01 14:44')
    QInputDateTime(filled=True, style='width: 600px', a=wp, classes="q-pa-md", value='2022-05-01 18:44')
    return wp


jp.justpy(input_test)
```

## Component to Link Chart and Grid
[live demo]({{demo_url}}/grid_test)

Please see [linking charts and grids](grids_tutorial/grid_events?id=linking-a-chart-and-a-grid-using-grid-events) for an explanation.

When you use ag-Grid's filtering and sorting options, the results are not just reflected in the grid, but also in the chart.


```python
import justpy as jp
import pandas as pd

class LinkedChartGrid(jp.Div):

    def __init__(self, df, x, y, **kwargs):
        super().__init__(**kwargs)
        self.df = df
        self.x = x
        self.y = y
        self.kind = kwargs.get('kind', 'column')
        self.stacking = kwargs.get('stacking', '')
        self.title = kwargs.get('title', '')
        self.subtitle = kwargs.get('subtitle', '')
        self.set_classes('flex flex-col')
        self.chart = df.jp.plot(x, y, a=self, classes='m-2 p-2 border', kind=self.kind, stacking=self.stacking, title=self.title, subtitle=self.subtitle)
        self.grid = df.jp.ag_grid(a=self)
        self.grid.parent = self
        for event_name in ['sortChanged', 'filterChanged', 'columnMoved', 'rowDragEnd']:
            self.grid.on(event_name, self.grid_change)


    @staticmethod
    def grid_change(self, msg):
        self.parent.df = jp.read_csv_from_string(msg.data)
        c = self.parent.df.jp.plot(self.parent.x, self.parent.y, kind=self.parent.kind, title=self.parent.title,
                                   subtitle=self.parent.subtitle, stacking=self.parent.stacking)
        self.parent.chart.options = c.options



alcohol_df = pd.read_csv('https://raw.githubusercontent.com/fivethirtyeight/data/master/alcohol-consumption/drinks.csv', encoding="ISO-8859-1")
bad_drivers_df = pd.read_csv('https://raw.githubusercontent.com/fivethirtyeight/data/master/bad-drivers/bad-drivers.csv', encoding="ISO-8859-1")


def grid_test():
    wp = jp.WebPage()
    c = LinkedChartGrid(alcohol_df, 0, [1,2,3,4], kind='column', a=wp, classes='m-4 p-2 border',
                        stacking='normal', title='Alcohol Consumption per Country', subtitle='538 data')
    LinkedChartGrid(bad_drivers_df, 0, [1,2,3,4,5,6,7], kind='column', a=wp, classes='m-4 p-2 border-4', title='Bad Drivers per US State', subtitle='538 data')
    return wp

jp.justpy(grid_test)
```
