# Custom Components

The idea behind component programming is simple and compelling: Build a component once, and then reuse it in different applications. 

In JustPy, components are Python classes and so are custom components. Developing a component in JustPy means in most cases declaring a new Python class. Why only in most cases? In some cases, developing complex JustPy components requires also developing a [Vue.js](https://vuejs.org/) component. For example, the `HighCharts` charting component required developing a Vue.js component. For JustPy to support [Quasar](https://quasar.dev/) components, a Vue.js component was also required. It turns out that all Quasar components can be supported with one Vue.js component and that simplified matters considerably.

However, let's start with the basics. Most components require only writing a Python class and no knowledge of Vue.js or JavaScript is required.

## Alert Component

Our first component is based on this [example](https://tailwindcss.com/components/alerts/#top-accent-border) from the Tailwind documentation.

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

As previously discussed, we will use `parse_html` to easily convert this to JustPy commands.

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

def alert_test():
    wp = jp.WebPage()
    d = MyAlert(a=wp, classes='m-2 w-1/4', title_text='hello', body_text='How is everybody?')
    d.title_text = 'Shalom'
    return wp

jp.justpy(alert_test)
```

When you run the program above, notice that the title of the MyAlert instance is rendered as 'Hello' instead of 'Shalom' even though the line `d.title_text = 'Shalom'` is executed after it is created. To fix this bug we need to assign the attributes `title_text` and `body_text` to the text of the appropriate elements when the instance is rendered, not when it is created.

## The react method

To facilitate this, each JustPy component supports the `react` method. It is run just before an element is rendered. It receives two arguments, the instance and the `data` attribute of its parent element or that of the `WebPage` if it has no parent. In base JustPy elements, `react` does nothing. It is there to be overridden in custom components.

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


def alert_test():
    wp = jp.WebPage()
    for greeting in greetings:
        d = MyAlert(a=wp, classes='m-2 w-1/4', title_text='hello', body_text='How is everybody?')
        d.title_text = greeting
    return wp


jp.justpy(alert_test)
```

At the end of `__init__` we added the two lines:
```python
self.title_p = c7
self.body_p = c8
```

These two attributes now hold the paragraphs where the title and body will be placed.
In the `react` meghod

## Date Card Component

Here is an example a simple date card component.

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

def comp_test():
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

jp.justpy(comp_test)
```

In this component we are using the template like features of Python f-strings to create a date card with some features that can be changed. This simple component inherits from the component `Div`. It changes only the `__init__` method and inherits all the others. 

Notice the `super().__init__(**kwargs)` line in `__init__`. It is required to take care of all the plumbing that goes along with a JustPy component. This line executes the `__init__` of `Div`.  We define the defaults for the component specific attributes before this line so as not to overwrite keyword arguments that the user has provided and are assigned to attributes in the superclass `__init__`. 

This component works well enough but has a flaw. The `inner_html` attribute is set in `__init__` when the instance is created. If for example, the instance's day attribute would change after `__init__` has run, it would not be reflected in the inner html and the component will not be rendered correctly. 

To solve this problem, we need to move setting `inner_html` from the time the instance was created to the time it is rendered. This is where convert_object_to_dict comes in. It is called each time a component is rendered and creates a Python dictionary that JustPy eventually converts to JSON and sends to the page to be rendered in the browser using a Vue.js component.

The result looks like this:
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


    def convert_object_to_dict(self):
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
        d = super().convert_object_to_dict()
        return d

def comp_test():
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

jp.justpy(comp_test)
```

Each JustPy component has a method called react that is called each time before the object is converted to a dict. The example above can therefore be written as follows:

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


def comp_test():
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

jp.justpy(comp_test)
```

Please notice two things. The first one is that we no longer need to override convert_object_to_dict. The second thing to notice is that the react method accepts an additional argument to self. The argument data is the data attribute of the component's direct parent. If the component has no parent, it is the data attribute of the page. Using react we can have child components change their behavior when rendered based on the data attribute of their parent or the page they are on. 
For example, let's make the color of the component dependent on the data attribute of their holding Div.

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


def comp_test():
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
                  change='self.d.data["color"] = self.value')
    s.d = d
    for color in colors:
        s.add(jp.Option(value=color, text=color, classes=f'bg-{color}-600'))
    return wp

jp.justpy(comp_test)
```

This example is a little more complex as we have added a [Select](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/select) component at the bottom of the page. Try changing the selected color. The color of the CalendarDate instances in the second group changes. This happens because when we created the Select on the page, we used the following to assign a simple function to its change event handler:
change='self.d.data["color"] = self.value'

This function sets the value of the 'color' key in the data dict of the Div that holds the CalendarDate instances to the new value of the Select component. In this example, we changed the react function so it uses this value instead of self.color (which was used in the previous example) to set the color to display.

A few more words about Select: A Select component includes Option components. In this example we add them to the Select using a predefined list of colors. When a specific option is selected, its value attribute becomes the value attribute of the Select. The change in value is acted upon by binding a method to the change event of the Select instance. 

## The Hello Component
 
JustPy comes with a simple Hello component, which we will now examine.

First run the following short program.
```python
import justpy as jp

def hello_test():
    wp = jp.WebPage()
    h = jp.Hello()
    for i in range(5):
        wp.add(h)
    return wp

jp.justpy(hello_test)
```

The program puts five Hello components on the page. Click any one of them. All five will show the number of times any component was clicked because each time through the loop, we add the same component to the page. There may be 5 rendered elements on the page, but for JustPy, these are the same component.

If we would like there to be independent components on the page, we would write the program in the following way:
```python
import justpy as jp

def hello_test():
    wp = jp.WebPage()
    for i in range(5):
        wp.add(jp.Hello() )
    return wp

jp.justpy(hello_test)
```
In this program, each time thorough the loop we create a new Hello component and add it to the page. When any component is clicked, no other component on the page is affected.

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

Again, JustPy components are Python classes. In our case, `Hello` inherits from `Div` and only changes `Div`'s `__init__` (the class constructor).

In the constructor we first initialize a counter for the instance. This is a new attribute that is not initialized by `Div`. Then we call the super class constructor, in our case the constructor of Div. This call provides Hello with the initializations required to work correctly inside the JustPy framework. Since we are calling the super class constructor after having provided a default value to the counter attribute, we can change it with a keyword argument. Try running the following:
```python
import justpy as jp

def hello_test():
    return jp.WebPage().add(*[jp.Hello(counter=100) for i in range(5)])

jp.justpy(hello_test)
```

I do not condone code like above, but it works. I recommend writing the program this way:
```python
import justpy as jp

def hello_test():
    wp = jp.WebPage()
    for i in range(5):
        jp.Hello(a=wp, counter=100)
    return wp

jp.justpy(hello_test)
```


Since counter is initialized  to 100, the components will start counting from 100. The call to the super class constructor takes care of assigning the keyword arguments. If we had put the initialization of `counter` after the call to the super class constructor, the keyword argument would have had no effect. 
Next, in the definition of Hello, we set the classes of the component to give it some basic design and we set the text. Then we define the click event handler and assign it to the instance. That's it.
Let's say we are not pleased with the Hello message and its colors and want to define a better Hello component. This is how we would do it:
```python
import justpy as jp

class MyHello(jp.Hello):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.classes = 'm-1 p-1 text-6xl text-center text-red-500 bg-yellow-500 hover:bg-yellow-800 cursor-pointer'
        self.text = 'Much Better Hello! (click me)'

def hello_test():
    return jp.WebPage().add(*[MyHello() for i in range(5)])

jp.justpy(hello_test)
```

We define a new component called `MyHello` which inherits from `Hello`. By running the super class `__init__` in the `__init__` of `MyHello`, we get all the functionality of `Hello`. We then just modify the classes and text. 

Just to review what happens when the same WebPage instance is returned to different browser tabs please run the following version of the program above:
```python
import justpy as jp

class MyHello(jp.Hello):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.classes = 'm-1 p-1 text-6xl text-center text-red-500 bg-yellow-500 hover:bg-yellow-800 cursor-pointer'
        self.text = 'Much Better Hello! (click me)'

wp = jp.WebPage(delete_flag=False).add(*[MyHello() for i in range(5)])

def hello_test():
    return wp
```

Here we define wp as a global variable and return it for every request. Open two or more browser tabs and see what happens when you click one of the components (hint: the component will be updated on all the pages).  Reminder: When an event handler finishes executing and returns None, JustPy updates all the browser tabs in which the WebPage instance is rendered. 

## The Calculator Component

In this part of the tutorial we will build a simple calculator component. We will build it in stages. First, we will build a component that does not handle events or the model attribute. Please run the following example.
```python

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


def calculator_test():
    wp = WebPage()
    for i in range(10):
        c = Calculator(a=wp, classes='m-1 border inline-block', style='width: 250px')
    return wp

justpy(calculator_test)
```

First look at the function `calculator_test`. This function creates a WebPage and adds ten instances of the Calculator component to it. The result in the browser is a tab with ten calculators. Try changing the number of calculators on the page by changing the argument to range. Once a JustPy component has been defined, it is simple to reuse it. The Calculator component can be used now in multiple projects.

JustPy components are regular Python classes, there is nothing special about them from a Python point of view. The Calculator component is therefore a Python class. The Calculator class inherits from Div so Calculator is endowed from the start will all the features and capabilities of the Div component. These features are used in the __init__, the class constructor, in order to add the other components needed to implement the calculator.

The class constructor first calls the class constructor of the super class (in this case Div). If a class inherits from another JustPy component, it will almost be the case that you would run the __init__ of the super class. It then sets the value attribute to 0 and adds two Input components, one for the tape and one for the result. The two Inputs are assigned to instance attributes for future reference and added to self (which is a Div and therefore other components can be added to it). The Inputs are also designated readonly so that the user cannot type in them.

After the two Inputs are added to the instance, two nested loops are used to add the calculator buttons based on the layout list which is a list of lists. Each list each represents a line of buttons. Each button is assigned the same click event handler, self.calculator_click which is a static method of the Calculator class (we could have defined the event handler inside the __init_ function instead). We also assign to the button calc attribute a reference to the Calculator instance of which the button is part of. This is used in the click event handler to set the value of the Calculator instance.

In this example, for the sake of brevity, we implemented a very simple state machine for the calculator, and it is not perfect (for example, it does not handle 0 in front of a number). But for our purposes, it will do. The state machine is inside the click event handler. All buttons on the calculator use the same event handler but it knows which specific button was pressed based on self.text, the text of the button, which is different for each button. 

As it is currently defined, Calculator does not support any useful events. We would like to add a meaningful change event to it. This event will fire when the value of the Calculator instance changes. We do this by modifying the click event handler of the buttons. The value of the Calculator instance will not change unless some button is clicked. We therefore check if the specific button click changed the value and if that is the case, we run the change event handler of the Calculator instance. This is how the result looks like: 

```python
from justpy import Div, Input, Button, WebPage, justpy, run_event_function

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
                return await run_event_function(calc, 'change', calc_msg)


def calc_change(self, msg):
    print('In change')
    print(msg)
    self.d.text = self.value

def calculator_test():
    wp = WebPage()
    c = Calculator(a=wp, classes='m-1 border inline-block', style='width: 250px', change=calc_change)
    d = Div(classes='border m-2 p-1 w-64 text-xl', text='0', a=wp)
    c.d = d
    return wp

justpy(calculator_test)
```

Run the program above. You will see that the value of the calculator is reflected in the Div below it since that is what we defined the change event handler to do. Inside the click event handler, if a change occurs, we check if there is a change event handler and if it does, we run the Calculator event handler using the JustPy provided function `run_event_function`. 

This function takes four parameters, one of which has a default. The first parameter is the component we want to run the event handler for. The second is the event type. The third, is the dictionary we want to be passed as the second positional argument to the event handler. This is what we usually designate as msg in our event handlers. The fourth argument determines whether to create a dot notation addressable dict from the third parameter. It is True by default.
 
 In our case, we are providing the function already with dot notation accessible dict since we are using msg, which is already a such a dict. Before calling run_event_function we modify some values in msg to make it more informative. In general, you would create the appropriate msg for how you believe the component will be used. In our case we have added the button_text key which stores the text of the last button that was clicked and that generated the change event.

Please note that run_event_function is an async function and therefore since calculator_click awaits it, it needs to be a coroutine also and is defined using async. 

To make Calculator complete, we will also add handling of the model attribute to it. This is quite simple in our case. First, we need to remember that Calculator inherits from Div and is a derived (child) class of Div. The Div model_update method sets the Div instance's text attribute to the model. Therefore, we need to override it in our case to do nothing so we don't see the value as text at the top of the calculator. Try removing the model_update method from the example below and see what happens.

```python
from justpy import Div, Input, Button, WebPage, justpy, run_event_function, set_model

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
            set_model(calc, calc.value)  #******************** updates model 
            if calc.has_event_function('change'):
                calc_msg = msg
                calc_msg.event_type = 'change'
                calc_msg.id = calc.id
                calc_msg.button_text = self.text
                calc_msg.value = calc.value
                calc_msg.class_name = calc.__class__.__name__
                return await run_event_function(calc, 'change', calc_msg)

    def model_update(self):
        pass

def calculator_test():
    wp = WebPage(data={'value': 0})
    Calculator(a=wp, classes='m-1 border inline-block', style='width: 250px', model=[wp, 'value'])
    for i in range(5):
        Div(classes='border m-2 p-1 w-64 text-xl', text='0', a=wp, model=[wp, 'value'])
    return wp

justpy(calculator_test)
```

Notice that we have added a call to the JustPy utility function  set_model in the click event handler. This function checks if the component provided as its first positional argument has a model attribute and if so, sets it to the second positional argument.  The function set_model is defined as follows:

```python
def set_model(c, value):
    if hasattr(c, 'model'):
        c.model[0].data[c.model[1]] = value
```