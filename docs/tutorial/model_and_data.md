# The model and data Attributes

## Introduction and Examples

The `model` attribute is a special one in JustPy. You don't need to use it, but if you do, it may make your code more concise and readable. It is an elegant and simple way to share data between independent components (it was inspired by the [`v-model`](https://vuejs.org/v2/api/#v-model) directive in Vue.js and works in a similar manner).

Try running the following program and typing into the input field in the browser:

### Input field demo
```python
import justpy as jp

async def input_demo_model1(request):
    wp = jp.WebPage(data={ 'text': 'Initial text'})
    input_classes = "m-2 bg-gray-200 appearance-none border-2 border-gray-200 rounded xtw-64 py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-purple-500"
    jp.Input(a=wp, classes=input_classes, placeholder='Please type here', model=[wp, 'text'])
    jp.Div(model=[wp, 'text'], classes='m-2 p-2 h-32 text-xl border-2 overflow-auto', a=wp)
    return wp

jp.justpy(input_demo_model1)
```

Text entered in an input field is reflected in a div on the page. The connection between the input and the div is made using the `model` and `data` attributes. Notice that when we create the web page, we initialize a `data` attribute. The `data` attribute must be a Python dictionary. In our case it is a dictionary with one entry. The key is 'text' and the value is 'Initial text'.

When we create the Input element, we add the following to its keyword arguments: `model=[wp, 'text']`

This tells the Input instance that it will model itself based on the value under the 'text' key in `wp`'s data. For an Input element this means that when rendered it will take its value from `wp.data['text']` AND when its value is changed due to an input event, it will set `wp.data['text']` to its new value.

!!! note
    It is important to understand that in the case of Input, `model` has a two way influence. It gets its value from the appropriate data attribute and when an input event occurs it changes the appropriate data attribute.

In the case of a Div element the relation is only one way. Its text attribute is rendered according to the model attribute but it does not change the data dictionary.

If an element has an input event, the model attribute works in two directions, otherwise just in one. For two directional elements the attribute changed is value while for one directional ones the attribute changed is text.

How is this useful? Let's put three divs on the page instead of just one:
### Input field demo with three divs
```python
import justpy as jp

async def input_demo_model2(request):
    wp = jp.WebPage(data={'text': 'Initial text'})
    input_classes = "m-2 bg-gray-200 appearance-none border-2 border-gray-200 rounded xtw-64 py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-purple-500"
    jp.Input(a=wp, classes=input_classes, placeholder='Please type here', model=[wp, 'text'])
    for i in range(3):
        jp.Div(model=[wp, 'text'], classes='m-2 p-2 h-32 text-xl border-2 overflow-auto', a=wp)
    return wp

jp.justpy(input_demo_model2)
```

Since all Div instances have the same model, they change when we type. Without the model attribute, implementing this would be more verbose.

Now let's duplicate the Inputs. Let's have five Inputs instead of one:

### Input field demo with five Inputs
```python
import justpy as jp

async def input_demo_model3(request):
    wp = jp.WebPage(data={'text': 'Initial text'})
    input_classes = "m-2 bg-gray-200 appearance-none border-2 border-gray-200 rounded xtw-64 py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-purple-500"
    for _ in range(5):
        jp.Input(a=wp, classes=input_classes, placeholder='Please type here', model=[wp, 'text'])
    for _ in range(3):
        jp.Div(model=[wp, 'text'], classes='m-2 p-2 h-32 text-xl border-2 overflow-auto', a=wp)
    return wp

jp.justpy(input_demo_model3)
```

Type into any one of the five Input fields and see what happens. Since all elements share the same model, they all change in tandem. We didn't need to write any event handler.

Let's make a small modification to the program and add a reset button that will clear all the elements on the page:

### Input field demo with reset button
```python
import justpy as jp

def reset_all(self, msg):
    msg.page.data['text'] = ''

async def input_demo_model4(request):
    wp = jp.WebPage(data={'text': 'Initial text'})
    button_classes = 'w-32 m-2 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded'
    b = jp.Button(text='Reset', click=reset_all, a=wp, classes=button_classes)
    jp.Hr(a=wp)  # Add horizontal like to page
    input_classes = "m-2 bg-gray-200 appearance-none border-2 border-gray-200 rounded xtw-64 py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-purple-500"
    for i in range(5):
        jp.Input(a=wp, classes=input_classes, placeholder='Please type here', model=[wp, 'text'])
    for i in range(3):
        jp.Div(model=[wp, 'text'], classes='m-2 p-2 h-32 text-xl border-2 overflow-auto', a=wp)
    return wp

jp.justpy(input_demo_model4)
```

When the button is clicked, the following command in `reset_all` is executed: `msg.page.data['text'] = ''`

Since all the Inputs and Divs are modeled after this dictionary entry, they are all reset to the empty string when the button is clicked.

!!! note
    Any element, a Div for example, may have a data attribute and be used in a model attribute, not just a WebPage.

With the `model` and `data` attributes you can easily propagate a change in one element to others.

## Advanced use of the model attribute

!!! tip
    This part of the tutorial will use custom components. I recommend skipping this section initially and returning to it after having completed the first few sections of the [Creating Custom Components](../custom_components) part of the tutorial

The following program is the base one we will expand on. It uses `model` in the same way as examples above.

### use of model
```python
import justpy as jp

corner_classes = 'p-3 absolute bg-gray-200 '

def model_demo1():
    wp = jp.WebPage()
    d = jp.Div(classes='relative h-screen bg-gray-600', a=wp, data={'text': ''})
    for v_pos in ['top', 'bottom']:
        for h_pos in ['left', 'right']:
            corner_div = jp.Div(classes=corner_classes + f'{v_pos}-0 {h_pos}-0', a=d)
            jp.Div(text=f'{v_pos} {h_pos}', a=corner_div)
            jp.Div(text=f'typing will go here', a=corner_div, model=[d, 'text'])
    middle_input = jp.Input(text='middle', classes='absolute text-xl border-2 border-red-600',
                            placeholder='Type here', style='top: 50%; left: 40%', model=[d, 'text'], a=d)
    return wp

jp.justpy(model_demo1)
```

When you type text into `middle_input` it shows up in the four corners of the window. In each corner there is a Div that contains two other Divs. The second Div has the `model` property and the text in it changes when the user types into `middle_input`'`.

If we want the corners to show the text "Nothing typed yet" when `middle_input` is empty, the best way to implement this, is by creating a new component with a more sophisticated `model` handling method.

The program would look like this:
### more sophisticated use of model
```python
import justpy as jp

corner_classes = 'p-3 absolute bg-gray-200 '

class MyDiv(jp.Div):

    def model_update1(self):
        # model has the form [wp, 'text'] for example
        if self.model[0].data[self.model[1]]:
            self.text = str(self.model[0].data[self.model[1]])
        else:
            self.text = "Nothing typed yet"


def model_demo2():
    wp = jp.WebPage()
    d = jp.Div(classes='relative h-screen bg-gray-600', a=wp, data={'text': ''})
    for v_pos in ['top', 'bottom']:
        for h_pos in ['left', 'right']:
            corner_div = jp.Div(classes=corner_classes + f'{v_pos}-0 {h_pos}-0', a=d)
            jp.Div(text=f'{v_pos} {h_pos}', a=corner_div)
            MyDiv(text=f'typing will go here', a=corner_div, model=[d, 'text'])
    middle_input = jp.Input(text='middle', classes='absolute text-xl border-2 border-red-600',
                            placeholder='Type here', style='top: 50%; left: 40%', model=[d, 'text'], a=d)
    return wp

jp.justpy(model_demo2)
```

We define a new component, `MyDiv` that inherits from `Div` and is identical except for the `model_update` method.
The standard `model_update` method `Div` comes with is:
```python
def model_update2(self):
    # [wp, 'text-data'] for example
    self.text = str(self.model[0].data[self.model[1]])
```

In `MyDiv`'s `model_update` we check first if the value to set the `text` attribute is the empty string, and if so, assign to it the string "Nothing typed yet". It creates the functionality we were looking for.

## More complex model_update methods

We can put more functionality into the the `model_update` function.

```python
import justpy as jp

corner_classes = 'p-3 absolute bg-gray-200 '

class MyDiv(jp.Div):

    def model_update3(self):
        # [wp, 'text-data'] for example
        if self.model[0].data[self.model[1]]:
            self.text = (str(self.model[0].data[self.model[1]]) + ' ')*self.repeat
        else:
            self.text = self.initial_text


def model_demo3():
    wp = jp.WebPage()
    d = jp.Div(classes='relative h-screen bg-gray-600', a=wp, data={'text': ''})
    repeat = 1
    for v_pos in ['top', 'bottom']:
        for h_pos in ['left', 'right']:
            corner_div = jp.Div(classes=corner_classes + f'{v_pos}-0 {h_pos}-0', a=d)
            jp.Div(text=f'{v_pos} {h_pos}', a=corner_div)
            MyDiv(text=f'typing will go here', a=corner_div, model=[d, 'text'], repeat=repeat, initial_text = 'Yada Yada')
            repeat += 1
    middle_input = jp.Input(text='middle', classes='absolute text-xl border-2 border-red-600',
                            placeholder='Type here', style='top: 50%; left: 40%', model=[d, 'text'], a=d)
    return wp

jp.justpy(model_demo3)
```

 We add the two attributes `repeat` and `initial_text` to `MyDiv`. The first, `repeat` determines how many time the model value will be repeated in the text. We give each corner a different value.
