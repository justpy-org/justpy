# Introduction

## What is JustPy?

JustPy is an object-oriented, component based, high-level Python Web Framework that requires no front-end programming. With a few lines of only Python code, you can create interactive websites with no need for JavaScript programming.  

When developing with JustPy, there is no frontend/backend distinction. All programming is done on the backend allowing a simpler and more Pythonic web development experience. This is a major difference from other frameworks that is hard to describe in words but will become evident when you see some concrete examples. 

!> The best way to understand JustPy is to follow the [tutorial](tutorial/getting_started.md). 

In JustPy, elements on the web page are instances of component classes. A component in JustPy is a Python class. Customized, reusable components can be created from other components. Out of the box, JustPy comes with support for HTML and SVG components as well as more complex components such as charts and grids.  It also supports most of the components and the functionality of the [Quasar](https://quasar.dev/) library of [Material Design 2.0](https://material.io/) components. 

JustPy integrates seamlessly with [pandas](https://pandas.pydata.org/) and makes it simple to build web sites based on pandas analysis. With a simple command you can create an interactive [Highcharts chart](https://www.highcharts.com/) or [Ag-Grid grid](https://www.ag-grid.com/) from a pandas data frame.  

!> One time only marketing pitch: **Experimenting with JustPy is worth your time. It has made me an order of magnitude more productive. You will be surprised how little code is required to develop sophisticated web sites**

Hopefully, JustPy enables teaching web development in introductory Python courses by reducing the technologies that need to be mastered to basically only Python and reducing the complexity of web development.


## Hello World

```python
import justpy as jp

def hello_world():
    wp = jp.WebPage()
    d = jp.Div(text='Hello world!')
    wp.add(d)
    return wp
    
jp.justpy(hello_world)
```

That's it. The program above activates a web server that returns a web page with 'Hello world!' for any request. Locally, you would go to http://localhost:8000/ or http://127.0.0.1:8000 to see the result.
   

## Under the Hood

JustPy's backend is built using: 
* [starlette](https://www.starlette.io/) - "a lightweight [ASGI](https://asgi.readthedocs.io/en/latest/) framework/toolkit, which is ideal for building high performance asyncio services".
* [uvicorn](https://www.uvicorn.org/) - "a lightning-fast [ASGI](https://asgi.readthedocs.io/en/latest/) server, built on [uvloop](https://github.com/MagicStack/uvloop) and [httptools](https://github.com/MagicStack/httptools)".

JustPy's frontend (which is transparent to JustPy developers) is built using: 
* [Vue.js](https://vuejs.org/) - "The Progressive JavaScript Framework"

The way JustPy removes the frontend/backend distinction is by intercepting the relevant events on the frontend and sending them to the backend to be processed. 

## License 

[Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0.txt)

Copyright (c) 2018-present, Eliezer Mintz
