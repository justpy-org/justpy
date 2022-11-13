# The Basic Concepts

## JustPy Components
JustPy components are classes that instantiate reusable elements that can be be rendered in a browser.
Out of the box, JustPy comes with many components. You can use the available JustPy components
and also build more complex components using other components as building blocks.

In JustPy, components are implemented as Python classes. When you define a new component, you do so by defining a new Python class.

A JustPy element is an instance of a component class.

```python
import justpy as jp
p = jp.P()
p.text = "Hello!"
```

In the example above, `p` is an instance of the class `P`. Its text attribute is set to 'Hello!'.
The above is similar to the HTML element:
```html
<p>Hello!</p>
```

You can set the JustPy element attributes when the element is created (synonym for instantiated) using keyword arguments to make code shorter and clearer:
```python
import justpy as jp
p = jp.P(text="Hello!")
```

Just creating an element is not very useful. We need to get it on a web page and into the user's browser tab. We will do this next.

## JustPy Web Pages

In JustPy, web pages are instances of the JustPy class `WebPage`. You create a web page the same way you create any class instance in Python:
```python
import justpy as jp
wp = jp.WebPage()
```  

In the example above we created the web page `wp`. It is an empty web page that does not contain any elements.

Let's create an element and add it to the page:
```python
import justpy as jp
wp = jp.WebPage()
p = jp.P(text="Hello World!")
wp.add(p)  # Same as p.add_to(wp), wp = wp + p, wp += p
```

In the example above, we create a web page. Then we create a `p` element and add it to the page using the `add` method.

Since adding an element to a page is very common, there is a way to do so using the keyword argument `a`:
```python
import justpy as jp
wp = jp.WebPage()
p = jp.P(text="Hello World!", a=wp)
```

This code snippet has the same functionality as the one above it.

## JustPy Requests

So far we have created a page and added an element to it. We haven't yet loaded the page into the user's browser.

!!! note
    In this tutorial, I will call the process of delivering a Web page to a user "**rendering the page**".

When you type a URL into your browser's [Address Bar](https://en.wikipedia.org/wiki/Address_bar) and tell your browser to navigate to that address,
the browser generates a request; it requests data from the server the URL you entered points to.

When a request comes from a browser, the JustPy framework runs a user defined function.
This function must return a web page which is then rendered in the browser that sent the request. All that you as a developer need to do is write the function that takes a request and returns a web page.
The framework takes care of the rest.

Here is a basic example:

## First Hello World
[First Hello World live demo]({{demo_url}}/hello_world1)

```python
import justpy as jp

def hello_world1():
    wp = jp.WebPage()
    p = jp.P(text="Hello World!", a=wp)
    return wp

jp.justpy(hello_world1)
```

The function `hello_world1` creates a web page, adds a paragraph element to it and returns the page.

!!! note
    **In this tutorial, functions like `hello_world` will be called "request handlers".**

The `jp.justpy(hello_world1)` command starts a web server and sends all requests to the function `hello_world1`.

Run the program above (as explained in [getting started](../getting_started/#running-the-program) ).
You should see 'Hello World!' in your browser.

## More Hello World
[More Hello World live demo]({{demo_url}}/hello_world2)

Saying hello once isn't enough! We would like to say "hello" ten times. We also want to let the user know how many times we said "hello". More specifically, we would like "Hello World!" to show up ten times on the page and be enumerated. In addition, we would like to use a bigger font each time.

```python
import justpy as jp

def hello_world2():
    wp = jp.WebPage()
    for i in range(1,11):
        jp.P(text=f"{i}) Hello World!", a=wp, style=f"font-size: {10*i}px")
    return wp

jp.justpy(hello_world2)
```

Run the program above and look at the result in your browser.

!!! warning
    **Don't forget to terminate the previous program first.**  
Two JustPy servers cannot run at the same time on the same port.

The P instances are created inside a loop with the loop index being used to give each paragraph some different text and a different font size.

The `style` attribute in JustPy is the same as the HTML [style](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/style) attribute. It allows using [CSS](https://developer.mozilla.org/en-US/docs/Web/CSS) properties to style the element.

For example, change the style assignment to:
```python
style=f"color: blue; font-size: {10*i}px"
```
and see what happens.

## Tailwind and JustPy
[Tailwind and JustPy live demo]({{demo_url}}/hello_world3)

Another way to style elements is to use classes.
By default, instances of WebPage support styling using [Tailwind](https://tailwindcss.com/) classes. If you are familiar with CSS, checkout Tailwind. For me, it is a joy to work with.

!!! info
    You can also put your own CSS on a page and use your own class definitions by setting the `css` attribute of a page.

Let's use Tailwind classes to style our page:

```python
import justpy as jp

def hello_world3():
    wp = jp.WebPage()
    my_paragraph_design = "w-64 bg-blue-500 m-2 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
    for i in range(1,11):
        jp.P(text=f"{i}) Hello World!", a=wp, classes=my_paragraph_design)
    return wp

jp.justpy(hello_world3)
```

In this program Tailwind classes are used to make the output a little nicer. The JustPy attribute `classes` is equivalent to the HTML attribute [class](https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/class) (which is a reserved word in Python).

## Creating Web Pages Once
[Creating Web Pages Once live demo]({{demo_url}}/hello_world4)

You may have noticed that since we have been serving the same page to everyone, there is no need to create a new page each time a request is made.
We can create a page one time, and serve the same page for all requests:
```python
import justpy as jp

wp = jp.WebPage(delete_flag=False)
my_paragraph_design = "w-64 bg-blue-500 m-2 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
for i in range(1,11):
    jp.P(text=f"{i}) Hello World!", a=wp, classes=my_paragraph_design)

def hello_world4():
    return wp

jp.justpy(hello_world4)
```

!!! info
    When you define a page that is going to be rendered in more than one browser tab or page, you need to set its `delete_flag` to `False`.

Otherwise, the page (the instance of `WebPage` to be precise) will be deleted when a browser tab or window that renders that page is closed.
The default is for JustPy to remove all references to the page and the elements on it so that the Python garbage collector can reclaim the memory.

!!! warning
    When a page's (or element's) `delete_flag` is set to `False`, none of its child elements will be deleted, even if their `delete_flag` is `True`.

In the next part of the tutorial you will learn how to deal with events such as a mouse click.
