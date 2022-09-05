# Grid Events

## Example 1

Ag-Grid supports many [events](https://www.ag-grid.com/javascript-grid-events/). Let's look at some examples.

To begin, let's display in a separate Div the data from a grid row when it is selected.

```python
import justpy as jp
import pandas as pd

wm_df = pd.read_csv('https://elimintz.github.io/women_majors.csv').round(2)

def row_selected2(self, msg):
    print(msg)
    if msg.selected:
        self.row_data_div.text = msg.data
        self.row_selected2 = msg.rowIndex
    elif self.row_selected2 == msg.rowIndex:
        self.row_data_div.text = ''

def grid_test11():
    wp = jp.WebPage()
    row_data_div = jp.Div(a=wp)
    grid = wm_df.jp.ag_grid(a=wp)
    grid.row_data_div = row_data_div
    grid.on('rowSelected', row_selected2)
    grid.options.columnDefs[0].checkboxSelection = True
    return wp

jp.justpy(grid_test11)
```

We add a Div named `row_data_div` to the page and the `row_selected2` function, the event handler for the grid's rowSelected event, sets the row data as the text of the Div. 

JustPy provides in `msg.data` all the data from the row in a form of a dictionary whose keys are the column names. `msg.selected` is set to `True` if the row was selected and to `False` if the row was de-selected. Both selection and de-selection fire the same rowSelected event and `msg.selected` can be used to distinguish between them. 

The index of the row for which the selection or de-selection occurred is found in `msg.rowIndex`. If the same row that was previously selected is deselected, `row_data_div` content is set to the empty string.

## Example 2

This previous example is not very interesting. Let's change it to display a chart of the selected row instead.

```python
import justpy as jp
import pandas as pd

wm_df = pd.read_csv('https://elimintz.github.io/women_majors.csv').round(2)

def row_selected3(self, msg):
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
        self.row_selected3 = msg.rowIndex
        self.row_chart.show = True
    elif self.row_selected3 == msg.rowIndex:
        self.row_chart.show = False

def grid_test12():
    wp = jp.WebPage()
    row_chart = jp.HighCharts(a=wp)
    row_chart.options.chart.type = 'column'
    row_chart.options.yAxis.title.text = '%'
    row_chart.show = False
    grid = wm_df.jp.ag_grid(a=wp)
    grid.row_chart = row_chart
    grid.on('rowSelected', row_selected3)
    grid.options.columnDefs[0].checkboxSelection = True
    return wp

jp.justpy(grid_test12)
```

The chart is created once when the page is requested, but the first and only series in it is changed to reflect the new values once a row is selected.

## Example 3 - Multiple Row Selection

```python
import justpy as jp

grid_options = """
{
    rowSelection: 'multiple',
    defaultColDef: {
        filter: true,
        sortable: true,
        resizable: true,
        cellStyle: {textAlign: 'center'},
        headerClass: 'font-bold'
    }, 
      columnDefs: [
      {headerName: "Make", field: "make"},
      {headerName: "Model", field: "model"},
      {headerName: "Price", field: "price"}
    ],
      rowData: [
      {make: "Toyota", model: "Celica", price: 35000},
      {make: "Ford", model: "Mondeo", price: 32000},
      {make: "Porsche", model: "Boxter", price: 72000}
    ]
}
"""

def row_selected4(self, msg):
    print(msg.selected, msg)
    wp = msg.page
    if msg.selected:
        wp.selected_rows[msg.rowIndex] = msg.data
    else:
        wp.selected_rows.pop(msg.rowIndex)
    s = f'Selected rows {sorted(list(wp.selected_rows.keys()))}'
    for i in sorted(wp.selected_rows):
        s = f'{s}\n Row {i}  Data: {wp.selected_rows[i]}'
    if wp.selected_rows:
        wp.rows_div.text = s
    else:
        wp.rows_div.text = 'No row selected'


def grid_test13():
    wp = jp.WebPage()
    wp.selected_rows = {}  # Dictionary holding selected rows
    grid = jp.AgGrid(a=wp, options=grid_options, style='height: 200px; width: 300px; margin: 0.25em')
    grid.options.columnDefs[0].checkboxSelection = True
    grid.on('rowSelected', row_selected4)
    wp.rows_div = jp.Pre(text='Data will go here when you select rows', classes='border text-lg', a=wp)
    return wp

jp.justpy(grid_test13)
```

## Event Properties
 
Ag-Grid supports many [events](https://www.ag-grid.com/javascript-grid-events/). All the events supported by the community version can be captured and acted upon using JustPy. Each event contains different properties most of which JustPy makes available to the event handler through its second argument (`msg` in the tutorial).  

A simple way to see which properties are available is to print `msg`. Another way is to go [here](https://www.ag-grid.com/javascript-grid-events/#properties-and-hierarchy).

In the case of an event being one of `['sortChanged', 'filterChanged', 'columnMoved', 'rowDragEnd']` all the data in the gird after sorting and filtering is put into `msg.data` in CSV format.

!!! warning
    When working with websockets, the size of each message is limited to 1 MByte when using uvicorn, so if your tables are larger, use Ajax by setting the `websockets` key word argument of the `justpy` command to `False`.


## Linking a chart and a grid using grid events

Using grid events, it requires a few lines of code to link a grid to a chart. Filtering and sorting changes in the grid, will be reflected in the chart.

```python
import justpy as jp
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/fivethirtyeight/data/master/alcohol-consumption/drinks.csv', encoding="ISO-8859-1")

def grid_change(self, msg):
    msg.page.df = jp.read_csv_from_string(msg.data)
    c = msg.page.df.jp.plot(0, [1,2,3,4], kind='column', classes='m-2 p-2 w-2/3 border', title='Alcohol Consumption per Country')
    msg.page.c.options = c.options

def grid_test14():
    wp = jp.WebPage()
    wp.df = df
    wp.c = df.jp.plot(0, [1,2,3,4], kind='column', a=wp, classes='m-2 p-2 border', title='Alcohol Consumption per Country')
    grid = df.jp.ag_grid(a=wp)
    for event_name in ['sortChanged', 'filterChanged', 'columnMoved', 'rowDragEnd']:
        grid.on(event_name, grid_change)
    return wp

jp.justpy(grid_test14)
```  

## Create a Component to Link Chart and Grid

The example above can be simplified even further by creating a component in which a chart and a grid are linked. With the new component in hand, charts and grids can be linked with one line of code.


```python
import justpy as jp
import pandas as pd

class LinkedChartGrid(jp.Div):

    def __init__(self, df, x, y, **kwargs):
        super().__init__(**kwargs)
        self.df = df
        self.x = x
        self.y = y
        self.kind = kwargs.get('kind', 'column')
        self.stacking = kwargs.get('stacking', '')
        self.title = kwargs.get('title', '')
        self.subtitle = kwargs.get('subtitle', '')
        self.set_classes('flex flex-col')
        self.chart = df.jp.plot(x, y, a=self, classes='m-2 p-2 border', kind=self.kind, stacking=self.stacking, title=self.title, subtitle=self.subtitle)
        self.grid = df.jp.ag_grid(a=self)
        self.grid.parent = self
        for event_name in ['sortChanged', 'filterChanged', 'columnMoved', 'rowDragEnd']:
            self.grid.on(event_name, self.grid_change)


    @staticmethod
    def grid_change(self, msg):
        self.parent.df = jp.read_csv_from_string(msg.data)
        c = self.parent.df.jp.plot(self.parent.x, self.parent.y, kind=self.parent.kind, title=self.parent.title,
                                   subtitle=self.parent.subtitle, stacking=self.parent.stacking)
        self.parent.chart.options = c.options



alcohol_df = pd.read_csv('https://raw.githubusercontent.com/fivethirtyeight/data/master/alcohol-consumption/drinks.csv', encoding="ISO-8859-1")
bad_drivers_df = pd.read_csv('https://raw.githubusercontent.com/fivethirtyeight/data/master/bad-drivers/bad-drivers.csv', encoding="ISO-8859-1")


def grid_test15():
    wp = jp.WebPage()
    c = LinkedChartGrid(alcohol_df, 0, [1,2,3,4], kind='column', a=wp, classes='m-4 p-2 border',
                        stacking='normal', title='Alcohol Consumption per Country', subtitle='538 data')
    LinkedChartGrid(bad_drivers_df, 0, [1,2,3,4,5,6,7], kind='column', a=wp, classes='m-4 p-2 border-4', title='Bad Drivers per US State', subtitle='538 data')
    return wp

jp.justpy(grid_test15)
```