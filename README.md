# JustPy

[![pypi](https://img.shields.io/pypi/pyversions/justpy)](https://pypi.org/project/justpy/)
[![Github Actions Build](https://github.com/elimintz/justpy/workflows/Build/badge.svg?branch=master)](https://github.com/elimintz/justpy/actions?query=workflow%3ABuild+branch%3Amaster)
[![PyPI Status](https://img.shields.io/pypi/v/justpy.svg)](https://pypi.python.org/pypi/justpy/)
[![Downloads](https://pepy.tech/badge/justpy)](https://pepy.tech/project/justpy)
[![GitHub issues](https://img.shields.io/github/issues/elimintz/justpy.svg)](https://github.com/elimintz/justpy/issues)
[![GitHub closed issues](https://img.shields.io/github/issues-closed/elimintz/justpy.svg)](https://github.com/elimintz/justpy/issues/?q=is%3Aissue+is%3Aclosed)
[![License](https://img.shields.io/github/license/elimintz/justpy.svg)](https://www.apache.org/licenses/LICENSE-2.0)

## Docs and Tutorials
[JustPy Docs and Tutorials](https://justpy.io)

## Live Demos
[nicegui](https://nicegui.io/)
[justpy demos](https://jpdemo.bitplan.com)

## Questions and Discussions
Please file Bugs you found checking the issues Badge Link above.

Questions which involve details of upstream frameworks such as 
Quasar, Tailwind, Highcharts are best ask involving a larger community via 

[stackoverflow questions](https://stackoverflow.com/questions/tagged/justpy)

and tagging your question with both "justpy" and the tag or the specific library your are asking a question for

Our github dicussions are categorized. Please use the Category "Ideas" for feature requests. 
[github discussions](https://github.com/elimintz/justpy/discussions)

## Trying out with docker
```bash
git clone https://github.com/elimintz/justpy
scripts/rundocker -h
scripts/rundocker test
scripts/rundocker example dogs
scripts/rundocker dev
```
## Introduction

JustPy is an object-oriented, component based, high-level Python Web Framework that requires no front-end programming. With a few lines of only Python code, you can create interactive websites without any JavaScript programming. JustPy can also be used to create graphic user interfaces for Python programs. 

Unlike other web frameworks, JustPy has no front-end/back-end distinction. All programming is done on the back-end allowing a simpler, more productive, and more Pythonic web development experience. JustPy removes the front-end/back-end distinction by intercepting the relevant events on the front-end and sending them to the back-end to be processed. 

In JustPy, elements on the web page are instances of component classes. A component in JustPy is a Python class that allows you to instantiate reusable custom elements whose functionality and design is encapsulated away from the rest of your code. 

Custom components can be created using other components as building blocks. Out of the box, JustPy comes with support for [HTML](https://justpy.io/#/tutorial/html_components) and [SVG](https://justpy.io/#/tutorial/svg_components) components as well as more complex components such as [charts](https://justpy.io/#/charts_tutorial/introduction) and [grids](https://justpy.io/#/grids_tutorial/introduction).  It also supports most of the components and the functionality of the [Quasar](https://quasar.dev/) library of [Material Design 2.0](https://material.io/) components.

JustPy encourages creating your own components and reusing them in different projects (and, if applicable, sharing these components with others). 

JustPy supports visualization using [matplotlib](https://justpy.io/#/tutorial/matplotlib) and [Highcharts](https://justpy.io/#/charts_tutorial/introduction).

JustPy integrates nicely with [pandas](https://pandas.pydata.org/) and simplifies building web sites based on pandas analysis. JustPy comes with a [pandas extension](https://justpy.io/#/charts_tutorial/pandas?id=using-the-pandas-extension) that makes it simple to create interactive charts and grids from pandas data structures.

For updates and news please follow the [JustPy Twitter account](https://twitter.com/justpyframework)

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

The program above activates a web server that returns a web page with 'Hello world!' for any request. Locally, you would direct your browser to http://127.0.0.1:8000 or http://localhost:8000/ or  to see the result.

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

Many other examples can be found in the [tutorial](https://justpy.io/#/tutorial/getting_started)

## Under the Hood

JustPy's backend is built using: 
* [starlette](https://www.starlette.io/) - "a lightweight [ASGI](https://asgi.readthedocs.io/en/latest/) framework/toolkit, which is ideal for building high performance asyncio services".
* [uvicorn](https://www.uvicorn.org/) - "a lightning-fast [ASGI](https://asgi.readthedocs.io/en/latest/) server, built on [uvloop](https://github.com/MagicStack/uvloop) and [httptools](https://github.com/MagicStack/httptools)".

JustPy's frontend (which is transparent to JustPy developers) is built using: 
* [Vue.js](https://vuejs.org/) - "The Progressive JavaScript Framework"

The way JustPy removes the frontend/backend distinction is by intercepting the relevant events on the frontend and sending them to the backend to be processed. 

## License 

[Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0.txt)

Copyright (c) 2019-2022, Eliezer Mintz
