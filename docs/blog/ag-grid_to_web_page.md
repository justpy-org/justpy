# From a Pandas DataFrame to a Web Site with an ag-Grid in 10 Lines of Python

[dev.to link](https://dev.to/elimintz/from-a-pandas-dataframe-to-a-web-site-with-an-ag-grid-in-10-lines-of-python-2a9b)

## Introduction

[Pandas](https://pandas.pydata.org/) is "a fast, powerful, flexible and easy to use open source data analysis and manipulation tool, built on top of the Python programming language". It is used by millions of programmer.

[ag-Grid](https://www.ag-grid.com/) bills itself as "The Best JavaScript Grid in the World" and its extensive list of features as well as its speed make arguing against this assertion difficult.

[JustPy](https://justpy.io) is a Python package that allows you to build web applications without any JavaScript programming (I am the creator of JustPy). JustPy comes with a [Pandas extension](https://pandas.pydata.org/pandas-docs/stable/development/extending.html) that makes it very easy to insert the data from a DataFrame into an ag-Grid and into a web application.

## Basic Example
[Basic Example live demo]({{demo_url}}/basic_example)

The following program reads a a CSV file into a DataFrame and creates a web application that serves a web page with the ag-Grid. The [data](http://www.randalolson.com/2014/06/14/percentage-of-bachelors-degrees-conferred-to-women-by-major-1970-2012/) describes the percentage of bachelor's degrees conferred to women by major in the years 1970-2012.

```python
import justpy as jp
import pandas as pd

# Load data showing percent of women in different majors per year
wm = pd.read_csv('https://elimintz.github.io/women_majors.csv').round(2)

def basic_example():
    """
    basic AG Grid example reading a csv file and displaying it in a grid
    """
    wp = jp.WebPage()
    wm.jp.ag_grid(a=wp)  # a=wp adds the grid to WebPage wp
    return wp

jp.justpy(basic_example)

```

That is it. That is the whole program.

To run this program you need to have Python version 3.6 or higher and you need to install the pandas and justpy packages. Then, you would create a file with your favorite text editor and copy and paste the program above. If you called the file `grid.py` you would type `python3 grid.py` in the command line or you could use an IDE. By default, you would access the web page by pointing your browser to http://127.0.0.1:8000 (it is easy to change the IP address and port that the application uses if you wish)

For a more detailed explanation on how to get started using JustPy please see [Getting Started](https://justpy.io/#/tutorial/getting_started) from the tutorial.

Once the page loads, move the mouse to any of the column headers to try the interactive features of the grid.

## Several Grids on a Page
[Several Grids on a Page]({{demo_url}}/several_grids_onapage)
You can put as many ag-Grids on the page as you like. Below, we create another DataFrame only with the majors in which women started at less than 20% and put the original DataFrame and the new DataFrame on the page. Scroll down the browser tab to see the second grid.

```python
import justpy as jp
import pandas as pd

wm = pd.read_csv('https://elimintz.github.io/women_majors.csv').round(2)
wm_under_20 = wm[wm.loc[0, wm.loc[0] < 20].index]
wm_under_20.insert(0, 'Year', wm['Year'])

def several_grids_onapage():
    """
    show several grids on a page
    """
    wp = jp.WebPage()
    wm.jp.ag_grid(a=wp)
    wm_under_20.jp.ag_grid(a=wp)
    return wp

jp.justpy(several_grids_onapage)

```

## Customizing Grids

You can also specify further options for the ag-Grid after its creation. The Python class of JustPy that models the ag-Grid has an `options` attribute that is identical in structure to the JavaScript one. When it is modified, the grid on the page will reflect these changes.

In the program below we change the options so that:
 1) The grid is paginated
 2) The grid page size is automatically determined based on the browser tab size
 3) The 'Year' column is formatted with CSS classes (JustPy comes with [Tailwind CSS](https://tailwindcss.com/) classes out of th box)
 4) Each data cell is conditionally formatted based on its value


```python
import justpy as jp
import pandas as pd

wm_df = pd.read_csv('https://elimintz.github.io/women_majors.csv').round(2)

def grid_test3():
    wp = jp.WebPage()
    grid = wm_df.jp.ag_grid(a=wp)
    grid.options.pagination = True
    grid.options.paginationAutoPageSize = True
    grid.options.columnDefs[0].cellClass = ['text-white', 'bg-blue-500', 'hover:bg-blue-200']
    for col_def in grid.options.columnDefs[1:]:
        col_def.cellClassRules = {
            'font-bold': 'x < 20',
            'bg-red-300': 'x < 20',
            'bg-yellow-300': 'x >= 20 && x < 50',
            'bg-green-300': 'x >= 50'
        }
    return wp

jp.justpy(grid_test3)

```

## Routes and Multiple Pages

With JustPy it is simple to serve grids with different data based on the URL.

In the example below the URL http://127.0.0.1/wm will serve the full grid while the URL http://127.0.0.1/wm_20 will serve a grid only with the majors in which women started under 20%.


```python
import justpy as jp
import pandas as pd

wm = pd.read_csv('https://elimintz.github.io/women_majors.csv').round(2)
wm_under_20 = wm[wm.loc[0, wm.loc[0] < 20].index]
wm_under_20.insert(0, 'Year', wm['Year'])

# Tailwind classes to format header div
title_classes = 'text-2xl text-white bg-blue-500 text-center mb-2 p-2'

# Change grid default style to change height
grid_style = 'height: 85vh; width: 99%; margin: 0.25rem; padding: 0.25rem;'

@jp.SetRoute('/wm')
def serve_wm1():
    wp = jp.WebPage()
    jp.Div(text='All Majors', classes=title_classes, a=wp)
    wm.jp.ag_grid(a=wp, style=grid_style)
    return wp

@jp.SetRoute('/wm_20')
def serve_wm2():
    wp = jp.WebPage()
    jp.Div(text='Only Majors with Women Starting Under 20%', classes=title_classes, a=wp)
    wm_under_20.jp.ag_grid(a=wp, style=grid_style)
    return wp

jp.justpy()#women_majors_route_example
```

## ag-Grid Enterprise

By default, JustPy uses the ag-Grid community version which is a free to use product distributed under the MIT License. If you would like to try the enterprise version, create a file called `justpy.env` in the directory where your program file and include in it the following:

```python
AGGRID = False
AGGRID_ENTERPRISE = True
```

## Learn More

In future articles, I will show how to interact with grid events as well as how to create interactive charts that are linked to the gird data.

If you would like to learn more how you can move your pandas data quickly onto a web page without any JavaScript programming, please go to the [JustPy Docs and Tutorials](https://justpy.io/) and feel free to ask me any questions either in the comments below or on [GitHub](https://github.com/elimintz/justpy).
