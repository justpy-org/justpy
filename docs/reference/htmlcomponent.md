# HTML Components

## Introduction

In JustPy components are Python classes. All HTML components inherit from either the Div or Input component. The Input component itself inherits from the Div component. 

The reference will describe primarily the Div component and the Input component.

!!! tip "It would be helpful to read the [HTML Components](/tutorial/html_components) chapter in the tutorial first."

## Div Component

### Introduction

The Div component is the basic container component of JustPy. It is a component that can contain other components. It can of course, contain components that themselves are container components.


### Attributes
---

#### General

Attributes can be set as keywords when an element is created.
```python
import justpy as jp

jp.Div(text='hello', classes='text-red-500')
```

They can also be set anytime after the element is created (except for `delete_flag` which needs to be set at creation).


```python
import justpy as jp

d = jp.Div()
d.text = 'hello'
d.classes= 'text-red-500'
```

#### text
 
 * Type: `string`
 * Default: `""`  (the empty string)
 
The `text` attribute will always be rendered as the first child of the component. If you want a Div (or any container component) instance to render multiple texts in different locations, encompass the text in another container component and add that component to the Div at the location you want.

If you want to render an [HTML Entity](https://developer.mozilla.org/en-US/docs/Glossary/Entity) use the HTMLEntity component or set the `html_entity` attribute to `True`.

```python
import justpy as jp

def entity_test():
    wp = jp.WebPage()
    jp.Space(num=3, a=wp)
    jp.HTMLEntity(entity='a&#768;',a=wp, classes='text-lg')
    jp.Span(text='a&#768;',a=wp, classes='text-lg', html_entity=True)
    jp.Space(num=5, a=wp)
    jp.HTMLEntity(entity='a&#769',a=wp, classes='text-xl')
    jp.Span(text='a&#769',a=wp, classes='text-xl', html_entity=True)
    jp.Space(num=5, a=wp)
    jp.HTMLEntity(entity='&#8707;',a=wp, classes='text-2xl')
    jp.Span(text='&#8707;',a=wp, classes='text-2xl', html_entity=True)
    jp.Space(num=5, a=wp)
    jp.HTMLEntity(entity='&copy;', a=wp, classes='text-3xl')
    jp.Span(text='&copy;', a=wp, classes='text-3xl', html_entity=True)
    jp.Space(num=5, a=wp)
    return wp

jp.justpy(entity_test)
```

!!! info
    The Space component can be used to insert spaces. It creates a Span with `num` repeats of the html entity '&nbsp'.

#### classes

 * Type: `string`
 * Default: `""`  (the empty string)
 
The classes to attach to the element. Usually Tailwind classes, but may be any classes you define. Basically equivalent to the [`class`](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/class) attribute of HTML tags.

```python
import justpy as jp

def classes_test():
    wp = jp.WebPage()
    d = jp.Div(text='Classes Example', a=wp)
    # Assign Tailwind classes to d
    d.classes = 'text-5xl text-white bg-blue-500 hover:bg-blue-700 m-2 p-2 w-64'
    return wp

jp.justpy(classes_test)
```

#### style

 * Type: `string`
 * Default: `""`  (the empty string)
 
The CSS to attach to the element. Basically equivalent to the [`style`](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/style) attribute of HTML tags.

```python
import justpy as jp

def style_test():
    wp = jp.WebPage()
    for size in range(1,101):
        jp.Div(text=f' {size}', style=f'font-size: {size}px; color: red', a=wp, classes='inline cursor-pointer', size=size,
               click='self.size *= 2; self.style=f"font-size: {self.size}px; color: green";')
    return wp

jp.justpy(style_test)
```

#### components
 
 * Type: `list`
 * Default: `[]`
 
Holds the list of child elements in the Div. Strictly speaking these are not components, they are elements, instances of components. When the Div is rendered, the elements are rendered according to their place on the list, starting with the first.


In the following example, the Div elements will show up in a different order each time the page is loaded because `main_div.components` is shuffled.

```python
import justpy as jp
import random

def shuffle_test():
    wp = jp.WebPage()
    main_div = jp.Div(classes='flex flex-wrap m-2 p-2 ', a=wp)
    for i in range(1,101,1):
        jp.Div(text=f'Div {i}', a=main_div, classes='m-2 p-2 text-xl text-white bg-blue-500')
    random.shuffle(main_div.components)
    return wp


jp.justpy(shuffle_test)
```

#### events
 
 * Type: `list`
 * Default: `[]`

When an element is bound to an event, the event name (of type string) is added to `events`. You can use `events` to check which events the element will respond. Also, by removing an event name from the list, you will disable the element responding to that event.

#### allowed_events
 
 * Type: `list`
 * Default: `['click', 'mouseover', 'mouseout', 'mouseenter', 'mouseleave', 'input', 'change', 'after', 'before', 'keydown', 'keyup', 'keypress', 'focus', 'blur']`

If an event name is not in `allowed_events`, JustPy will generate an error if you try to bind to that event.
You can use the `add_event` method to add an allowed event to the list.

#### additional_properties
 
 * Type: `list`
 * Default: `[]`

JustPy does not pass all the JavaScript event properties by default since in most cases they are not needed. If you need additional properties from the JavasScript event, use the `additional_properties` attribute. In the example below, more fields are added to `msg`.

```python
import justpy as jp

def my_click(self, msg):
    print(msg)
    self.text = 'I was clicked'

def event_demo():
    wp = jp.WebPage()
    wp.debug = True
    d = jp.Div(text='Not clicked yet', a=wp, classes='w-48 text-xl m-2 p-1 bg-blue-500 text-white')
    d.on('click', my_click)
    d.additional_properties =['screenX', 'pageY','altKey','which','movementX','button', 'buttons']
    return wp

jp.justpy(event_demo)
```

#### inner_html

 * Type: `string`
 * Default: `""`  (the empty string)
 
Used to to set the HTML of an element directly.

```python
import justpy as jp

def inner_html_test():
    wp = jp.WebPage()
    for i in range(1,11):
        jp.Div(inner_html=f'<span style="color: orange">{i}) Hello!</span>', a=wp, classes='m-2 p-2 text-3xl')
    return wp

jp.justpy(inner_html_test)
```


!!! warning "If `inner_html` is not the empty string, it will override any other content of the element"

#### show

 * Type: `boolean`
 * Default: `True`
 
If set to `False`, the element is not rendered. See [here](/tutorial/html_components/#showing-and-hiding-elements)


#### set_focus

 * Type: `boolean`
 * Default: `False`
 
If set to `True`, the element will have focus when the page is rendered.

!!! warning "If multiple elements have the `set_focus` attribute set to `True`, the results will be unpredictable. The last element to be rendered by Vue will have focus."

```python
import justpy as jp

# Try not using this event handler and see what happens
def my_blur(self, msg):
        self.set_focus = False

def focus_test():
    wp = jp.WebPage()
    in1 = jp.Input(classes=jp.Styles.input_classes, placeholder='Input 1', a=wp, blur=my_blur)
    in2 = jp.Input(classes=jp.Styles.input_classes, placeholder='Input 2', a=wp, blur=my_blur)
    in3 = jp.Input(classes=jp.Styles.input_classes, placeholder='Input 3', a=wp, blur=my_blur)
    in4 = jp.Input(classes=jp.Styles.input_classes, placeholder='Input 4', a=wp, blur=my_blur)

    # Set focus on third Input element
    in3.set_focus = True

    return wp

jp.justpy(focus_test)

```

#### children

 * Type: `list`
 * Default: `[]`
 
 When an element is created, can be used to create its children also. Useful if you like defining elements in a hierarchical way.
 
 New in version 0.10

```python
import justpy as jp

def children_test():
    wp = jp.WebPage()
    div_classes = 'm-2 p-2 bg-blue-500 text-white text-lg'
    span_classes = 'm-2 p-2 bg-blue-500 text-yellow-700 text-xl'
    jp.Div(children=[jp.Div(classes=div_classes, children=
                            [jp.Span(text='s1', classes=span_classes), jp.Span(text='s2', classes=span_classes)])
        ,jp.Div(text='d2', classes=div_classes), jp.Div(text='d3', classes=div_classes), jp.Div(text='d4', classes=div_classes)], a=wp)

    return wp

jp.justpy(children_test)
```

#### animation

 * Type: `string`
 * Default: `""`  (the empty string)
 
Set the animation of the element. Uses [animate.css](https://daneden.github.io/animate.css/) 

Control the speed of the animation by adding classes:

| Class Name | Speed Time |
| ---------- | ---------- |
| `slow`     | `2s`       |
| `slower`   | `3s`       |
| `fast`     | `800ms`    |
| `faster`   | `500ms`    |

For more information and additional options consult the [animate.css documentation](https://github.com/daneden/animate.css/blob/master/README.md)

```python
import justpy as jp
import random

input_classes = "m-2 bg-gray-200 appearance-none border-2 border-gray-200 rounded w-64 py-2 px-4 text-gray-700 focus:outline-none focus:bg-white focus:border-purple-500"


def animate(self, msg):
    self.d.delete_components()  # remove all components from d
    directions = ['Up', 'Down', 'Left', 'Right']
    html_entity = False
    for letter in self.text_to_animate.value:
        if letter == ' ':
            letter = '&nbsp;'
            html_entity = True
        jp.Div(animation=f'fadeIn{random.choice(directions)}', text=letter, html_entity=html_entity,
               classes='rounded-full bg-blue-500 text-white text-6xl', a=self.d)
        html_entity = False


def animation_test():
    wp = jp.WebPage()
    text_to_animate = jp.Input(a=wp, classes=input_classes, placeholder='Enter text to animate', value='Animation Demo!', input='return True')
    animate_btn = jp.Button(text='Animate!', click=animate, classes='w-32 m-2 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded', a=wp)
    animate_btn.text_to_animate= text_to_animate
    d = jp.Div(classes='flex items-center justify-center', style='height: 500px', a=wp)
    animate_btn.d = d
    return wp

jp.justpy(animation_test)
```


#### id
 
 * Type: `string`
 * Default: Nothing assigned
 
 If you need to identify an element use the `name` attribute (or any other attribute you choose), NOT the `id` attribute. JustPy assigns a unique id to elements that are associated with events and uses it to identify which event handler to run.
 
!!! danger "It is advised not to change an element's `id` or assign it an id"
 

#### delete_flag

 * Type: `boolean`
 * Default: `True`
 
If set to `False`, element is not deleted when a page which it is on closes. In addition, non of its child components will be deleted.
If you create an element that will be used on more than one page, set the value to `False`.

#### event_propagation

 * Type: `boolean`
 * Default: `True`
 
The current version of JustPy supports only event bubbling. Events originate in the innermost child and bubble up through the parents unless`event_propagation` is set to `False`.


```python
import justpy as jp

def event_propagates():
    wp = jp.WebPage()
    main_div = jp.Div(classes='flex flex-wrap m-2 p-2 ', a=wp, click='self.text="main div clicked"')
    for i in range(1,10):
        jp.Div(text=f'Div {i}', a=main_div, classes='m-2 p-2 text-xl text-white bg-blue-500', click='self.text="clicked"')
    return wp

@jp.SetRoute('/no_propagation')
def event_does_not_propagate():
    wp = jp.WebPage()
    main_div = jp.Div(classes='flex flex-wrap m-2 p-2 ', a=wp, click='self.text="main div clicked"')
    for i in range(1,10):
        jp.Div(text=f'Div {i}', a=main_div, classes='m-2 p-2 text-xl text-white bg-blue-500',
               event_propagation=False, click='self.text="clicked"')
    return wp

jp.justpy(event_propagates)
```

#### vue_type

 * Type: `string`
 * Default: `'html_component'`
 
The Vue component to couple with the Python class. Used by the front end of the framework.

!!! danger "If you change this, the component will not be rendered correctly" 

!!! info "When you develop components that require a Vue component as well, you will need to set this attribute in the Python class"

#### html_tag

 * Type: `string`
 * Default: `'div'`
 
The HTML tag that corresponds to the component. If you change it, the component may not render correctly.

!!! danger "If you change this, the component may not be rendered correctly"

#### class_name

 * Type: `string`
 * Default: `'Div'`
 
The class (component) name of the element. Should be considered read only
 
#### Global HTML attributes

Div supports some HTML global attributes. Please review the  [Common Attributes](/tutorial/html_components/#common-attributes) section in the Tutorial. 

### Methods

`def delete(self)`  
Remove references to the object from JustPy internal data structures to allow garbage collection.

`def on(self, event_type, func)`  
Bind a function to an event

`def remove_event(self, event_type)`  
Remove and event from the element's allowed events

`def has_event_function(self, event_type)`  
Returns `True` if the element has the specified event

`async def update(self)`  
Updates just the element, not the whole page. The element is updated on all pages specified in the attribute `pages`.
See [Simple Message Board](/tutorial/pushing_data/#simple-message-board)  

`remove_page_from_pages(self, wp: WebPage)`  
Remove a page from `pages`

`def add_page(self, wp: WebPage)` and `def add_page_to_pages(self, wp: WebPage)`  
Add a page to `pages`

`def set_model(self, value)`  
Set the model value

`async def run_event_function(self, event_type, event_data)`  
Run an event function. This method takes two arguments in addition to `self`. The first is the event type. The second, is the dictionary we want passed as the second positional argument to the event handler. This is what we usually designate as `msg` in our event handler examples in the tutorial. See example [here](/tutorial/custom_components/#handling-the-change-event)

`@staticmethod def convert_dict_to_object(d)`  
Takes the dictionary created by `convert_object_to_dict` and returns an object. Can be used to make independent copies of objects.

`def __len__(self)`  
`len(c)` returns the number of direct children the element `c` has

`def add_to_page(self, wp: WebPage)`  
Adds the element to a page

`def add_attribute(self, attr, value)`  
Adds an attribute that will be part of the dictionary created by `convert_object_to_dict`

`def add_event(self, event_type)` and  `def add_allowed_event(self, event_type)`  
Add an allowed event to the element

`def add_scoped_slot(self, slot, c)`  
Relevant to Quasar and other Vue based frameworks or components.

`def to_html(self, indent=0, indent_step=0, format=True)`  
Returns an HTML representation of the element

`def react(self, data)`  
Executes just before the element is rendered. It is just `pass` for Div and is meant to be overridden by components that inherit from Div

`def convert_object_to_dict(self)`  
Converts the element to a dictionary in the format the can be sent to the frontend to be rendered.

`def add_component(self, child, position=None, slot=None)`  
Add a component at the specified position.

`def delete_components(self)`  
Use to empty a container element like Div. Does not delete the `text` attribute

`def add(self, *args)`  
Add all arguments as child elements after the current child elements

`def add_first(self, child)`  
Add a child element before all other child elements

`def remove_component(self, component)`  
Remove a child element

`def get_components(self)`  
Get child elements as a list

`def first(self)`  
Get first child element

`def last(self)`  
Get last child element

`def model_update(self)`  
Override as necessary. See example [here](/tutorial/model_and_data/#advanced-use-of-the-model-attribute)

