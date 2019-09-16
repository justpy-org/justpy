import justpy as jp
import pandas as pd

grid_options = """
{
    paginationAutoPageSize: true,
    pagination: false,
    defaultColDef: {
        filter: true,
        sortable: true,
        resizable: true,
        cellStyle: {textAlign: 'center'},
        headerClass: 'font-bold',
        width: 100
    }, 
      columnDefs: [
      {headerName: "Make", field: "make", sortable: true, resizable: true, checkboxSelection: true},
      {headerName: "Model", field: "model", cellClass: ['text-2xl','text-red-500','hover:bg-blue-500']},
      {headerName: "Price", field: "price", sortable: true, resizable: true, editable: true}
    ],
      rowData: [
      {make: "Toyota", model: "Celica", price: 35000},
      {make: "Ford", model: "Mondeo", price: 32000},
      {make: "Porsche", model: "Boxter", price: 72000}
    ]
}
"""

df =  pd.read_csv(f'https://elimintz.github.io/stocks/MSFT.csv').round(2)
# Index(['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'], dtype='object')

def grid_test():
    wp = jp.WebPage()
    jp.Hello(a=wp)
    d = jp.Div(text='Data will go here', classes='m-2 p-2 text-2xl', a=wp)
    grid = jp.AgGrid(a=wp, classes='m-2 p-2', style='height: 500px; width: 500px', auto_size=True, theme='ag-theme-balham')

    print(grid.options)
    # grid.options = grid_options
    grid.load_pandas_frame(df)
    # grid.options.rowHeight = 25
    for col in grid.options.columnDefs:
        # col.width = 150
        col.editable = True
        col.autoHeight = True
        # col.cellClass = ['text-xl', 'text-red-500', 'hover:bg-blue-500']
    # grid.auto_size = False
    # grid.events = ['cellClicked']
    def cell_click(self, msg):
        print(msg)
        d.text = f'Row clicked: {msg.rowIndex}, colid: {msg.colId} value: {msg.value} \n data: {msg.data}'
    # grid.on('cellMouseOver', cell_click)
    grid.on('cellValueChanged', cell_click)
    return wp

def qgrid_test():
    wp = jp.QuasarPage()
    jp.Hello(a=wp)
    d = jp.Div(text='Data will go here', classes='m-2 p-2 text-2xl', a=wp)
    grid = jp.QTable(a=wp)
    grid.load_pandas_frame(df)
    return wp

jp.justpy(grid_test)