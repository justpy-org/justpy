# Parsing and Using HTML

## Introduction

JustPy provides several way of working directly with HTML.

If you don't need any events associated with your HTML just set the `inner_html` of a Div instance as described below.

In order to interact with the HTML, you need to use `parse_html` to convert the HTML to JustPy commands that create the appropriate elements. You can then assign event handlers to the elements.

##  The inner_html Attribute

You can set the content of an element by assigning a HTML string to the element's `inner_html` attribute. This is the preferred method if you don't need to interact with the HTML. As a general rule, if you are not using the `name_dict` attribute created by `parse_html`, you probably should use `inner_html` instead.

```python
import justpy as jp

my_html = """
    <div>
    <p class="m-2 p-2 text-red-500 text-xl">Paragraph 1</p>
    <p class="m-2 p-2 text-blue-500 text-xl">Paragraph 2</p>
    <p class="m-2 p-2 text-green-500 text-xl">Paragraph 3</p>
    </div>
    """

def inner_demo():
    wp = jp.WebPage()
    d = jp.Div(a=wp, classes='m-4 p-4 text-3xl')
    d.inner_html = '<pre>Hello there. \n How are you?</pre>'
    jp.Div(a=wp, inner_html=my_html)
    for color in ['red', 'green', 'blue', 'pink', 'yellow', 'teal', 'purple']:
        jp.Div(a=wp, inner_html=f'<p class="ml-2 text-{color}-500 text-3xl">{color}</p>')
    return wp

jp.justpy(inner_demo)
```

!!! warning
    if you set `inner_html`, it will override any other content of your component.

## Inserting HTML at the WebPage level

You can inject HTML directly into the page by setting the `html` attribute of a WebPage instance.

```python
import justpy as jp

def html_demo():
    wp = jp.WebPage()
    jp.Div(text='This will not be shown', a=wp)
    wp.html = '<p class="text-2xl m-2 m-1 text-red-500">Hello world!<p>'
    jp.Div(text='This will not be shown', a=wp)
    return wp

jp.justpy(html_demo)
```

If the `html` attribute is set, all other additions to the page will be ignored.


## The parse_html Function

To convert HTML to JustPy elements, use the `parse_html` function.

```python
import justpy as jp

async def parse_demo1(request):
    wp = jp.WebPage()
    c = jp.parse_html("""
    <div>
    <p class="m-2 p-2 text-red-500 text-xl">Paragraph 1</p>
    <p class="m-2 p-2 text-blue-500 text-xl">Paragraph 2</p>
    <p class="m-2 p-2 text-green-500 text-xl">Paragraph 3</p>
    </div>
    """, a=wp)
    print(c)
    print(c.components)
    return wp

jp.justpy(parse_demo1)
```

Run the program above. It renders the HTML on the page. The two `print` commands output the following:
```
Div(id: 1, html_tag: div, vue_type: html_component, number of components: 3)
[P(id: 2, html_tag: p, vue_type: html_component, number of components: 0), P(id: 3, html_tag: p, vue_type: html_component, number of components: 0), P(id: 4, html_tag: p, vue_type: html_component, number of components: 0)]
```

The printout shows that `c` is a `Div` component that has 3 child components that are `P` components. The parsing function takes HTML and creates JustPy elements with the right relationships between them. It returns the topmost component if there is only one. If there are two or more siblings at the top level, it wraps them with a Div and returns the div. You can think of `parse_html` as returning the element at the base of the HTML tree.

There are several way to access the child components. For example, in our specific case the first paragraph is the first child of `c` and therefore can be accessed as `c.components[0]`.

### The name_dict dictionary

A more general way to access parsed elements is to use the `name` attribute inside the HTML. The function `parse_html` attaches to the component it returns an attribute called `name_dict`, that as its name implies, is a dictionary whose keys are the name attributes and its values are the components they correspond to.

Here is an example:

```python
import justpy as jp

async def parse_demo2(request):
    wp = jp.WebPage()
    c = jp.parse_html("""
    <div>
    <p class="m-2 p-2 text-red-500 text-xl">Paragraph 1</p>
    <p class="m-2 p-2 text-blue-500 text-xl" name="p2">Paragraph 2</p>
    <p class="m-2 p-2 text-green-500 text-xl">Paragraph 3</p>
    </div>
    """, a=wp)
    p2 = c.name_dict['p2']
    def my_click(self, msg):
        self.text = 'I was clicked!'
    p2.on('click', my_click)
    return wp

jp.justpy(parse_demo2)
```

If you click the second paragraph, its text will change. Notice that we added `name="p2"` to the HTML of the second paragraph. When the parser sees the name attribute it creates an entry in `name_dict` with the name as the key and the component as the value.

If more than one element is given the same name in the HTML text, the dictionary value is a list with all the elements with that name.

`name_dict` is of type Dict so its fields can be accessed using dot notation. Instead of `c.name_dict['a']` you can use `c.name_dict.a`.

### Additional parsing functions
Along with parse_html there are two additional functions in JustPy to parse HTML: `parse_html_file` parses a file instead of a string and `parse_html_file_async` is a co-routine that does the same asynchronously.  


### The commands attribute

The `commands` attribute is created by `parse_html` and includes a list of the Python commands (represented as strings) needed to create the element in the JustPy framework.

```python
import justpy as jp

def commands_demo1():
    wp = jp.WebPage()
    c = jp.parse_html("""
        <div>
        <p class="m-2 p-2 text-red-500 text-xl">Paragraph 1</p>
        <p class="m-2 p-2 text-blue-500 text-xl">Paragraph 2</p>
        <p class="m-2 p-2 text-green-500 text-xl">Paragraph 3</p>
        </div>
        """, a=wp)
    for i in c.commands:
        print(i)
        jp.Div(text=i, classes='font-mono ml-2', a=wp)
    print()
    c = jp.parse_html("""
            <div>
            <p class="m-2 p-2 text-red-500 text-xl">Paragraph 1</p>
            <p class="m-2 p-2 text-blue-500 text-xl">Paragraph 2</p>
            <p class="m-2 p-2 text-green-500 text-xl">Paragraph 3</p>
            </div>
            """, a=wp, command_prefix='justpy.')
    for i in c.commands:
        print(i)
        jp.Div(text=i, classes='font-mono ml-2', a=wp)
    return wp

jp.justpy(commands_demo1)
```

The `command_prefix` keyword argument allows specifying the prefix for the commands. The default is 'jp.'

!!! warning
    All non blank prefixes should have the '.' (period) as their last character

We can then use the commands to generate the output we need without parsing HTML:
### commands result usage example
```python
import justpy as jp

def commands_demo2():
    wp = jp.WebPage()
    root = jp.Div(a=wp)
    c1 = jp.Div(a=root)
    c2 = jp.P(classes='m-2 p-2 text-red-500 text-xl', a=c1, text='Paragraph 1')
    c3 = jp.P(classes='m-2 p-2 text-blue-500 text-xl', a=c1, text='Paragraph 2')
    c4 = jp.P(classes='m-2 p-2 text-green-500 text-xl', a=c1, text='Paragraph 3')
    return wp

jp.justpy(commands_demo2)
```

The only change needed to the commands is to add `root` to the page.

### parse_html limitations

The parser does not handle correctly HTML in which top level text is divided.

The following HTML will not parse correctly:
```html
<div> First part of text <span> span text </span> second part of text</div>
```

This is because by design, JustPy has just one `text` attribute per element and so the parser discards the first part.

In order to parse the HTML correctly, make each element have undivided text:
```html
<div> <span>First part of text</span><span class="ml-1">span text </span> <span class="ml-1">second part of text</span></div>
```

Now each span has undivided text. The left margin class is required to so that there is a space between the spans. `parse_html` removes all white space before and after the text of the elements.

### Converting to HTML
Each component in JustPy also supports the `to_html()` method. It returns a string with the HTML representation of the element including all its child elements. You can think of it as the inverse of `parse_html()`.
