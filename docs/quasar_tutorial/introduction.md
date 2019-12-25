# Quasar Introduction

## General

[Quasar](https://quasar.dev) is an MIT licensed open-source JavaScript framework that provides a comprehensive set of [Vue.js](https://vuejs.org/) components that follow the [Material Guidelines](https://material.io/). You can learn more about it [here](https://quasar.dev/introduction-to-quasar).

JustPy supports most of the Quasar components and their features. In JustPy, Quasar components, just like HTML components, are Python classes.

The Quasar documentation is excellent and includes many examples. You will need to consult it for the specifics of each component.

There are many Quasar components. I suggest browsing the documentation to see what is available.

The name of the Quasar component and the JustPy component is the same. If the Quasar component is called QMenu for example, the corresponding JustPy class is called QMenu also.  

I will be adding examples to this tutorial over time.

!> Quasar uses its own [classes](https://quasar.dev/style/typography) to style elements on the page, so do not use Tailwind classes on Quasar pages.

## Example

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

def quasar_example():
    wp = jp.QuasarPage(dark=True)  # Load page in dark mode
    d = jp.Div(classes='q-pa-md q-gutter-sm', a=wp)
    jp.QBtn(color='primary', icon='mail', label='On Left', a=d, click=my_click)
    jp.QBtn(color='secondary', icon_right='mail', label='On Right', a=d, click=my_click)
    jp.QBtn(color='red', icon='mail', icon_right='send', label='On Left and Right', a=d, click=my_click)
    jp.Br(a=d)
    jp.QBtn(icon='phone', label='Stacked', stack=True, glossy=True, color='purple', a=d, click=my_click)
    return wp

jp.justpy(quasar_example)
```

The program uses the JustPy QBtn component which is based on the [Quasar QBtn component](https://quasar.dev/vue-components/button). Click the buttons and notice the ripple effect which is part of the Material specification.

The JustPy component usually support all the Quasar component options (in the Quasar docs these are called `props`). In JustPy these are designated by setting the attributes of the element. This can be done at creation using keywords or later using standard attribute assignment. 

Quasar props are in kebab case: `icon-right` 
In JustPy the attribute names are in snake case: `icon_right`


## Parsing Quasar Tags

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

def quasar_example():
    wp = jp.QuasarPage()
    c = jp.parse_html(html_string, a=wp)
    for i in c.commands:
        print(i)
    return wp

jp.justpy(quasar_example)
```


## Quasar Directives

JustPy supports the following Quasar Vue directives:
'v-close-popup', 'v-close-menu', 'v-ripple', 'v-model', 'v-close-dialog'

!> In JustPy the directives are specified in snake case: `v_close_popup` instead of `v-close-popup`

```python
import justpy as jp

def quasar_example():
    wp = jp.QuasarPage()
    d = jp.Div(classes='q-pa-md row justify-center', a=wp)
    jp.QDiv(v_ripple=True, classes='relative-position flex flex-center text-white bg-primary',
                style='border-radius: 3px; cursor: pointer; height: 150px; width: 80%;',
                a=d, text='Click/tap me')
    return wp

jp.justpy(quasar_example)
```

!> Use QDiv instead of Div if you want to apply directives on an element.


