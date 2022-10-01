# Input Component

## Basic Use

Many web applications require users to fill forms. HTML forms are based on the [input HTML tag](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input).

The corresponding JustPy component is `Input`.

The following program adds a text input field to a page:
```python
import justpy as jp

input_classes = "m-2 bg-gray-200 border-2 border-gray-200 rounded w-64 py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-purple-500"

def input_demo1(request):
    wp = jp.WebPage()
    in1 = jp.Input(a=wp, classes=input_classes, placeholder='Please type here')
    return wp

jp.justpy(input_demo1)
```

## The input Event

The program above is quite boring, it does nothing except allow you to type text into the input field. To make it more interesting, let's have what we type reflected in a paragraph on the page. For this, we need to introduce the `input` event. When you type, each character typed into the input field generates an `input` event (yes, the tag and the event are called the same name).

Run the following program:

```python
import justpy as jp

input_classes = "m-2 bg-gray-200 border-2 border-gray-200 rounded w-64 py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-purple-500"
p_classes = 'm-2 p-2 h-32 text-xl border-2'

def my_input1(self, msg):
    self.div.text = self.value

def input_demo2(request):
    wp = jp.WebPage()
    in1 = jp.Input(a=wp, classes=input_classes, placeholder='Please type here')
    in1.div = jp.Div(text='What you type will show up here', classes=p_classes, a=wp)
    in1.on('input', my_input1)
    return wp

jp.justpy(input_demo2)
```

The function `input_demo` creates a web page and adds an input element called `in1` to it (ignore the classes, they are there just to make the input element look nicer and do not affect the functionality of the program).

Notice the `placeholder` attribute of `in1`. Before any text is typed into the input field or when it is emptied, the placeholder text is displayed in the field. We then define a div element that is added to the page (using the `a` keyword argument) and assigned to an attribute of `in1`. We saw this technique before. It simplifies event handling as we shall see in a second.

Next, we bind the input event of `in1` to the function `my_input` (we could have omitted this line by adding `input=my_input` as a keyword argument when we created `in1`). `my_input` is now the input event handler for `in1`.

The input event occurs each and every time a character is typed into an input element. After every keystroke this function is run (if the debounce period has expired - see below), and it changes the text of the div to the value of the input field.  By assigning the div to an `in1` attribute, we have access to all the variables we need in the event handler.

You may have noticed that there is a delay in the updating of the Div. That is because the component by default sets the `debounce` attribute of the input event to 200ms. This means an input event is generated only after a key has not been pressed for 200ms.

Try holding the a key down and have it repeated. Only when you lift your finger will the Div update. You can set the `debounce` attribute to the value you prefer in ms, just make sure to take into account the typing speed of your users and the latency of the connection. In general, a higher debounce value means the server will have to handle less communications and that may be an advantage for applications that need to scale.

## The change Event and the InputOnlyChange Component

The regular Input component generates an event each time a character is typed into the field. In some case this is not necessary and may put unwanted burden on the server. If you are not implementing a look ahead or validating the field as the user is typing, it is preferable to use InputOnlyChange instead of Input.

InputOnlyChange does not generate the input event, only the change event. The change event is generated when the field loses focus or the user presses the Enter button. It is not generated when the user types a character.

The example below is the same as the one above except that InputOnlyChange is used instead of Input.

```python
import justpy as jp

input_classes = "m-2 bg-gray-200 border-2 border-gray-200 rounded w-64 py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-purple-500"
p_classes = 'm-2 p-2 h-32 text-xl border-2'

def my_input2(self, msg):
    self.div.text = self.value

def input_demo3(request):
    wp = jp.WebPage()
    in1 = jp.InputChangeOnly(a=wp, classes=input_classes, placeholder='Please type here')
    in1.div = jp.Div(text='What you type will show up here only when Input element loses focus or you press Enter',
                     classes=p_classes, a=wp)
    in1.on('input', my_input2)
    in1.on('change', my_input2)
    return wp

jp.justpy(input_demo3)

```

## The Type Attribute

### Number Example

The input component can be of different [types](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input#%3Cinput%3E_types) such as 'number' or  'password'.

```python
import justpy as jp

input_classes = "m-2 bg-gray-200 border-2 border-gray-200 rounded w-64 py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-purple-500"
p_classes = 'm-2 p-2 h-32 text-xl border-2'

def my_input3(self, msg):
    self.div.text = self.value

def input_demo4(request):
    wp = jp.WebPage()
    in1 = jp.Input(type='number', a=wp, classes=input_classes, placeholder='Please type here')
    in1.div = jp.Div(text='What you type will show up here', classes=p_classes, a=wp)
    in1.on('input', my_input3)
    return wp

jp.justpy(input_demo4)
```

In the example above the type of `in1` is set to 'number'. Run the program and verify that only numbers can be input into the element.
> Note: `jp.Input(type='number'...` mimics the behavior of [HTML input number](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/number) thus the value is converted to a javascript [Number](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Number) after updating the value.
> This means large numbers can not be handled accurately as they are bound to the accuracy of [double-precision 64-bit binary format IEEE 754](https://en.wikipedia.org/wiki/Double-precision_floating-point_format).
> In python use float to have the same value as displayed in the input field.
> For details see [Issue#38](https://github.com/justpy-org/justpy/issues/38)
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

!!! tip
    If you plan to use Quasar with JustPy, checkout the [QOptionGroup component](https://quasar.dev/vue-components/option-group)

```python
import justpy as jp

def radio_test1():
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

jp.justpy(radio_test1)

```

Radio buttons generate the 'change' event on all browsers. They generate the 'input' event just on some. When one is checked the 'change' event is generated.

 When one radio button is checked, JustPy automatically un-checks the other radio buttons in the group.

 Radio buttons are grouped according to their `name` attribute and the value of their `form` attribute if one is assigned. Buttons with the same name on different assigned forms, will be in different groups. All radio buttons not in any form but with the same name, will be in one group.

!!! note
    You explicitly need to specify the form the buttons are on using the `form` attribute if you want to give button groups in different forms the same name. This is because JustPy does not know which form the button will be added to or has been added to. Alternatively, just have a unique name for each button group on the page.

In the example below, the results of clicking a radio button are shown using the event handler `radio_changed`. Notice that the value of the radio button is always the same. What changes is its `checked` property. The value of a group of radio buttons is the value of the radio button in the group that is checked.

To make all the radio buttons in the group available to the event handler, when we create them, we also create a list that holds all the radio buttons in the group. We assign this list to an attribute of each radio button element (in our case `btn_list`). In the event handler we iterate over this list to report which radio button is pressed.
### Radio Button Example with radio_changed event handler

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


def radio_test2():
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

jp.justpy(radio_test2)
```

### Checkbox Example

Below is an example of a checkbox and a textbox connected using the `model` attribute (you may skip this for now and return to this example after completing the chapter describing the `model` attribute in this tutorial).

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

## Changing Focus using Keyboard Events

In the example below, Input elements respond to the Esc and Enter keys. When Esc is pressed, the field value is set to the empty string. When Enter is pressed, focus moves to the next field down unless it is the last field in which case focus is moved to the first.

To make the example work, an event handler for the 'blur' event is required. When one of the input elements loses focus, the blur event occurs and the focus field of the element is set to false so that the correct element will have focus.

By setting the `set_focus` attribute of an element to `True`, you transfer the focus to it. If the attribute is `True` for multiple elements on the page, the results are unpredictable and therefore the blur event handler is required to make sure the attribute is `True` for only one element.

```python
import justpy as jp

def my_blur(self, msg):
        self.set_focus = False

def key_down(self, msg):
    # print(msg.key_data)
    key = msg.key_data.key
    if key=='Escape':
        self.value=''
        return
    if key=='Enter':
        self.set_focus = False
        try:
            next_to_focus = self.input_list[self.num + 1]
        except:
            next_to_focus = self.input_list[0]
        next_to_focus.set_focus = True
        return
    return True  # Don't update the page


def focus_test_input():
    wp = jp.WebPage()
    d = jp.Div(classes='flex flex-col  m-2', a=wp, style='width: 600 px')
    input_list = []
    number_of_fields = 5
    for i in range(1, number_of_fields + 1):
        label = jp.Label( a=d, classes='m-2 p-2')
        jp.Span(text=f'Field {i}', a=label)
        in1 = jp.Input(classes=jp.Styles.input_classes, placeholder=f'{i} Type here', a=label, keydown=key_down, spellcheck="false")
        in1.on('blur', my_blur)
        in1.input_list = input_list
        in1.num = i - 1
        input_list.append(in1)
    return wp

jp.justpy(focus_test_input)
```

As a rule of thumb, try to limit the usage of keyboard events to a minimum since they don't work well for mobile users.

## Using Select

The [select](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/select) tag needs to be used together with the option tag. In JustPy these correspond to Select and Option elements.

The program below creates a select element whose value changes the background color of a Div.


```python
import justpy as jp


def change_color(self, msg):
    self.color_div.set_class(f'bg-{self.value}-600')


def comp_test():
    wp = jp.WebPage()
    colors = ['red', 'green', 'blue', 'pink', 'yellow', 'teal', 'purple']
    select = jp.Select(classes='w-32 text-xl m-4 p-2 bg-white  border rounded', a=wp, value='red',
                  change=change_color)
    for color in colors:
        select.add(jp.Option(value=color, text=color, classes=f'bg-{color}-600'))
    select.color_div = jp.Div(classes='bg-red-600 w-32 h-16 m-4',a=wp)
    return wp

jp.justpy(comp_test)
```

## Your First Component

JustPy allows building your own reusable components. We will have a lot more to say about this later, but just to start easing into the subject, let's suppose we want to encapsulate the functionality of an Input coupled to a Div into one component (like in one of the first examples above). The program would look like this:

```python
import justpy as jp

class InputWithDiv(jp.Div):

    input_classes = "m-2 bg-gray-200 border-2 border-gray-200 rounded w-64 py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-purple-500"

    @staticmethod
    def input_handler(self, msg):
        self.div.text = self.value

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.in1 = jp.Input(a=self, classes=self.input_classes, placeholder='Please type here', input=self.input_handler)
        self.in1.div = jp.Div(text='What you type will show up here', classes='m-2 p-2 h-32 text-xl border-2', a=self)


def input_demo5(request):
    wp = jp.WebPage()
    for i in range(10):
        InputWithDiv(a=wp)
    return wp

jp.justpy(input_demo5)
```

Try running the program. It will put on the page 10 pairs of input and div elements. If you type into the respective input field, the text will show up in the respective div.

JustPy components are Python classes that inherit from JustPy classes. In the example above, we define the class `InputWithDiv` which inherits from the JustPy class `Div`. In the `__init__` method an input element and another div is added to the basic div, with the appropriate functionality. Now, we have a component, `InputWithDiv`, that we can reuse as we please in any project.

If you don't completely understand what is going on, don't worry. We will revisit this in much more detail later. The take home message at this stage is that the way you build complex applications in JustPy is by building components with isolated functionality. Hopefully, if JustPy gains popularity, there will be many components that the community will develop and share.
