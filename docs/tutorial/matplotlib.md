# Creating matplotlib Charts

The most popular Python plotting library is [matplotlib](https://matplotlib.org/index.html). Chances are that if you are interested in visualization, you have already used it.

JustPy includes in its standard component library the component Matplotlib that makes it simple to include matplotlib charts in a web page without having to change any matplotlib command.

## The Matplotlib component

Run the following example that uses the Matplotlib component:

### matplotlib.pyplot example
```python
import justpy as jp
import matplotlib.pyplot as plt

def plot_test1():
    wp = jp.WebPage()
    plt.plot([0, 1, 4, 9], marker='*', markersize=20, markeredgecolor='red')
    plt.title('Matplotlib Example')
    plt.xlabel('x data')
    plt.ylabel('y data')
    jp.Matplotlib(a=wp)

    # If memory may be an issue, don't forget to close figures not in use anymore
    plt.close()
    return wp

jp.justpy(plot_test1)
```

The line `jp.Matplotlib(a=wp)` creates a Matplotlib instance and adds it to `wp`.

!!! tip
    If you call Matplotlib where you would normally call `plt.show()` the chart instance is created reflecting all the matplotlib commands issued so far.

The Matplotlib component is a modified Div component whose `inner_html` attribute is set to the SVG representation of a [matplotlib figure](https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.figure.Figure.html).

If a matplotlib figure is not specified explicitly when a Matplotlib instance is created (like in the example above), Matplotlib uses the current figure. If you want to put some other figure on the page use the `figure` keyword when creating the instance or use the `set_figure(figure)` method of the component after creation.

!!! tip
    Don't forget to close matplotlib figures that are not in use. This will not affect any JustPy Matplotlib instances as the SVG representation that was created from the figure is distinct from the figure and will not be deleted.

In the example below, the first chart created is displayed second and the second chart created is displayed first.
### matplotlib.pyplot example with display order
```python
import justpy as jp
import matplotlib.pyplot as plt

def plot_test2():
    wp = jp.WebPage()

    first_figure = plt.figure()
    plt.plot([0, 1, 4, 9], marker='*', markersize=20, markeredgecolor='red')
    plt.title('First Figure Showing Second')
    plt.xlabel('x data')
    plt.ylabel('y data')

    second_figure = plt.figure()
    plt.plot([0, 1, 4, 9], marker='+', markersize=20, markeredgecolor='red')
    plt.title('Second Figure Showing First')
    plt.xlabel('x data')
    plt.ylabel('y data')

    # Keyword method of setting figure
    jp.Matplotlib(figure=second_figure, a=wp)
    # Using method after creation
    c = jp.Matplotlib(a=wp)
    c.set_figure(first_figure)

    # If memory may be an issue, don't forget to close figures not in use anymore
    plt.close(first_figure)
    plt.close(second_figure)
    return wp

jp.justpy(plot_test2)
```

## Updating charts following events

In the example below, each time the button is clicked, another point is added to the chart. This is done by creating a new figure in the event handler and setting the figure of the component to this new figure. In effect, the `inner_html` attribute of the element is set to the SVG of the new figure.

### matplotlib chart update using inner_html of SVG figure
```python
import justpy as jp
import matplotlib.pyplot as plt


def plot_test3():
    wp = jp.WebPage()

    f = plt.figure()
    plt.plot([0, 1, 4, 9], marker='*', markersize=20, markeredgecolor='red')
    plt.title('Matplotlib Example')
    plt.xlabel('x data')
    plt.ylabel('y data')
    chart = jp.Matplotlib(a=wp)
    chart.num_points = 4
    plt.close(f)

    b = jp.Button(text='Add Point', a=wp,
                  classes='m-2 bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded')
    b.chart = chart

    def add_point(self, msg):
        self.chart.num_points += 1
        np = self.chart.num_points
        f = plt.figure()
        plt.plot([i*i for i in range(np)], marker='*', markersize=20, markeredgecolor='red')
        plt.title(f'This chart has {np} points')
        plt.xlabel('x data')
        plt.ylabel('y data')
        self.chart.set_figure(f)
        plt.close(f)

    b.on('click', add_point)

    return wp


jp.justpy(plot_test3)
```

The chart component itself is a JustPy component so it responds also to events. In the example below, clicking the button adds a point to the chart while clicking the chart subtracts a point.
### matplotlib chart adding a point on an event
```python
import justpy as jp
import matplotlib.pyplot as plt


def plot_test4():
    wp = jp.WebPage()
    print(f'start {plt.get_fignums()}')
    f = plt.figure()
    plt.plot([0, 1, 4, 9], marker='*', markersize=20, markeredgecolor='red')
    plt.title('Matplotlib Example')
    plt.xlabel('x data')
    plt.ylabel('y data')
    chart = jp.Matplotlib(a=wp)
    chart.num_points = 4
    plt.close(f)

    b = jp.Button(text='Add Point', a=wp,
                  classes='m-2 bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded')
    b.chart = chart

    def add_point(self, msg):
        self.chart.num_points += 1
        np = self.chart.num_points
        f = plt.figure()
        plt.plot([i*i for i in range(np)], marker='*', markersize=20, markeredgecolor='red')
        plt.title(f'This chart has {np} points')
        plt.xlabel('x data')
        plt.ylabel('y data')
        self.chart.set_figure(f)
        plt.close(f)

    b.on('click', add_point)

    def subtract_point(self, msg):
        self.num_points -= 1
        np = self.num_points
        f = plt.figure()
        plt.plot([i*i for i in range(np)], marker='*', markersize=20, markeredgecolor='red')
        plt.title(f'This chart has {np} points')
        plt.xlabel('x data')
        plt.ylabel('y data')
        self.set_figure(f)
        plt.close(f)

    chart.on('click', subtract_point)

    return wp


jp.justpy(plot_test4)
```

## Multiple charts on a page

The program below is very similar to the example above except that it puts the same chart element several times on the page. Since it is the same element, the event handlers modify all the charts.

### matplotlib chart with several copies on same page
```python
import justpy as jp
import matplotlib.pyplot as plt


def plot_test5():
    wp = jp.WebPage()
    print(f'start {plt.get_fignums()}')
    f = plt.figure(figsize=(2, 2))
    plt.plot([0, 1, 4, 9], marker='*', markersize=20, markeredgecolor='red')
    plt.title('Matplotlib Example')
    plt.xlabel('x data')
    plt.ylabel('y data')
    d = jp.Div(classes='flex flex-wrap', a=wp)
    chart = jp.Matplotlib(classes='m-1 p-2')
    for i in range(5):
        d.add(chart)

    chart.num_points = 4
    plt.close(f)

    b = jp.Button(text='Add Point', a=wp,
                  classes='m-2 bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded')
    b.chart = chart

    def add_point(self, msg):
        self.chart.num_points += 1
        np = self.chart.num_points
        f = plt.figure(figsize=(2, 2))
        plt.plot([i*i for i in range(np)], marker='*', markersize=20, markeredgecolor='red')
        plt.title(f'This chart has {np} points')
        plt.xlabel('x data')
        plt.ylabel('y data')
        self.chart.set_figure(f)
        plt.close(f)

    b.on('click', add_point)

    def subtract_point(self, msg):
        self.num_points -= 1
        np = self.num_points
        f = plt.figure(figsize=(2, 2))
        plt.plot([i*i for i in range(np)], marker='*', markersize=20, markeredgecolor='red')
        plt.title(f'This chart has {np} points')
        plt.xlabel('x data')
        plt.ylabel('y data')
        self.set_figure(f)
        plt.close(f)

    chart.on('click', subtract_point)

    return wp

jp.justpy(plot_test5)
```

If we want to treat each chart separately in the event handlers we need to modify the program. In the program below clicking the button adds a point to all charts while clicking each chart subtracts a point only from the chart clicked.

### matplotlib chart with event treatment per chart

```python
import justpy as jp
import matplotlib.pyplot as plt


def add_point(self, msg):
    for chart in self.chart_list:
        chart.num_points += 1
        np = chart.num_points
        f = plt.figure(figsize=(2, 2))
        plt.plot([i * i for i in range(np)], marker='*', markersize=20, markeredgecolor='red')
        plt.title(f'This chart has {np} points')
        plt.xlabel('x data')
        plt.ylabel('y data')
        chart.set_figure(f)
        plt.close(f)

def subtract_point(self, msg):
    self.num_points -= 1
    np = self.num_points
    f = plt.figure(figsize=(2, 2))
    plt.plot([i*i for i in range(np)], marker='*', markersize=20, markeredgecolor='red')
    plt.title(f'This chart has {np} points')
    plt.xlabel('x data')
    plt.ylabel('y data')
    self.set_figure(f)
    plt.close(f)

def plot_test6():
    wp = jp.WebPage()
    f = plt.figure(figsize=(2, 2))
    plt.plot([0, 1, 4, 9], marker='*', markersize=20, markeredgecolor='red')
    plt.title('Matplotlib Example')
    plt.xlabel('x data')
    plt.ylabel('y data')
    d = jp.Div(classes='flex flex-wrap', a=wp)
    chart_list = []
    for i in range(5):
        chart = jp.Matplotlib(a=d, classes='m-1 p-2')
        chart.num_points = 4
        chart_list.append(chart)
        chart.on('click', subtract_point)

    plt.close(f)

    b = jp.Button(text='Add Point', a=wp,
                  classes='m-2 bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded')
    b.chart_list = chart_list
    b.on('click', add_point)

    return wp


jp.justpy(plot_test6)
```

In order to handle each chart separately, we create 5 distinct chart elements and assign to the button the list of the chart elements we created and then iterate over the charts in the button's click event handler.


## Creating matplotlib charts with pandas

Pandas provides a [visualization layer](https://pandas.pydata.org/pandas-docs/stable/user_guide/visualization.html) over matplotlib.

Since pandas creates matplotlib plots, the Matplotlib component works in this case as well. Simply call Matplotlib when in your code you would normally call `plt.show()`.

!!! tip
    If you create matplotlib charts within request handlers, don't forget to close the matplotlib figures associated with them in order to conserve memory and make your application scalable.

!!! note
    The example below takes about 15 seconds to load a request, it is not hanging
### pandas load to matplotlib.plot
```python
import justpy as jp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# All examples from https://pandas.pydata.org/pandas-docs/stable/user_guide/visualization.html

def plot_test7():
    wp = jp.WebPage()

    jp.Div(text='Series Plot', a=wp, classes='text-white bg-blue-500 text-center text-xl')
    ts = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))
    ts = ts.cumsum()
    ts.plot()
    jp.Matplotlib(a=wp)
    plt.close()

    jp.Div(text='Frame Plot', a=wp, classes='text-white bg-blue-500 text-center text-xl')
    df = pd.DataFrame(np.random.randn(1000, 4), index=ts.index, columns=list('ABCD'))
    df = df.cumsum()
    df.plot()
    jp.Matplotlib(a=wp)
    plt.close()

    jp.Div(text='Histogram', a=wp, classes='text-white bg-blue-500 text-center text-xl')
    df4 = pd.DataFrame({'a': np.random.randn(1000) + 1, 'b': np.random.randn(1000), 'c': np.random.randn(1000) - 1}, columns=['a', 'b', 'c'])
    df4.plot.hist(alpha=0.5)
    jp.Matplotlib(a=wp)
    plt.close()

    jp.Div(text='Multiple Subplots', a=wp, classes='text-white bg-blue-500 text-center text-xl')
    df.diff().hist(color='k', alpha=0.5, bins=50)
    jp.Matplotlib(a=wp)
    plt.close()

    jp.Div(text='Multiple Pie Charts', a=wp, classes='text-white bg-blue-500 text-center text-xl')
    df_pie = pd.DataFrame(3 * np.random.rand(4, 2),index=['a', 'b', 'c', 'd'], columns=['x', 'y'])
    df_pie.plot.pie(subplots=True, figsize=(8, 4))
    jp.Matplotlib(a=wp)
    plt.close()

    # The following example takes some time (about 15 seconds) to generate, so the page loads slowly
    jp.Div(text='Plotting Tools, Scatter Matrix', a=wp, classes='text-white bg-blue-500 text-center text-xl')
    df_scatter = pd.DataFrame(np.random.randn(1000, 4), columns=['a', 'b', 'c', 'd'])
    pd.plotting.scatter_matrix(df_scatter, alpha=0.2, figsize=(10, 10), diagonal='kde')
    jp.Matplotlib(a=wp)
    plt.close()

    return wp

jp.justpy(plot_test7)
```

If you don't need to customize the chart for each request, you can speed up your website's response time by generating the charts once and serving the same chart elements with each request.

Here is the program above modified in this fashion:
### pandas load to matplotlib.plot with preloading
```python
import justpy as jp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# All examples from https://pandas.pydata.org/pandas-docs/stable/user_guide/visualization.html

def create_page():
    wp = jp.WebPage(delete_flag=False)

    jp.Div(text='Series Plot', a=wp, classes='text-white bg-blue-500 text-center text-xl')
    ts = pd.Series(np.random.randn(1000), index=pd.date_range('1/1/2000', periods=1000))
    ts = ts.cumsum()
    ts.plot()
    jp.Matplotlib(a=wp)
    plt.close()

    jp.Div(text='Frame Plot', a=wp, classes='text-white bg-blue-500 text-center text-xl')
    df = pd.DataFrame(np.random.randn(1000, 4), index=ts.index, columns=list('ABCD'))
    df = df.cumsum()
    df.plot()
    jp.Matplotlib(a=wp)
    plt.close()

    jp.Div(text='Histogram', a=wp, classes='text-white bg-blue-500 text-center text-xl')
    df4 = pd.DataFrame({'a': np.random.randn(1000) + 1, 'b': np.random.randn(1000), 'c': np.random.randn(1000) - 1}, columns=['a', 'b', 'c'])
    df4.plot.hist(alpha=0.5)
    jp.Matplotlib(a=wp)
    plt.close()

    jp.Div(text='Multiple Subplots', a=wp, classes='text-white bg-blue-500 text-center text-xl')
    df.diff().hist(color='k', alpha=0.5, bins=50)
    jp.Matplotlib(a=wp)
    plt.close()

    jp.Div(text='Multiple Pie Charts', a=wp, classes='text-white bg-blue-500 text-center text-xl')
    df_pie = pd.DataFrame(3 * np.random.rand(4, 2),index=['a', 'b', 'c', 'd'], columns=['x', 'y'])
    df_pie.plot.pie(subplots=True, figsize=(8, 4))
    jp.Matplotlib(a=wp)
    plt.close()

    # The following example takes some time (about 10 seconds) to generate.
    jp.Div(text='Plotting Tools, Scatter Matrix', a=wp, classes='text-white bg-blue-500 text-center text-xl')
    df_scatter = pd.DataFrame(np.random.randn(1000, 4), columns=['a', 'b', 'c', 'd'])
    pd.plotting.scatter_matrix(df_scatter, alpha=0.2, figsize=(10, 10), diagonal='kde')
    jp.Matplotlib(a=wp)
    plt.close()

    return wp

wp = create_page()

def plot_test8():
    return wp

jp.justpy(plot_test8)
```

## Creating charts with seaborn

> [Seaborn](https://seaborn.pydata.org/index.html) is a Python data visualization library based on matplotlib. It provides a high-level interface for drawing attractive and informative statistical graphics.

Seaborn allows you to create beautiful visualizations with few lines of code.

Again, since seaborn, like pandas' visualization, is based on matplotlib, Matplotlib (the JustPy component) works well also with seaborn.

Following are a few examples taken from the [seaborn introduction](https://seaborn.pydata.org/introduction.html):
### seaborn example
```python
import justpy as jp
import seaborn as sns

# All examples from https://seaborn.pydata.org/introduction.html

def create_page():
    wp = jp.WebPage(delete_flag=False)
    chart_classes = 'm-2'

    jp.Div(text='Tips Dataset', a=wp, classes='text-white bg-blue-500 text-center text-xl')
    sns.set()
    tips = sns.load_dataset("tips")
    sns.relplot(x="total_bill", y="tip", col="time",
                hue="smoker", style="smoker", size="size",
                data=tips)
    jp.Matplotlib(a=wp, classes=chart_classes)
    sns.lmplot(x="total_bill", y="tip", col="time", hue="smoker",
               data=tips)
    jp.Matplotlib(a=wp, classes=chart_classes)
    sns.catplot(x="day", y="total_bill", hue="smoker",
                kind="swarm", data=tips)
    jp.Matplotlib(a=wp, classes=chart_classes)
    sns.catplot(x="day", y="total_bill", hue="smoker",
                kind="violin", split=True, data=tips)
    jp.Matplotlib(a=wp, classes=chart_classes)

    jp.Div(text='Dots Dataset', a=wp, classes='text-white bg-blue-500 text-center text-xl')
    dots = sns.load_dataset("dots")
    sns.relplot(x="time", y="firing_rate", col="align",
                hue="choice", size="coherence", style="choice",
                facet_kws=dict(sharex=False),
                kind="line", legend="full", data=dots)
    jp.Matplotlib(a=wp, classes=chart_classes)

    jp.Div(text='FMRI Dataset', a=wp, classes='text-white bg-blue-500 text-center text-xl')
    fmri = sns.load_dataset("fmri")
    sns.relplot(x="timepoint", y="signal", col="region",
                hue="event", style="event",
                kind="line", data=fmri)
    jp.Matplotlib(a=wp, classes=chart_classes)

    jp.Div(text='Iris Dataset', a=wp, classes='text-white bg-blue-500 text-center text-xl')
    iris = sns.load_dataset("iris")
    sns.jointplot(x="sepal_length", y="petal_length", data=iris)
    jp.Matplotlib(a=wp, classes=chart_classes)
    sns.pairplot(data=iris, hue="species")
    jp.Matplotlib(a=wp, classes=chart_classes)

    return wp


wp = create_page()

def plot_test9():
    return wp

jp.justpy(plot_test9)
```
