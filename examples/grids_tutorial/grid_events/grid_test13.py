# Justpy Tutorial demo grid_test13 from docs/grids_tutorial/grid_events.md
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

# initialize the demo
from  examples.basedemo import Demo
Demo ("grid_test13",grid_test13)
