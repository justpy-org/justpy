# Creating Charts

## Your First Chart
[Your First Chart live demo]({{demo_url}}/create_chart_test1)

To begin, we'll use the Highchart's documentation [Your First Chart](https://www.highcharts.com/docs/getting-started/your-first-chart) example.

In JustPy this example would look like this:
```python
import justpy as jp

# Example from https://www.highcharts.com/docs/getting-started/your-first-chart
my_chart_def = """
{
        chart: {
            type: 'bar'
        },
        title: {
            text: 'Fruit Consumption'
        },
        xAxis: {
            categories: ['Apples', 'Bananas', 'Oranges']
        },
        yAxis: {
            title: {
                text: 'Fruit eaten'
            }
        },
        series: [{
            name: 'Jane',
            data: [1, 0, 4]
        }, {
            name: 'John',
            data: [5, 7, 3]
        }]
}
"""

def create_chart_test1():
    wp = jp.WebPage()
    my_chart = jp.HighCharts(a=wp, classes="m-2 p-2 border", style="width: 600px")
    my_chart.options = my_chart_def
    return wp

jp.justpy(create_chart_test1)
```

Run the program above as explained [here](/tutorial/getting_started).

We create a chart using the JustPy HighCharts class. Like other JustPy components, it recognizes keyword arguments like `classes`, `style` and `a`.

In this example the variable `my_chart_def` defines the chart's options (settings). It is a string which can be converted directly to a valid JavaScript object. This JavaScript object is not however a valid Python dictionary because the keys of the object (for example `chart` and `title`) do not have single quotes or double quotes around them and therefore are not valid Python keys.

When `my_chart_def` is assigned to `my_chart.options` the code in `HighCharts` (a Python class) checks if a string is being assigned, and if that is the case, it is converted to a [Python dictionary that also allows dot notation](https://github.com/mewwts/addict).

If a standard Python dictionary is assigned to the `options` attribute, it is also converted to a dictionary that allows dot notation access. Don't worry if this is not completely clear at this stage. There are plenty of examples coming that will make things clearer.

Try for example, changing the text of the chart title in `my_chart_def` and running the program again.

## Chart Types
[Chart Types live demo]({{demo_url}}/create_chart_test2)

Let's do something a little more complex. Change `create_chart_test1` in the above example to the following:
```python
import justpy as jp

# Example from https://www.highcharts.com/docs/getting-started/your-first-chart
my_chart_def = """
{
        chart: {
            type: 'bar'
        },
        title: {
            text: 'Fruit Consumption'
        },
        xAxis: {
            categories: ['Apples', 'Bananas', 'Oranges']
        },
        yAxis: {
            title: {
                text: 'Fruit eaten'
            }
        },
        series: [{
            name: 'Jane',
            data: [1, 0, 4]
        }, {
            name: 'John',
            data: [5, 7, 3]
        }]
}
"""


def create_chart_test2():
    wp = jp.WebPage()
    for chart_type in ["bar", "column", "line", "spline"]:
        my_chart = jp.HighCharts(a=wp, classes="m-2 p-2 border w-1/2", options=my_chart_def)
        my_chart.options.chart.type = chart_type
        my_chart.options.title.text = f"Chart of Type {chart_type.capitalize()}"
        my_chart.options.subtitle.text = f"Subtitle {chart_type.capitalize()}"
    return wp

jp.justpy(create_chart_test2)
```

Four charts are created and put on the page, each one of a different type. We accomplish this by iterating over a list with four different chart types that Highcharts supports. When we create each chart, we load the same options (via a keyword argument) to all of them.

!!! info
    The reference for the Highcharts chart options can be found at https://api.highcharts.com/highcharts/

However, we then proceed to change the options. Using the dot notation, we assign different values to [`options.chart.type`](https://api.highcharts.com/highcharts/chart.type), [`options.title.text`](https://api.highcharts.com/highcharts/title.text) and [`options.subtitle.text`](https://api.highcharts.com/highcharts/subtitle.text).

!!! note
    Notice that `options.subtitle` was not specified in `my_chart_def`. The [addict](https://github.com/mewwts/addict) library `Dict` structure creates sub dictionaries automatically when required.


## Using Highcharts Online Examples

There are many examples of Highcharts charts online and particularly in the Highcharts [documentation](https://www.highcharts.com/docs/index). The structure of the `options` attribute of HighCharts (the Python class defined by JustPy) matches exactly the structure of the JavaScript object that defines the settings of a Highchart JavaScript chart. This is very convenient and allows you to use the numerous JavaScript examples of Highcharts charts as a starting point for your own charts.

The Highcharts library is a JavaScript library and the the chart examples are all in JavaScript. That is why JustPy's `HighCharts` supports converting strings that represent simple Javascript objects to Python dictionaries. Let's look at a concrete example from the Highcharts documentation.

Please go to https://api.highcharts.com/highcharts/chart.type and follow the link under "Try it" labeled ["Bar"](https://jsfiddle.net/gh/get/library/pure/highcharts/highcharts/tree/master/samples/highcharts/chart/type-bar/). In the Highcharts documentation and in other discussions of Highcharts it is common to link to a JavaScript [jsfiddle](https://jsfiddle.net) or [codepen](https://codepen.io) working example. In this case, a jsfiddle window opens. Look at the JavaScript window in the lower left of the page. The second argument to `Highcharts.chart` is the JavaScript object that defines the chart. Let's copy this object and assign it to a Python string and try replicating this chart.

If you simply copy the object like I did  below, you will get an error. Run the program and see for yourself there is an issue.

### highcharts example
[highcharts example live demo]({{demo_url}}/create_chart_test3)
```python
import justpy as jp

my_chart_def = """
{
    chart: {
        type: 'bar'
    },
    xAxis: {
        categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    },
    legend: {
        layout: 'vertical',
        floating: true,
        backgroundColor: '#FFFFFF',
        align: 'right',
        verticalAlign: 'top',
        y: 60,
        x: -60
    },
    tooltip: {
        formatter: function () {
            return '<b>' + this.series.name + '</b><br/>' +
                this.x + ': ' + this.y;
        }
    },
    series: [{
        data: [29.9, 71.5, 106.4, 129.2, 144.0, 176.0, 135.6, 148.5, 216.4, 194.1, 95.6, 54.4]
    }]
}
"""


def create_chart_test3():
    wp = jp.WebPage()
    my_chart = jp.HighCharts(a=wp, classes="m-2 p-2 border w-1/2", options=my_chart_def)
    return wp


jp.justpy(create_chart_test3)
```

The problem is that the value of the `tooltip.formatter` key is a JavaScript function definition. JustPy does not support this. We will soon see how to define tooltip formatters in JustPy, but for now, please remove the whole tooltip section and run the program. Your program should look like this:
### highcharts example with removed tooltip section
[highcharts example with removed tooltip live demo]({{demo_url}}/create_chart_test4)
```python
import justpy as jp

my_chart_def = """
{
    chart: {
        type: 'bar'
    },
    xAxis: {
        categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    },
    legend: {
        layout: 'vertical',
        floating: true,
        backgroundColor: '#FFFFFF',
        align: 'right',
        verticalAlign: 'top',
        y: 60,
        x: -60
    },
    series: [{
        data: [29.9, 71.5, 106.4, 129.2, 144.0, 176.0, 135.6, 148.5, 216.4, 194.1, 95.6, 54.4]
    }]
}
"""


def create_chart_test4():
    wp = jp.WebPage()
    my_chart = jp.HighCharts(a=wp, classes="m-2 p-2 border w-1/2", options=my_chart_def)
    my_chart.options.series[0].name = "'Tourists in \'000'"
    my_chart.options.title.text = "Tourists in Middle Earth"
    return wp


jp.justpy(create_chart_test4)
```

This time, there is no error. When you copy a JavaScript object, make sure that it does not include function definitions or uses JavaScript language functions to compute values. These will cause errors.

!!! warning
    JustPy can only parse JavaScript objects that look like a Python dictionary except for the missing quotes around the dictionary keys. Also, mixing single and double quotes in the JavaScript object may cause problems. Use only single quotes as is the norm with most Highcharts examples.

!!! tip
    It is very likely someone has already created a chart like that one you need and put it online. Use that chart as a stepping stone to create yours. Eventually, you may need to make use of the excellent Highcharts [docs](https://www.highcharts.com/docs/index)

## Chart Series

Notice that we have added two lines to `chart_test4` above.  The first of these lines gives the series a name and makes the legend more informative.

!!! note
    The Dicts that describe the series of a chart are held in a list so the first series is `options.series[0]`

Here is an example of how you create a chart with multiple series.

!!! warning
    numpy needs to be installed for this example to work

```python
import justpy as jp
import numpy as np


def sine_test():
    wp = jp.WebPage()
    chart = jp.HighCharts(a=wp, classes="border m-2 p-2 w-3/4")
    o = chart.options
    o.title.text = "Sines Galore"
    x = np.linspace(-np.pi, np.pi, 201)
    for frequency in range(1,11):
        y = np.sin(frequency * x)
        s = jp.Dict()
        s.name = f"F{frequency}"
        s.data = list(zip(x, y))
        o.series.append(s)
    return wp


jp.justpy(sine_test)
```

This example uses numpy to generate sines with different frequencies and adds them as separate series to a chart (numpy needs to be installed for this example to work).

This and other examples will use the Python standard library function `zip`. Using `zip`, it is very simple to create lists of x, y pairs which is one data format Highcharts supports for its series (it supports other formats also such as dictionaries).  

Try moving the mouse over different areas of the chart to see its interactive features. For example, when you hover over a series name in the legend, it highlights the series. When you click the series name in the legend, it is disabled.

## Sharing Charts

In many cases, having created a chart, you would like to share it with others. One way is to deploy JustPy and have people access the charts via a URL.

```python
import justpy as jp

# https://github.com/elimintz/elimintz.github.io/tree/master/charts
# Try https://127.0.0.1:8000/ + any one of the entries in charts
# For example: http://127.0.0.1:8000/bubbles
charts = ["org", "bubbles", "item", "timeline", "states", "browsers", "wheel"]


@jp.SetRoute("/{chart_name}")
async def create_chart_test5(request):
    wp = jp.WebPage()
    chart_name = request.path_params.get("chart_name", "item")   # Default chart is item
    if chart_name not in charts:
        chart_name = "item"
    chart_options = await jp.get(f"https://elimintz.github.io/charts/{chart_name}", "text")
    my_chart = jp.HighCharts(a=wp, classes="m-2 p-2 border w-3/4", options=chart_options)
    return wp

jp.justpy(create_chart_test5)
```

The program above fetches chart definitions from a static page server (a github repository in this case) based on the URL. Take a look at the different charts for a small taste of what Highcharts can do (these are all taken from the Highcharts website where there are many more examples). You could deploy the program above and have others accessing the charts via the appropriate URLs.
The chart definitions can be found [here](https://github.com/elimintz/elimintz.github.io/tree/master/charts).

Another option is to send people the code snippet above to run by themselves. Of course, they would need to have the appropriate environment installed on their computer.

The advantage of reading the chart definition remotely is that you can change these remote files and additional files without needing to resend or restart your program.
