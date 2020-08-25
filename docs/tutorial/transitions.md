# Transitions

CSS transitions are a powerful way to make components interactive and engaging. From version 1.3, Tailwind provides [classes](https://tailwindcss.com/docs/transition-property/) that simplify adding transitions to elements.

JustPy uses [Alpine's transition format](https://github.com/alpinejs/alpine#x-transition) to apply classes for an element's transition from hidden to a non-hidden state. 


!!! warning
    You must add or remove the class `hidden` to change the state of an element. You can do this using the set_class and remove_class methods. See the example below. The `hidden` class is defined both in Tailwind and Quasar pages. If you use neither, you need to define it yourself as `{display: none;}`

A CSS transition is defined by three sets of classes. The first set of classes are classes that are associated with the element throughout the transition process. The second set of classes defines the initial state of the element. The third set of classes defines the end state of the element after the transition has ended.

You can apply these three sets of classes to three types of element states. The 'enter' state applies when an element transitions from hidden to not hidden. The 'leave' state applies when an element transitions from not hidden to hidden. The 'load' state applies when the page is initially loaded.

These classes are stored in a dictionary of the form:
```python
transition_dict = {
'enter': 'transition ease-out duration-1000',  
'enter_start': 'opacity-0 transform scale-0', 
'enter_end': 'opacity-100 transform scale-100', 
'leave': 'transition ease-out duration-1000', 
'leave_start': 'opacity-100 transform scale-100', 
'leave_end': 'opacity-0 transform scale-0', 
'load': 'transition ease-out duration-1000', 
'load_start': 'opacity-0 transform scale-0', 
'load_end': 'opacity-100 transform scale-100'
}
```

To enable transitions on an element, assign this dictionary to the element's `transition` attribute.

```python

d = jp.Div(text='hello')
d.transition = transition_dict

```

The transition dictionary does not need to have all the keys shown above. If you want a transition only when the element loads the dictionary could look like this:

```python
transition_dict = {
'load': 'transition ease-out duration-1000', 
'load_start': 'opacity-0 transform scale-0', 
'load_end': 'opacity-100 transform scale-100'
}
```

!!! info
    If you want to transition a Quasar element, encompass it inside a Div and transition the Div.

In the example below, 10 Divs are transitioned each time the button is clicked:

```python
import justpy as jp

def toggle_hidden(self, msg):
    for d in self.div_list:
        if d.has_class('hidden'):
            d.remove_class('hidden')
        else:
            d.set_class('hidden')


def transition_test():
    wp = jp.WebPage()
    tran = jp.Dict()
    tran.load = "transition ease-out duration-1000"
    tran.load_start = 'opacity-0 transform scale-0'
    tran.load_end = 'opacity-100 transform scale-100'
    tran.enter = 'transition ease-out duration-1000'
    tran.enter_start = 'opacity-0 transform scale-0'
    tran.enter_end = 'opacity-100 transform scale-1000'
    tran.leave = "transition ease-out duration-1000"
    tran.leave_start = 'opacity-100 transform scale-1000'
    tran.leave_end = 'opacity-0 transform scale-0'
    div_list = []
    flex_div = jp.Div(classes='flex flex-wrap', a=wp)
    for i in range(10):
        d = jp.Div(a=flex_div, text='hello', style='height: 150px; width:200px')
        jp.Pre(text=' test', a=d)
        d.transition = tran
        d.classes = 'border text-xl m-2 h-16 w-16 bg-blue-500'
        div_list.append(d)
    b = jp.Button(text='Click here', classes=jp.Styles.button_simple + ' m-2', a=wp, click=toggle_hidden)
    b.div_list = div_list
    return wp

jp.justpy(transition_test)

```


    