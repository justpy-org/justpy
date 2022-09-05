# Creating Grids

Here is a simple example of a adding a grid to the page. 
```python
import justpy as jp

grid_options = """
{
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

def grid_test4():
    wp = jp.WebPage()
    grid = jp.AgGrid(a=wp, options=grid_options)
    return wp

jp.justpy(grid_test4)
```
In this case the grid options are defined using a string that represents a JavaScript object. It could also be a Python dictionary. The options object is described in the [ag_Grid documentation](https://www.ag-grid.com/documentation-main/documentation.php).
 
!!! note
    We will see later, that when working with pandas, JustPy can automate the process and there is no need to go into the grid specification details.

As mentioned above, AgGrid provides a default style to the grid when it is created. Let’s change that style. Replace the function `grid_test4` in the example above with the following:
```python
def grid_test5():
    wp = jp.WebPage()
    grid = jp.AgGrid(a=wp, options=grid_options, style='height: 200px; width: 300px; margin: 0.25em')
    return wp
```
When you run the program, the rendered grid is smaller.

After the grid is created, you can modify its options further. Let's add a data row after the grid is created:
 
```python
def grid_test6():
    wp = jp.WebPage()
    grid = jp.AgGrid(a=wp, options=grid_options, style='height: 200px; width: 300px; margin: 0.25em')
    grid.options.rowData.append({'make': 'Autocars', 'model': 'Sussita', 'price': 3})
    return wp
```

Let's make all columns editable and add a checkbox in the second column.
```python
def grid_test7():
    wp = jp.WebPage()
    grid = jp.AgGrid(a=wp, options=grid_options, style='height: 200px; width: 300px; margin: 0.25em')
    for col_def in grid.options.columnDefs:
        col_def.editable = True
    grid.options.columnDefs[1].checkboxSelection = True
    return wp
```

You can now edit any cell in the grid. After selecting a cell, just start typing.
The appearance of data in a column can be modified by assigning a list of classes to the `cellClass` attribute of a column definition. In the example below the appearance of the Model column is modified.

```python
def grid_test8():
    wp = jp.WebPage()
    grid = jp.AgGrid(a=wp, options=grid_options, style='height: 200px; width: 300px; margin: 0.25em')
    for col_def in grid.options.columnDefs:
        col_def.editable = True
    grid.options.columnDefs[1].cellClass = ['text-2xl','text-red-500','hover:bg-blue-500']
    return wp
```

Ag_Grid is very rich in features, very few which are covered here. For a detailed description of the grid features, please look at its [documentation](https://www.ag-grid.com/documentation-main/documentation.php). 
