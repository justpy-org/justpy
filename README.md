# JustPy
---
[JustPy Docs and Tutorials](https://elimintz.github.io/justpy)

## Introduction

JustPy is an object-oriented, component based, high-level Python Web Framework that requires no front-end programming. With a few lines of only Python code, you can create interactive websites without any JavaScript programming.  

When developing with JustPy, there is no front-end/back-end distinction. All programming is done on the back-end allowing a simpler and more Pythonic web development experience. JustPy removes the front-end/back-end distinction by intercepting the relevant events on the front-end and sending them to the back-end to be processed. This is a major difference from other frameworks that is hard to describe in words but will become evident when you see some concrete examples. 

In JustPy, elements on the web page are instances of component classes. A component in JustPy is a Python class. Customized, reusable components can be created from other components. Out of the box, JustPy comes with support for HTML and SVG components as well as more complex components such as charts and grids.  It also supports most of the components and the functionality of the [Quasar](https://quasar.dev/) library of [Material Design 2.0](https://material.io/) components.

JustPy encourages creating your own components and reusing them in different projects (and, if applicable, sharing these components with others). 

JustPy integrates nicely with [pandas](https://pandas.pydata.org/) and simplifies building web sites based on pandas analysis. 

JustPy supports visualization using [matplotlib](tutorial/matplotlib.md) and [Highcharts](charts_tutorial/introduction.md).

## Hello World!

```python
import justpy as jp

def hello_world():
    wp = jp.WebPage()
    d = jp.Div(text='Hello world!')
    wp.add(d)
    return wp
    
jp.justpy(hello_world)
```

The program above activates a web server that returns a web page with 'Hello world!' for any request. Locally, you would direct your browser to to http://localhost:8000/ or http://127.0.0.1:8000 to see the result.

Here is a slightly modified version in which 'Hello world!' changes to 'I was clicked!' when it is clicked.

```python
import justpy as jp

def my_click(self, msg):
    self.text = 'I was clicked!'

def hello_world():
    wp = jp.WebPage()
    d = jp.Div(text='Hello world!')
    d.on('click', my_click)
    wp.add(d)
    return wp

jp.justpy(hello_world)
```

## Under the Hood

JustPy's backend is built using: 
* [starlette](https://www.starlette.io/) - "a lightweight [ASGI](https://asgi.readthedocs.io/en/latest/) framework/toolkit, which is ideal for building high performance asyncio services".
* [uvicorn](https://www.uvicorn.org/) - "a lightning-fast [ASGI](https://asgi.readthedocs.io/en/latest/) server, built on [uvloop](https://github.com/MagicStack/uvloop) and [httptools](https://github.com/MagicStack/httptools)".

JustPy's frontend (which is transparent to JustPy developers) is built using: 
* [Vue.js](https://vuejs.org/) - "The Progressive JavaScript Framework"

The way JustPy removes the frontend/backend distinction is by intercepting the relevant events on the frontend and sending them to the backend to be processed. 

## License 

[Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0.txt)

Copyright (c) 2019, Eliezer Mintz
