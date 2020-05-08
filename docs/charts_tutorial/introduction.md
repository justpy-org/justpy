# Highcharts Introduction

!!! note
    It is recommended to go through the general [tutorial](/tutorial/getting_started) first. 

JustPy makes it simple to create charts using the [Highcharts](https://www.highcharts.com/) JavaScript charting library.

!!! info
    JustPy also supports [matplotlib charts](/tutorial/matplotlib)

There are several JavaScript charting libraries available, but my personal favorite is Highcharts. It is not too difficult to integrate other charting libraries with JustPy, so perhaps more charting libraries will be supported in the future.

The Highcharts and JustPy combination is great for creating and sharing interactive charts, even if you don't plan to develop a web application. JustPy allows you to share your visualizations by providing access to the charts through any browser.
 
Highcharts is [free](https://shop.highsoft.com/faq#Non-Commercial-0) for non-commercial use and this includes individuals using the software for personal use, testing and demonstration.

A Highcharts chart in JustPy is a component. It is represented by a Python class, just like any other component. Because Highcharts is a JavaScript library it uses a JavaScript object to define the options or settings of a chart. 

In JustPy however, charts are defined using a dictionary that allows values to be set using the dot notation. To facilitate using chart examples written in JavaScript, the chart options in JustPy can also be a Python string representing a subset of JavaScript objects. This will become clearer when we look at some examples.
