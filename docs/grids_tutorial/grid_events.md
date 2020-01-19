# Grid Events

## Example 1

Ag-Grid supports many [events](https://www.ag-grid.com/javascript-grid-events/). Let's look at some examples.

To begin, let's display in a separate Div the data from a grid row when it is selected.

```python
import justpy as jp
import pandas as pd

wm_df = pd.read_csv('https://elimintz.github.io/women_majors.csv').round(2)

def row_selected(self, msg):
    print(msg)
    if msg.selected:
        self.row_data_div.text = msg.data
        self.row_selected = msg.rowIndex
    elif self.row_selected == msg.rowIndex:
        self.row_data_div.text = ''

def grid_test():
    wp = jp.WebPage()
    row_data_div = jp.Div(a=wp)
    grid = wm_df.jp.ag_grid(a=wp)
    grid.row_data_div = row_data_div
    grid.on('rowSelected', row_selected)
    grid.options.columnDefs[0].checkboxSelection = True
    return wp

jp.justpy(grid_test)
```

We add a Div named `row_data_div` to the page and the `row_selected` function, the event handler for the grid's rowSelected event, sets the row data as the text of the Div. 

JustPy provides in `msg.data` all the data from the row in a form of a dictionary whose keys are the column names. `msg.selected` is set to `True` if the row was selected and to `False` if the row was de-selected. Both selection and de-selection fire the same rowSelected event and `msg.selected` can be used to distinguish between them. 

The index of the row for which the selection or de-selection occurred is found in `msg.rowIndex`. If the same row that was previously selected is deselected, `row_data_div` content is set to the empty string.

## Example 2

This previous example is not very interesting. Let's change it to display a chart of the selected row instead.

```python
import justpy as jp
import pandas as pd

wm_df = pd.read_csv('https://elimintz.github.io/women_majors.csv').round(2)

def row_selected(self, msg):
    print(msg)
    if msg.selected:
        categories, values = list(msg.data.keys()), list(msg.data.values())
        o = self.row_chart.options
        o.title.text = f'{values[0]} - Percent Women in Major'
        o.xAxis.categories = categories[1:]
        s = jp.Dict({'name': values[0], 'data': values[1:]})
        s.dataLabels.enabled = True
        if len(o.series) > 0:
            o.series[0] = s
        else:
            o.series.append(s)
        self.row_selected = msg.rowIndex
        self.row_chart.show = True
    elif self.row_selected == msg.rowIndex:
        self.row_chart.show = False

def grid_test():
    wp = jp.WebPage()
    row_chart = jp.HighCharts(a=wp)
    row_chart.options.chart.type = 'column'
    row_chart.options.yAxis.title.text = '%'
    row_chart.show = False
    grid = wm_df.jp.ag_grid(a=wp)
    grid.row_chart = row_chart
    grid.on('rowSelected', row_selected)
    grid.options.columnDefs[0].checkboxSelection = True
    return wp

jp.justpy(grid_test)
```

The chart is created once when the page is requested, but the first and only series in it is changed to reflect the new values once a row is selected.

## Event Properties
 
Ag-Grid supports many [events](https://www.ag-grid.com/javascript-grid-events/). All the events supported by the community version can be captured and acted upon using JustPy. Each event contains different properties most of which JustPy makes available to the event handler through its second argument (`msg` in the tutorial).  

A simple way to see which properties are available is to print `msg`. Another way is to go [here](https://www.ag-grid.com/javascript-grid-events/#properties-and-hierarchy).

In the case of an event being one of `['sortChanged', 'filterChanged', 'columnMoved', 'rowDragEnd']` all the data in the gird after sorting and filtering is put into `msg.data` in CSV format.

!> When working with websockets, the size of each message is limited to 1 MByte after compression when using uvicorn, so if your tables are larger, use Ajax by setting the `websockets` key word argument of the `justpy` command to `False`.


  