# Justpy Tutorial demo grid_test4 from docs/grids_tutorial/creating_grids.md
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

# initialize the demo
from  examples.basedemo import Demo
Demo ("grid_test4",grid_test4)
