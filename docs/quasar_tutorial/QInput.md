# QInput

## Introduction

The [Quasar QInput component](https://quasar.dev/vue-components/input) is very versatile and comes with many features and options. Almost all are supported by JustPy.

QInput like Input creates an input event when its value changes.

The program below puts on the page several QInput elements with different features. All are connected using the the same `model` attribute. 

```python
import justpy as jp

def input_test(request):
    wp = jp.QuasarPage(data={'text': ''})
    c1 = jp.Div(classes='q-pa-md', a=wp)
    c2 = jp.Div(classes='q-gutter-md', style='max-width: 300px', a=c1)
    c3 = jp.QInput(label='Standard', a=c2, model=[wp, 'text'])
    c4 = jp.QInput(filled=True, label='Filled', a=c2, model=[wp, 'text'])
    c5 = jp.QInput(outlined=True, label='Outlined', a=c2, model=[wp, 'text'])
    c6 = jp.QInput(standout=True, label='Standout', a=c2, model=[wp, 'text'])
    c7 = jp.QInput(standout='bg-teal text-white', label='Custom standout', a=c2, model=[wp, 'text'])
    c8 = jp.QInput(borderless=True, label='Borderless', a=c2, model=[wp, 'text'])
    c9 = jp.QInput(rounded=True, filled=True, label='Rounded filled', a=c2, model=[wp, 'text'])
    c10 = jp.QInput(rounded=True, outlined=True, label='Rounded outlined', a=c2, model=[wp, 'text'])
    c11 = jp.QInput(rounded=True, standout=True, label='Rounded standout', a=c2, model=[wp, 'text'])
    c12 = jp.QInput(square=True, filled=True, label='Square filled', hint='This is a hint', a=c2, model=[wp, 'text'])
    c13 = jp.QInput(square=True, outlined=True, label='Square outlined', a=c2, model=[wp, 'text'])
    c14 = jp.QInput(square=True, standout=True, label='Square standout', a=c2, model=[wp, 'text'])
    return wp

jp.justpy(input_test)
```

## Using slots

```python
import justpy as jp

def input_test(request):
    wp = jp.QuasarPage()
    c1 = jp.Div(classes='q-pa-md', a=wp)
    c2 = jp.Div(classes='q-gutter-md', style='max-width: 300px', a=c1)
    icon1 = jp.QIcon(name='event', color='blue')
    icon2 = jp.QIcon(name='place', color='red')
    for slot in ['append', 'prepend', 'before']:
        in1 = jp.QInput(label=slot, filled=True, hint=f'Icon is in slot "{slot}" and "after"', a=c2, after_slot=icon2)
        #in1.after_slot = icon2    # Alternative to keyword method used in line above
        setattr(in1, slot + '_slot', icon1)
    return wp

jp.justpy(input_test)

```

## Password visibility toggle example

```python
import justpy as jp

def input_test(request):
    wp = jp.QuasarPage(data={'text': ''})
    c1 = jp.Div(classes='q-pa-md', a=wp)
    c2 = jp.Div(classes='q-gutter-md', style='max-width: 300px', a=c1)

    password_input = jp.QInput(filled=True,  type='password', a=c2, hint="Password with toggle")
    visibility_icon = jp.QIcon(name='visibility_off', classes='cursor-pointer')
    visibility_icon.password_input = password_input

    password_input.append_slot = visibility_icon

    def toggle_password(self, msg):
        if self.name == 'visibility_off':
            self.name = 'visibility'
            self.password_input.type='text'
        else:
            self.name = 'visibility_off'
            self.password_input.type = 'password'

    visibility_icon.on('click', toggle_password)

    return wp

jp.justpy(input_test)
```

Or better yet, as a reusable component

```python
import justpy as jp

class PasswordWithToggle(jp.QInput):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'password'
        visibility_icon = jp.QIcon(name='visibility_off', classes='cursor-pointer')
        visibility_icon.password_input = self
        self.append_slot = visibility_icon
        visibility_icon.on('click', self.toggle_password)

    @staticmethod
    def toggle_password(self, msg):
        if self.name == 'visibility_off':
            self.name = 'visibility'
            self.password_input.type = 'text'
        else:
            self.name = 'visibility_off'
            self.password_input.type = 'password'


def input_test(request):
    wp = jp.QuasarPage(data={'text': ''})
    c1 = jp.Div(classes='q-pa-md', a=wp)
    c2 = jp.Div(classes='q-gutter-md', style='max-width: 300px', a=c1)
    for i in range(1,6):
        PasswordWithToggle(filled=True,  type='password', a=c2, hint=f'Password with toggle #{i}')
    return wp

jp.justpy(input_test)

```

## Input masks


```python
import justpy as jp

def input_test(request):
    wp = jp.QuasarPage(data={'text': ''})
    c1 = jp.Div(classes='q-pa-md', a=wp)
    c2 = jp.Div(classes='q-gutter-md', style='max-width: 300px', a=c1)
    jp.QInput(filled=True, label='Phone', mask='(###) ### - ####', hint="Mask: (###) ### - ####", a=c2)
    return wp

jp.justpy(input_test)

```

