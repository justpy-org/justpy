# JustPy
---

## Introduction

JustPy is an object-oriented, component based, high-level Python Web Framework that requires no front-end programming. With a few lines of only Python code, you can create interactive websites without any JavaScript programming. JustPy can also be used to create graphic user interfaces for Python programs.  

Unlike other web frameworks, JustPy has no front-end/back-end distinction. All programming is done on the back-end allowing a simpler, more productive, and more Pythonic web development experience. JustPy removes the front-end/back-end distinction by intercepting the relevant events on the front-end and sending them to the back-end to be processed.

!!! note
    The best way to understand JustPy is to follow the [tutorial](/tutorial/getting_started) in which there are many examples.

In JustPy, elements on the web page are instances of component classes. A component in JustPy is a Python class that allows you to instantiate reusable custom elements whose functionality and design is encapsulated away from the rest of your code.

Custom components can be created using other components as building blocks. Out of the box, JustPy comes with support for [HTML](tutorial/html_components) and [SVG](tutorial/svg_components) components as well as more complex components such as [charts](charts_tutorial/introduction.md) and [grids](grids_tutorial/introduction.md).  It also supports most of the components and the functionality of the [Quasar](https://quasar.dev/) library of [Material Design 2.0](https://material.io/) components.

JustPy encourages creating your own components and reusing them in different projects (and, if applicable, sharing these components with others).

JustPy supports visualization using [matplotlib](tutorial/matplotlib) and [Highcharts](charts_tutorial/introduction.md).

JustPy integrates nicely with [pandas](https://pandas.pydata.org/) and simplifies building web sites based on pandas analysis. JustPy comes with a [pandas extension](charts_tutorial/pandas?id=using-the-pandas-extension) that makes it simple to create interactive charts and grids from pandas data structures.

Hopefully, JustPy will enable teaching web development in introductory Python courses by reducing the complexity of web development.

## Current Version of justpy

As of {{ docdate }} the current version of justpy is {{ version }}



## If you have questions, suggestions or would like to get in touch
If you have a question about JustPy you are welcome to check
[stackoverflow questions tagged justpy](https://stackoverflow.com/questions/tagged/justpy) and
Especially questions which involve details of upstream frameworks such as
[ag-grid](https://stackoverflow.com/questions/tagged/ag-grid), [highcharts](https://www.highcharts.com/), [pandas](https://pandas.pydata.org/), [plotly](https://plotly.com/python/), [quasar](https://quasar.dev/), [tailwind](https://tailwindcss.com/) and others are best ask involving the larger [stackoverflow](https://stackoverflow.com/) community and tagging your question with both "justpy" and the tag of the specific library your are asking a question for such as "ag-grid", "highcharts","quasar", "pandas"
and others.

If you'd like to specifically address the JustPy contributors the
[github dicussions](https://github.com/justpy-org/justpy/discussions/new) are place to ask questions,
propose new features and generally get in touch with the contributors.

Our github dicussions are categorized. Please use the Category "Ideas" for feature requests.

Issues and pull requests are also welcome. Please make sure that you follow the stackoverflow style guidelines when
posting issues. A good way to do this is to state the problem as a stackoverflow question first. This way a larger audience
is able to discuss solutions and work arounds and find out which part of the technology stack you are using is actually involved
in the issue you'd like to get resolved.

If you followed the procedure you are welcome to [open an issue](https://github.com/justpy-org/justpy/issues/new/choose) in the [JustPy Github repository](https://github.com/justpy-org/justpy)

## Hello World! example
This is a simple hello world example for justpy.

```python
import justpy as jp

def hello_world_readme():
    wp = jp.WebPage()
    d = jp.Div(text='Hello world!')
    wp.add(d)
    return wp

jp.justpy(hello_world_readme)
```

The program above activates a web server that returns a web page with 'Hello world!' for any request. Locally, you would direct your browser to http://127.0.0.1:8000 or http://localhost:8000/ to see the result.

Here is a slightly modified version in which 'Hello world!' changes to 'I was clicked!' when it is clicked.

### Hello world with click

```python
import justpy as jp

def my_click(self, msg):
    self.text = 'I was clicked!'

def hello_world_readme2():
    wp = jp.WebPage()
    d = jp.Div(text='Hello world!')
    d.on('click', my_click)
    wp.add(d)
    return wp

jp.justpy(hello_world_readme2)
```


## Under the Hood

JustPy's backend is built using:

* [starlette](https://www.starlette.io/) - "a lightweight [ASGI](https://asgi.readthedocs.io/en/latest/) framework/toolkit, which is ideal for building high performance asyncio services".
* [uvicorn](https://www.uvicorn.org/) - "a lightning-fast [ASGI](https://asgi.readthedocs.io/en/latest/) server, built on [uvloop](https://github.com/MagicStack/uvloop) and [httptools](https://github.com/MagicStack/httptools)".

JustPy's frontend (which is transparent to JustPy developers) is built using:

* [Vue.js](https://vuejs.org/) - "The Progressive JavaScript Framework"

The way JustPy removes the frontend/backend distinction is by intercepting the relevant events on the frontend and sending them to the backend to be processed.

## News and Updates

For news and updates please follow the [JustPy Twitter account](https://twitter.com/justpyframework)

## License

[Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0.txt)

Copyright (c) 2019-2022 Eliezer Mintz
