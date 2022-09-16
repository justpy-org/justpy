# HTML Components

JustPY supports components corresponding to HTML and SVG tags. The name of the component is the same as the name of the HTML tag with the first letter capitalized. For example, we already saw the `Div` and `P` components that correspond to the the `div` and `p` HTML tags. JustPy supports all tags that put elements on the page and are not deprecated in HTML 5.

## Simple example with three HTML components

```python
import justpy as jp

def html_comps1():
    wp = jp.WebPage()
    jp.I(text='Text in Italic', a=wp)
    jp.Br(a=wp)
    jp.Strong(text='Text in the Strong element', a=wp)
    return wp

jp.justpy(html_comps1)
```

* The [i](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/i) HTML tag displays text typically in italics.
* The [br](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/br) HTML tag produces a line break.
* The [strong](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/strong) HTML tag is typically rendered in bold type.

The JustPy function `get_tag`, creates an instance of a component based on the HTML tag. Its first argument is a string with the tag and the rest of the arguments are the identical optional keyword arguments for the class `__init__` method. The program below is equivalent to the one above:

## Simple example with three HTML components using get_tag

```python
import justpy as jp

def html_comps2():
    wp = jp.WebPage()
    jp.get_tag('i', text='Text in Italic', a=wp)
    jp.get_tag('br',a=wp)
    jp.get_tag('br',a=wp)
    jp.get_tag('br',a=wp)
    jp.get_tag('br',a=wp)
    jp.get_tag('strong', text='Text in the Strong element', a=wp)
    return wp

jp.justpy(html_comps2)
```

It is also possible to get the same formatting using the the `Div` component with the appropriate Tailwind classes:

## Tailwind formatting with Div

```python
import justpy as jp

def html_comps3():
    wp = jp.WebPage()
    jp.Div(text='Text in italic', a=wp, classes='italic')
    jp.Div(text='Text in bold', a=wp, classes='font-bold')
    return wp

jp.justpy(html_comps3)
```

If you do not need the semantic information the specialized tags provide, it is more convenient to use `Div`, `P`, or `Span` with the appropriate Tailwind classes or style attribute.

## Container Elements

Many HTML elements can have children elements. In JustPy parlance, an element can contain other elements.

```python
import justpy as jp

def html_comps4():
    wp = jp.WebPage()
    for i in range(10):
        d = jp.Div(a=wp, classes='m-2')
        for j in range(10):
            jp.Span(text=f'Span #{j+1} in Div #{i+1}', a=d, classes='text-white bg-blue-700 hover:bg-blue-200 ml-1 p-1')
    return wp

jp.justpy(html_comps4)
```

In the program above, in each iteration of the outer loop a new `Div` element is created and in the inner loop, ten `Span` elements are added to it. This is done using the `a=d` keyword argument.

Change the element created in the inner loop from a `Span` to a `Div`, `P`, or `I` and see what happens.

## Common Attributes

HTML components have common attributes as well as specific ones. JustPy components support the following [global attributes](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes) for all HTML components:
`contenteditable`, `dir`, `tabindex`, `title`, `accesskey`, `draggable`, `lang`, `hidden`

In this example we use the `contenteditable`, `dir`, and `lang` attributes:

```python
import justpy as jp

def html_comps5():
    wp = jp.WebPage()
    for j in range(10):
        p = jp.P(text=f'אני אוהב לתכנת בפייתון', a=wp, contenteditable=True, classes='text-white bg-blue-500 hover:bg-blue-700 ml-1 p-1 w-1/2')
        p.dir = 'rtl'
        p.lang = 'he'
    return wp

jp.justpy(html_comps5)
```

The text in each P element is made editable by setting `contenteditable` to `True` (using a keyword argument). We set `dir` to "rtl" (right-to-left) and `lang` to "he" (the language code for Hebrew). We do so by setting the attribute directly though we could have used a keyword argument.

Run the program and try editing some text. You will see also that the Hebrew text is rendered right to left.

## Specific Attributes

Some components have specific attributes. For example, the   [img HTML tag](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/img) has the `src` attribute that specifies the URL for the image.
Run the following program:
```python
import justpy as jp

def html_comps6():
    wp = jp.WebPage()
    for degree in range(0, 361, 10):
        image = jp.Img(src='https://www.python.org/static/community_logos/python-powered-h-140x182.png', a=wp)
        image.classes = 'm-4 p-4 inline-block'
        image.style = f'transform: rotate({degree}deg)'
        image.height = 100
        image.width = 100
        image.degree = degree

        def straighten1(self, msg):
            self.style = f'transform: rotate(0deg)'

        def rotate_back1(self, msg):
            self.style = f'transform: rotate({self.degree}deg)'

        def no_rotate1(self, msg):
            self.degree = 0
            self.set_class('bg-red-200')

        image.on('mouseenter', straighten1)
        image.on('mouseleave', rotate_back1)
        image.on('click', no_rotate1)

    return wp

jp.justpy(html_comps6)
```

The program renders on the page a progression of images of the **Python Powered** logo each rotated 10 degrees relative to the former image. When the mouse enters an image, it "straightens" and when it leaves, it returns to its original rotation. If you click on an image, it does not rotate anymore.

The images are added inside a loop. In each iteration of the loop, an image is added to the page. The `src` attribute designates where to fetch the image from, in our case the [python.org](https://www.python.org) website. As you see in this example, you can combine Tailwind classes (or any CSS classes) with setting the `style` attribute. Here, the style is set to [rotate](https://developer.mozilla.org/en-US/docs/Web/CSS/transform-function/rotate) the image based on the loop variable. We also set the height and width attributes of the image to 100.

The program then sets the `degree` attribute of the image to the loop variable. It will be used in the event handlers that define the interaction with the mouse.

!!! note
    `degree` is a different kind of attribute than `src`, `height`, and `width`. It is a user defined attribute that is not part of the HTML specification. In the JustPy component definitions, attributes that are part of the HTML specification are explicitly identified and handled accordingly.

The mouse event handlers change the `style` and `class` attributes of the element as needed using the `degree` attribute of the image if required. For clarity, the event handlers are defined inside the loop, but they could be defined just once outside the loop or outside the request handler. We could also set the attributes as keyword arguments and the result is the following:

## Setting Attributes with keyword arguments
```python
import justpy as jp

def straighten2(self, msg):
    self.style = f'transform: rotate(0deg)'

def rotate_back2(self, msg):
    self.style = f'transform: rotate({self.degree}deg)'

def no_rotate2(self, msg):
    self.degree = 0
    self.set_class('bg-red-200')

def html_comps7():
    wp = jp.WebPage()
    for degree in range(0, 361, 10):
        jp.Img(src='https://www.python.org/static/community_logos/python-powered-h-140x182.png', a=wp,
                classes='m-4 p-4 inline-block', style=f'transform: rotate({degree}deg)', height=100, width=100,
                degree=degree, mouseenter=straighten2, mouseleave=rotate_back2, click=no_rotate2)
    return wp

jp.justpy(html_comps7)
```

## HTML Links

In JustPy you create hyperlinks using the `A` component which corresponds to the [`a` HTML tag](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/a).

The `A` component is also named `Link` (in case you want to use a more descriptive name).

### simple python.org link

```python
import justpy as jp

def link_demo1():
    wp = jp.WebPage()
    jp.A(text='Python Org', href='https://python.org', a=wp, classes='m-2 p-2 text-xl text-white bg-blue-500 hover:bg-blue-700')
    return wp

jp.justpy(link_demo1)

```

The link above goes to the Python.org web page. If you want the link to open in a new window, set the `target` attribute of the `A` component instance to '_blank'

If you want to link to an element on the page, use the `bookmark` attribute and assign to it the element you want to link to. If you want to scroll to the element, instead of jumping instantly, set the `scroll` attribute to `True`.

### scroll example
```python
import justpy as jp

def link_demo2():
    wp = jp.WebPage()
    link = jp.A(text='Scroll to target', a=wp, classes='inline-block m-2 p-2 text-xl text-white bg-blue-500 hover:bg-blue-700')
    # jp.Br(a=wp)
    for i in range(50):
        jp.P(text=f'{i+1} Not a target', classes='m-1 p-1 text-white bg-blue-300', a=wp)
    target = jp.A(text=f'This is the target - it is linked to first link, click to jump there', classes='inline-block m-1 p-1 text-white bg-red-500', a=wp)
    link.bookmark = target
    link.scroll = True
    target.bookmark = link
    for i in range(50):
        jp.P(text=f'{i+50} Not a target', classes='m-1 p-1 text-white bg-blue-300', a=wp)
    return wp

jp.justpy(link_demo2)
```

## Lists

The [ul tag](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/ul) together with the [li tag](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/ul) can be used to create lists. The corresponding JustPy components are `Ul` and `Li`.
```python
import justpy as jp

def list_demo():
    wp = jp.WebPage()
    my_list = jp.Ul(a=wp, classes='m-2 p-2')
    for i in range (1,11):
        jp.Li(text=f'List one item {i}', a=my_list)
    my_list = jp.Ul(a=wp, classes='m-2 p-2 list-disc list-inside')
    for i in range(1, 11):
        jp.Li(text=f'List two item {i}', a=my_list, classes='hover:bg-gray-200')
    my_list = jp.Ul(a=wp, classes='m-2 p-2 list-decimal list-inside')
    for i in range(1, 11):
        jp.Li(text=f'List three item {i}', a=my_list)
    return wp

jp.justpy(list_demo)
```

The program above creates three lists. Use the [`list-disc` and `list-decimal`](https://tailwindcss.com/docs/list-style-type) Tailwind classes to get bulleted or numeric lists. The [`list-inside`](https://tailwindcss.com/docs/list-style-position) class controls the positions of the markers of the list. If you choose to put them outside, make sure there is enough room to render them.

## Showing and Hiding Elements

All JustPy components use the `show` boolean attribute to determine whether an element should be rendered on the page. If `show` is `False`, the element will not be on the page at all.

If you want the element to be on the page, but be invisible, use the `visible` and `invisible` Tailwind classes (or appropriate `style` values). When an element is invisible, the page structure stays the same.

Run the following program and see the difference by clicking both buttons.

```python
import justpy as jp

button_classes='m-2 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded'

def show_demo():
    wp = jp.WebPage()
    b = jp.Button(text='Click to toggle show', a=wp, classes=button_classes)
    d = jp.Div(text='Toggled by show', classes='m-2 p-2 text-2xl border w-48', a=wp)
    b.d = d
    jp.Div(text='Will always show', classes='m-2', a=wp)

    def toggle_show(self, msg):
        self.d.show = not self.d.show

    b.on('click', toggle_show)

    b = jp.Button(text='Click to toggle visibility', a=wp, classes=button_classes)
    d = jp.Div(text='Toggled by visible', classes='m-2 p-2 text-2xl border w-48', a=wp)
    d.visibility_state = 'visible'
    b.d = d
    jp.Div(text='Will always show', classes='m-2', a=wp)

    def toggle_visible(self, msg):
        if self.d.visibility_state == 'visible':
            self.d.set_class('invisible')
            self.d.visibility_state = 'invisible'
        else:
            self.d.set_class('visible')
            self.d.visibility_state = 'visible'

    b.on('click', toggle_visible)
    return wp

jp.justpy(show_demo)
```
