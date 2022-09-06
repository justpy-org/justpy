# Rendering Checkboxes

To render a column as a checkbox set the `cellRenderer` value of the column in `columnDefs' to 'checkboxRenderer'.

The value of a checkbox is either `True` or `False`.

In the example below, the 'Enabled' column is rendered as a checkbox.

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
      {headerName: "Price", field: "price"},
      {headerName: "Enabled", field: "enabled", cellRenderer: 'checkboxRenderer'}
    ],
      rowData: [
      {make: "Toyota", model: "Celica", price: 35000, enabled: false},
      {make: "Ford", model: "Mondeo", price: 32000, enabled: true},
      {make: "Porsche", model: "Boxter", price: 72000, enabled: false}
    ]
}
"""


def grid_change(self, msg):
    print(msg)


def grid_test_checkbox1():
    wp = jp.WebPage()
    grid = jp.AgGrid(a=wp, options=grid_options)
    grid.on('cellValueChanged', grid_change)
    return wp


jp.justpy(grid_test_checkbox1)
```
