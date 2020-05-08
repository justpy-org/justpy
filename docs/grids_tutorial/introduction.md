# ag-Grid Introduction

JustPy comes with a grid component based on [ag-Grid Community](https://www.ag-grid.com/) which is a [free](https://www.ag-grid.com/license-pricing.php) to use product distributed under the MIT License. The features provided in the Community version of ag-Grid are comprehensive and its API and documentation are clear and easy to work with. 

!!! note
    It took about 100 lines of Python and about 100 lines of JavasScript to add ag-Grid as a component to JustPy. If you are interested in integrating other grid or JavaScript components with JustPy, please take a look at the code and contact me.
 
An ag-Grid grid is represented in JustPy as an instance of the class AgGrid. The grid is defined by the `options` attribute which is a Python dictionary that corresponds to the JavaScript object that defines the grid in JavaScript. The correspondence is one to one. As in the case with chart options, the grid options can be loaded from a string representing a JavaScript object (with the usual caveats).

The AgGrid component comes with some default settings that can be changed. One of these setting is the `style` attribute which gives some width and height to the grid. 

!!! warning
    If you change the style, make sure to specify height and width. Without these, the grid will not be displayed.

The simplest way to load data to the grid is from a pandas frame. We will cover some examples of this below.
