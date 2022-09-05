# Running Grid API Commands

To run a grid API command use the grid's `run_api()` method. The method accepts two arguments. The first is a string representing the command and the second is the page the grid is on.

The example below uses the grid API to select and deselect rows.

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

def row_selected1(self, msg):
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


async def select_all_rows(self, msg):
    await self.grid.run_api('selectAll()', msg.page)


async def deselect_rows(self, msg):
    await self.grid.run_api('deselectAll()', msg.page)


def grid_test10():
    wp = jp.WebPage()
    wp.selected_rows = {}  # Dictionary holding selected rows
    grid = jp.AgGrid(a=wp, options=grid_options, style='height: 200px; width: 300px; margin: 0.25em')
    grid.options.columnDefs[0].checkboxSelection = True
    grid.on('rowSelected', row_selected1)
    wp.rows_div = jp.Pre(text='Data will go here when you select rows', classes='border text-lg', a=wp)
    btn_deselect = jp.Button(text='Deselect rows', classes=jp.Styles.button_simple+' m-2', a=wp, click=deselect_rows)
    btn_deselect.grid = grid
    btn_select_all = jp.Button(text='Select all rows', classes=jp.Styles.button_simple+' m-2', a=wp, click=select_all_rows)
    btn_select_all.grid = grid
    return wp


jp.justpy(grid_test10)
```