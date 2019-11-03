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
p.text = 'Hello!'
``` 

In the example above, `p` is an instance of the class `P`. It's text attribute is set to 'Hello!'.
The above is equivalent to the HTML element:
```html
<p>Hello!</p>
```

You can set the JustPy element attributes when the element is created (synonym for instantiated) using keyword arguments to make code shorter and clearer:
```python
import justpy as jp
p = jp.P(text='Hello!')
``` 

Just creating an element is not very useful. We need to get it on a Web page and into the user's browser tab. We will do this next.

## JustPy Web Pages

In JustPy, Web pages are instances of the JustPy class `WebPage`. You create a Web page the same way you create any class instance in Python:
```python
import justpy as jp
wp = jp.WebPage()
```  

In the example above we created the Web page `wp`. It is an empty Web page that does not contain any elements.

Let's create an element and add it to the page:
```python
import justpy as jp
wp = jp.WebPage()
p = jp.P(text='Hello World!')
wp.add(p)
```

In the example above, we create a Web page. Then we create a the `p` element add it to the page using the `add` method.

Since adding an element to a page is very common, there is a way to do so using the keyword parameter `a`: 
```python
import justpy as jp
wp = jp.WebPage()
p = jp.P(text='Hello World!', a=wp)
```

Both code snippets have identical functionality.

## JustPy Requests

So far we have created a page and added an element to it. We haven't yet loaded the page into the user's browser.
I will call the process of delivering a Web page to a user "rendering the page" in this tutorial.

When you type a URL into your browser's [Address Bar](https://en.wikipedia.org/wiki/Address_bar) and tell your browser to navigate to that address,
the browser generates a request; it requests data from the server the URL you entered points to. 

When a request comes from a browser, the JustPy framework runs a user defined function. 
This function must return a web page which is then rendered in the browser that sent the request. All the user needs to do is write the function that takes a request and returns a web page.
The framework takes care of the rest.

## Hello World

It is simpler to demonstrate this than to explain:
```python
import justpy as jp

def hello_world():
    wp = jp.WebPage()
    p = jp.P(text='Hello World!', a=wp)
    return wp

jp.justpy(hello_world)
```

The function `hello_world` creates a web page, adds a paragraph element to it and returns the page.
The `jp.justpy(hello_world)` command tells starts a web server and sends all requests to the function `hello_world'.

Run the program above (as explained in [getting started](tutorial/getting_started.md#Run "Getting Started") ).
You should see 'Hello World!' on the page.

## More Hello World

Saying hello once isn't enough! We would like to say hello ten times. We also want to let the user know how many times we said hello. In other words, we would like 'Hello World!' to show up ten times on the page and be enumerated. In addition, we would like to say hello using a bigger font each time. 

```python
import justpy as jp

def hello_world():
    wp = jp.WebPage()
    for i in range(1,11):
        jp.P(text=f'{i}) Hello World!', a=wp, style=f'font-size: {10*i}px')
    return wp

jp.justpy(hello_world)
```
 
Run the program above  and look at the result in your browser. Don't forget to terminate the previous program first. 
Two JustPy servers cannot run at the same time on one machine.
The P instances are created inside a loop with the loop index being used to give each paragraph different text and a different font size. 
The style attribute in JustPy is the same as the HTML style attribute. 
It allows using CSS properties to style the element. For example, change the style assignment to 
```python
style=f'color: blue; font-size: {10*i}px' 
```
and see what happens.

## Tailwind and JustPy

Another way to style elements on the web page is to use classes.
By default, instances of WebPage support all [Tailwind](https://tailwindcss.com/) classes. If you are familiar with CSS, checkout Tailwind. It is a joy to work with.
You can also put your own CSS on a page by setting the `css` attribute of a page.

Let's use Tailwind classes to style our page:

```python
import justpy as jp

def hello_world():
    wp = jp.WebPage()
    my_paragraph_design = "w-64 bg-blue-500 m-2 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
    for i in range(1,11):
        jp.P(text=f'{i}) Hello World!', a=wp, classes=my_paragraph_design)
    return wp

jp.justpy(hello_world)
```

In this program Tailwind classes are used to make the output a little nicer. The JustPy attribute classes is equivalent to the HTML attribute class (which is a reserved word in Python).
 
## Creating Web Pages Once

You may have noticed that since we have been serving the same page to everyone, there is no need to create a new page each time a request is made.
We can create a page one time, and serve the same page for all requests like so:
```python
import justpy as jp

wp = jp.WebPage(delete_flag=False)
my_paragraph_design = "w-64 bg-blue-500 m-2 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
for i in range(1,11):
    jp.P(text=f'{i}) Hello World!', a=wp, classes=my_paragraph_design)

def hello_world():
    return wp

jp.justpy(hello_world)
```

When you define a page that is going to be rendered on more than one browser, you need to set its delete_flag to False.
Otherwise, the page (the instance of `WebPage` to be precise) will be deleted when a browser tab or window that renders that page is closed.
The default is for JustPy to remove all references to the page and the components on it so that the Python garbage collector can reclaim the memory. 
When a page's (or component's) delete_flag is set to False, none of its child components will be deleted, even if their delete_flag is True. 

In the next part of the tutorial you will learn how to deal with events such as a mouse click happening in the browser.
 
