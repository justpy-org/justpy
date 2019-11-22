# Using Pandas to Create Charts

Using Highcharts and JustPy it is simple to visualize data residing in [pandas](https://pandas.pydata.org/) frames. The program below loads a csv file into a pandas frame and then creates a chart based on the data in the frame. This example was inspired by [this](https://www.dataquest.io/blog/making-538-plots/) blog post.  
 
 Many thanks to [Randal Olson](http://www.randalolson.com/2014/06/14/percentage-of-bachelors-degrees-conferred-to-women-by-major-1970-2012/) for creating and hosting the data set.

!> To run the program below you will need to have pandas installed.
```python
import justpy as jp
import pandas as pd
import itertools

# https://www.dataquest.io/blog/making-538-plots/
# http://www.randalolson.com/2014/06/14/percentage-of-bachelors-degrees-conferred-to-women-by-major-1970-2012/

wm = pd.read_csv('https://elimintz.github.io/women_majors.csv').round(2)
wm_under_20 = list(wm.loc[0, wm.loc[0] < 20].index) # Create list of majors which start under 20%


def make_pairs_list(x_data, y_data):
    return list(map(list, itertools.zip_longest(x_data, y_data)))


def women_majors():
    wp = jp.WebPage(highcharts_theme='grid')
    wm_chart = jp.HighCharts(a=wp, classes='m-2 p-2 border w-3/4')
    o = wm_chart.options  # Will save us some typing and make code cleaner
    o.title.text = 'The gender gap is transitory - even for extreme cases'
    o.title.align = 'left'
    o.xAxis.title.text = 'Year'
    o.xAxis.gridLineWidth = 1
    o.yAxis.title.text = '% Women in Major'
    o.yAxis.labels.format = '{value}%'
    o.legend.layout = 'proximate'
    o.legend.align = 'right'
    o.series = []
    x_data = wm.iloc[:, 0].tolist()
    for major in wm_under_20:
        s = jp.Dict()
        y_data = wm[major].tolist()
        s.data = make_pairs_list(x_data, y_data)
        s.name = major
        s.type = 'spline'
        o.series.append(s)
        s.marker.enabled = False
    return wp

jp.justpy(women_majors)
```

If you work with Pandas or plan to do so, using JustPy and Highcharts is an option for visualization or building interactive charts or dashboards. 

The form of a series' data in JustPy mirrors that of the [series](https://www.highcharts.com/docs/chart-concepts/series) in Highcharts , with JavaScript arrays corresponding to Python lists and JavaScript objects corresponding to Python dictionaries. 

In our specific case, the data of each series is a list of lists of pairs, each pair representing the x and y of each point respectively. It is simple to create such lists in Python using the `zip` and `list` functions. 

In this example, we used the itertools library function `zip_longes`t to make sure missing values are handled correctly. Since the zip family of functions returns tuples, we need to convert them to lists (this is not strictly true since the standard library `json.dumps` function converts python tuples to JavaScript arrays). All this is done in the function `make_pairs_list` above.

JustPy comes with several Highcharts themes. The theme of all charts on a page must be the same and therefore `highcharts_theme` is a WebPage attribute. In this example we set the theme to 'grid'.
