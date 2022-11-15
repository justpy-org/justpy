# Quasar Introduction

## General

[Quasar](https://quasar.dev) is an MIT licensed open-source JavaScript framework that provides a comprehensive set of [Vue.js](https://vuejs.org/) components that follow the [Material Guidelines](https://material.io/). You can learn more about it [here](https://quasar.dev/introduction-to-quasar).

JustPy supports most of the Quasar components and their features. In JustPy, Quasar components, just like HTML components, are Python classes.

The Quasar documentation is excellent and includes many examples. You will need to consult it for the specifics of each component.

As there are many Quasar components, I suggest browsing the documentation to see what is available.

The name of the Quasar component and the JustPy component is the same. If the Quasar component is called QMenu for example, the corresponding JustPy class is called QMenu also.  

This guide/tutorial is far from complete and I will be adding examples to it over time.

!!! warning
    Quasar uses its own [classes](https://quasar.dev/style/typography) to style elements on the page, so do not use Tailwind classes on Quasar pages unless you set the `tailwind` attribute to `True`..

## Example

### QBtn example
[QBtn example live demo]({{demo_url}}/quasar_example1)
The following example puts some Quasar buttons on the page and toggles their color and label when they are clicked. Also, clicking any button toggles the dark mode of the page.

```python
import justpy as jp
import random

async def my_click(self, msg):
    self.color = random.choice(['primary', 'secondary', 'accent', 'dark', 'positive',
                                'negative','info', 'warning'])
    self.label = self.color
    msg.page.dark = not msg.page.dark
    await msg.page.set_dark_mode(msg.page.dark)

def quasar_example1():
    wp = jp.QuasarPage(dark=True)  # Load page in dark mode
    d = jp.Div(classes='q-pa-md q-gutter-sm', a=wp)
    jp.QBtn(color='primary', icon='mail', label='On Left', a=d, click=my_click)
    jp.QBtn(color='secondary', icon_right='mail', label='On Right', a=d, click=my_click)
    jp.QBtn(color='red', icon='mail', icon_right='send', label='On Left and Right', a=d, click=my_click)
    jp.Br(a=d)
    jp.QBtn(icon='phone', label='Stacked', stack=True, glossy=True, color='purple', a=d, click=my_click)
    return wp

jp.justpy(quasar_example1)
```

The program uses the JustPy QBtn component which is based on the [Quasar QBtn component](https://quasar.dev/vue-components/button). Click the buttons and notice the ripple effect which is part of the Material specification.

## props of Quasar components

The JustPy component usually supports all the Quasar component options (in the Quasar docs these are called `props`). In JustPy these are designated by setting the attributes of the element. This can be done at creation using keywords or later using standard attribute assignment.

Quasar props are in kebab case: `icon-right`
In JustPy the attribute names are in snake case: `icon_right`

If a quasar prop is set just by specifying it, in JustPy you set the corresponding attribute to `True`.

For example, if a Quasar button is defined like this:
```html
<q-btn round color="primary" icon="shopping_cart" />
```

In JustPy it would look like this:
```python
import justpy as jp
jp.QBtn(round=True, color='primary', icon='shopping_cart') # round is set to True
```


## Slots

Quasar components have also slots in addition to props. JustPy supports most of the slots.

Slots differ from attributes at they contain content in the form of an element as their value.

In the example below we add an icon to several QInput slots.

```python
import justpy as jp

def input_test1(request):
    wp = jp.QuasarPage()
    c1 = jp.Div(classes='q-pa-md', a=wp)
    c2 = jp.Div(classes='q-gutter-md', style='max-width: 300px', a=c1)
    icon1 = jp.QIcon(name='event', color='blue')
    icon2 = jp.QIcon(name='place', color='red')
    for slot in ['append', 'prepend', 'before']:
        in1 = jp.QInput(label=slot, filled=True, hint=f'Icon is in slot "{slot}" and "after"', a=c2, after_slot=icon2)
        setattr(in1, slot + '_slot', icon1)
    return wp

jp.justpy(input_test1)

```

To insert content into a slot use the regular attribute assignment syntax. To insert element `e` in slot `append` of element `in1`  you could write:
```python
in1.append_slot = e
```

Just add '_slot' to the slot name and treat it as an instance attribute.

## Parsing Quasar Tags
[Parsing Quasar Tags live demo]({{demo_url}}/quasar_example2)

The JustPy `parse_html` function recognizes Quasar tags. This is convenient as it allows using examples in the Quasar documentation. The example below was taken from the [QList documentation](https://quasar.dev/vue-components/list-and-list-items).

The parsing function also generates the `commands` attribute which is a list of JutPy commands required to generate the HTML. In the example below we print these commands.


```python
import justpy as jp


html_string = """
<div class="q-pa-md" style="max-width: 350px">
    <q-list bordered>
      <q-item clickable v-ripple>
        <q-item-section avatar>
          <q-icon color="primary" name="bluetooth" />
        </q-item-section>

        <q-item-section>Icon as avatar</q-item-section>
      </q-item>

      <q-item clickable v-ripple>
        <q-item-section avatar>
          <q-avatar color="teal" text-color="white" icon="bluetooth" />
        </q-item-section>

        <q-item-section>Avatar-type icon</q-item-section>
      </q-item>

      <q-item clickable v-ripple>
        <q-item-section avatar>
          <q-avatar rounded color="purple" text-color="white" icon="bluetooth" />
        </q-item-section>

        <q-item-section>Rounded avatar-type icon</q-item-section>
      </q-item>

      <q-item clickable v-ripple>
        <q-item-section avatar>
          <q-avatar color="primary" text-color="white">
            R
          </q-avatar>
        </q-item-section>

        <q-item-section>Letter avatar-type</q-item-section>
      </q-item>

      <q-separator />

      <q-item clickable v-ripple>
        <q-item-section avatar>
          <q-avatar>
            <img src="https://cdn.quasar.dev/img/boy-avatar.png">
          </q-avatar>
        </q-item-section>
        <q-item-section>Image avatar</q-item-section>
      </q-item>

      <q-item clickable v-ripple>
        <q-item-section avatar>
          <q-avatar square>
            <img src="https://cdn.quasar.dev/img/boy-avatar.png">
          </q-avatar>
        </q-item-section>
        <q-item-section>Image square avatar</q-item-section>
      </q-item>

      <q-item clickable v-ripple>
        <q-item-section avatar>
          <q-avatar rounded>
            <img src="https://cdn.quasar.dev/img/boy-avatar.png">
          </q-avatar>
        </q-item-section>
        <q-item-section>Image rounded avatar</q-item-section>
      </q-item>

      <q-separator />

      <q-item clickable v-ripple>
        <q-item-section avatar>
          <q-avatar rounded>
            <img src="https://cdn.quasar.dev/img/mountains.jpg">
          </q-avatar>
        </q-item-section>
        <q-item-section>List item</q-item-section>
      </q-item>

      <q-item clickable v-ripple>
        <q-item-section thumbnail>
          <img src="https://cdn.quasar.dev/img/mountains.jpg">
        </q-item-section>
        <q-item-section>List item</q-item-section>
      </q-item>
    </q-list>
  </div>
"""

def quasar_example2():
    """
    Show parsing and command generation
    """
    wp = jp.QuasarPage()
    div_root_component = jp.parse_html(html_string, a=wp)
    # print out all commands on console
    for i in div_root_component.commands:
        print(i)
    return wp

jp.justpy(quasar_example2)
```


## Quasar Directives

JustPy supports the following Quasar Vue directives:
'v-close-popup', 'v-close-menu', 'v-ripple', 'v-model', 'v-close-dialog'

!!! info "In JustPy the directives are specified in snake case: `v_close_popup` instead of `v-close-popup`"

!!! info "Use QDiv instead of Div if you want to apply directives on an element."

### QDiv to apply Quasar Directives

```python
import justpy as jp

def quasar_example3():
    wp = jp.QuasarPage()
    d = jp.Div(classes='q-pa-md row justify-center', a=wp)
    jp.QDiv(v_ripple=True, classes='relative-position flex flex-center text-white bg-primary',
                style='border-radius: 3px; cursor: pointer; height: 150px; width: 80%;',
                a=d, text='Click/tap me')
    return wp

jp.justpy(quasar_example3)
```

The value of the directive can be a dictionary for configuring more options:
### QDiv directive as dictionary
[Ripple Example live demo]({{demo_url}}/ripple_test)
```python
import justpy as jp
# https://quasar.dev/vue-directives/material-ripple#Ripple-API

def ripple_test():
    """
    show the Quasar ripple effect
    """
    wp = jp.QuasarPage()
    d = jp.QDiv(classes="q-pa-md q-gutter-md row justify-center", a=wp)
    d1 = jp.QDiv(
      v_ripple={'center': True, 'color': 'orange-5'},
      classes="relative-position container bg-grey-3 text-black inline flex flex-center",
      text='center',
      style='border-radius: 50%; cursor: pointer; width: 150px; height: 150px', a=d)
    return wp

jp.justpy(ripple_test)
```

## Running Quasar Component Methods

In order to run Quasar methods use the `run_method` method of the JustPy Quasar component.

The following example runs the start() and stop() methods of [QAjaxBar](https://quasar.dev/vue-components/ajax-bar#QAjaxBar-API)

!!! warning
    You must set `temp=False` when the component is created because this generates an id for the element without which `run_method` will not work

```python
import justpy as jp

async def start_bar(self, msg):
    wp = msg.page
    await wp.ajax_bar.run_method('start()', msg.websocket)

async def stop_bar(self, msg):
    wp = msg.page
    await wp.ajax_bar.run_method('stop()', msg.websocket)


def bar_example():
    wp = jp.QuasarPage()
    d = jp.Div(classes='q-pa-md', a=wp)
    # temp=False is important because this generates an id for the element that is required for run_method to work
    wp.ajax_bar = jp.QAjaxBar(position='bottom', color='accent', size='10px', skip_hijack=True, a=d, temp=False)
    btn_start = jp.QBtn(color='primary', label='Start Bar', a=d, click=start_bar, style='margin-right: 20px')
    btn_stop = jp.QBtn(color='primary', label='Stop Bar', a=d, click=stop_bar)
    return wp

jp.justpy(bar_example)

```
