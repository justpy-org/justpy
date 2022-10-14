# Using Pandas to Create Charts

If you work with [pandas](https://pandas.pydata.org/) or plan to do so, using JustPy and Highcharts is an option for visualization or building interactive charts and dashboards.

## Using the Pandas Extension

JustPy comes with a [pandas extension](https://pandas.pydata.org/pandas-docs/stable/development/extending.html) called `jp` that makes it simple to create charts from [pandas frames](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html).

The program below loads a [csv](https://elimintz.github.io/women_majors.csv) file into a pandas frame and then creates a chart based on the data in the frame.

!!! note
    The examples in this section were inspired by [this](https://www.dataquest.io/blog/making-538-plots/) blog post. Many thanks to [Randal Olson](http://www.randalolson.com/2014/06/14/percentage-of-bachelors-degrees-conferred-to-women-by-major-1970-2012/) for creating and hosting the data set.

!!! warning
    To run the program below you will need to have pandas installed.

```python
import justpy as jp
import pandas as pd


wm = pd.read_csv('https://elimintz.github.io/women_majors.csv').round(2)
# Create list of majors which start under 20% women students
wm_under_20 = list(wm.loc[0, wm.loc[0] < 20].index)

def women_majors1():
    wp = jp.WebPage()
    wm.jp.plot(0, 
      	wm_under_20, 
      	kind='spline', 
     	a=wp, 
      	title='The gender gap is transitory - even for extreme cases',
      	subtitle='Percentage of Bachelors conferred to women form 1970 to 2011 in the US for extreme cases where the percentage was less than 20% in 1970',
      	classes='m-2 p-2 w-3/4')
    return wp

jp.justpy(women_majors1)
```

The JustPy pandas extension `jp` includes the function `plot` that creates and returns a chart instance.

It has two positional arguments:

- The frame column to use as the x value, can either be the index of the column or its name
- A list of the columns to plot as y values. Items on the list can either be column indexes or names

The `plot` function also accepts several keyword arguments:
- `kind`: &nbsp;&nbsp;&nbsp; String describing the type of the chart, default is "column"
- `title`:  &nbsp;&nbsp;&nbsp; The title of the chart, default is the empty string
- `subtitle`:  &nbsp;&nbsp;&nbsp; The subtitle of the chart, default is the empty string
- `categories`: &nbsp;&nbsp;&nbsp;  Boolean indicating whether to treat x values as categories or numbers, default is `True`
- `stacking`:  &nbsp;&nbsp;&nbsp; One of  "",  "normal",  "percent". The default is "" (the empty string) meaning no stacking of series
- All the other keyword arguments HighCharts accepts

## Customizing the Chart

Sometimes you will need to customise the result you get from `plot`. As it returns a HighCharts instance this is simple to do.

The program below puts two charts on the page. The first is the result of running `plot` without any customization and the second is the customized chart.

```python
import justpy as jp
import pandas as pd


wm = pd.read_csv('https://elimintz.github.io/women_majors.csv').round(2)
wm_under_20 = list(
  wm.loc[0, wm.loc[0] < 20].index
) # Create list of majors which start under 20%

def women_majors2():
    wp = jp.WebPage()

    # First chart
    wm.jp.plot(0, wm_under_20, kind='spline', a=wp, title='The gender gap is transitory - even for extreme cases',
                subtitle='Percentage of Bachelors conferred to women form 1970 to 2011 in the US for extreme cases where the percentage was less than 20% in 1970',
                classes='m-2 p-2 w-3/4')

    # Second Chart
    wm_chart = wm.jp.plot(0, wm_under_20, kind='spline', a=wp, categories=False,
                          title='The gender gap is transitory - even for extreme cases',
                          subtitle='Percentage of Bachelors conferred to women form 1970 to 2011 in the US for extreme cases where the percentage was less than 20% in 1970',
                          classes='m-2 p-2 w-3/4 border', style='height: 700px')
    o = wm_chart.options
    o.title.align = 'left'
    o.title.style.fontSize = '24px'
    o.subtitle.align = 'left'
    o.subtitle.style.fontSize = '20px'
    o.xAxis.title.text = 'Year'
    o.xAxis.gridLineWidth = 1
    o.yAxis.title.text = '% Women in Major'
    o.yAxis.labels.format = '{value}%'
    o.legend.layout = 'proximate'
    o.legend.align = 'right'
    o.plotOptions.series.marker.enabled = False
    return wp

jp.justpy(women_majors2)
```

Since `plot` returns a HighChart instance, we just modify its options to customize it. We also set `categories` to `False` in the second chart so that not all the years are displayed on the x axis.

## Modifying a Series

By default, all series on the chart created by `plot` are of the same kind. We can modify this after the chart is created.
For example add the following line at the end of `women_majors` (just before `return wp` ) amd re-run:
```python
o.series[3].type = 'column'
```

## Using Pandas without the Extension

For completeness, below is how you would get the same result without using the extension. This method provides more control but requires more code.

```python
import justpy as jp
import pandas as pd
import itertools


wm = pd.read_csv('https://elimintz.github.io/women_majors.csv').round(2)
wm_under_20 = list(
  wm.loc[0, wm.loc[0] < 20].index
) # Create list of majors which start under 20%


def make_pairs_list(x_data, y_data):
    return list(map(list, itertools.zip_longest(x_data, y_data)))


def women_majors3():
    wp = jp.WebPage(highcharts_theme='grid')
    wm_chart = jp.HighCharts(a=wp, classes='m-2 p-2 w-3/4')
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

jp.justpy(women_majors3)
```


The form of a series' data in JustPy mirrors that of the [series](https://www.highcharts.com/docs/chart-concepts/series) in Highcharts , with JavaScript arrays corresponding to Python lists and JavaScript objects corresponding to Python dictionaries.

In our specific case, the data of each series is a list of lists of pairs, each pair representing the x and y of each point respectively. It is simple to create such lists in Python using the `zip` and `list` functions.

In this example, we used the itertools library function `zip_longest` to make sure missing values are handled correctly. Since the zip family of functions returns tuples, we need to convert them to lists (this is not strictly true since the standard library `json.dumps` function converts python tuples to JavaScript arrays). All this is done in the function `make_pairs_list` above.

!!! info
    JustPy comes with several Highcharts themes. The theme of all charts on a page must be the same and therefore `highcharts_theme` is a WebPage attribute. In this example we set the theme to 'grid'.
