# Working with HTML


## The parse_html Function
Sometimes it is convenient to take regular HTML and convert it to JustPy elements. In order to do so we use the function `parse_html`.
```python
import justpy as jp

async def parse_demo(request):
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

jp.justpy(parse_demo)
```

Run the program above. It renders the HTML on the page. The two `print` commands output the following:
```
Div(id: 1, html_tag: div, vue_type: html_component, number of components: 3)
[P(id: 2, html_tag: p, vue_type: html_component, number of components: 0), P(id: 3, html_tag: p, vue_type: html_component, number of components: 0), P(id: 4, html_tag: p, vue_type: html_component, number of components: 0)]
```

The printout shows that `c` is a `Div` component that has 3 child components that are `P` components. The parsing function takes HTML and creates JustPy elements with the right relationships between them. It returns the topmost component if there is only one. If there are two or more siblings at the top level, it wraps them with a Div and returns the div. You can think of parse_html as returning the element at the base of the HTML tree.
 
There are several way to access the child components. For example, in our specific case the first paragraph is the first child of `c` and therefore can be accessed as `c.components[0]`.

A more general way is to use the `name` attribute inside the HTML. The function `parse_html` attaches to the component it returns an attribute called `name_dict`, that as its name implies, is a dictionary whose keys are the name attributes and its values are the components they correspond to. Here is an example:
```python
import justpy as jp

async def parse_demo(request):
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

jp.justpy(parse_demo)
```

If you click the second paragraph, its text will change. Notice that we added `name="p2"` to the HTML of the second paragraph. When the parser sees the name attribute it creates an entry in `name_dict` with the name as the key and the component as the value.

Along with parse_html there are two additional functions in JustPy to parse HTML: `parse_html_file` parses a file instead of a string and `parse_html_file_async` is a co-routine that does the same asynchronously.  

Each component in JustPy also supports the `to_html()` method. It converts a component to its HTML representation including all its child components. You can think of it as the inverse of `parse_html()`.

##  The inner_html Attribute

If we want to just insert HTML onto the page, we can do so using the `inner_html` attribute of any JustPy component.
```python
import asyncio
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

Be aware that if you set inner_html, it will override any other content of your component. 

Add: HTML at the page level
