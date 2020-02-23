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
      {headerName: "Action", field: "action"}
    ],
      rowData: [
      {make: "Toyota", model: "Celica", price: 35000},
      {make: "Ford", model: "Mondeo", price: 32000},
      {make: "Porsche", model: "Boxter", price: 72000}
    ]
}
"""
# <i class="fas fa-dragon"></i>

def cell_clicked(self, msg):
    print(msg)

def grid_test():
    # ' <i class="fas fa-trash-alt">&nbsp;<i class="fas fa-edit"></i>'
    wp = jp.WebPage()
    grid = jp.AgGrid(a=wp, options=grid_options)
    grid.html_columns = [3]
    for data in grid.options.rowData:
        print(data)
        d = jp.Div()
        jp.I(a=d, classes='fas fa-trash-alt', click='print(msg)')
        jp.Span(text='&nbsp;', a=d)
        jp.I(a=d, classes='fas fa-edit')
        data.action = d.to_html(format=False)
        print(data)
    grid.on('cellClicked', cell_clicked)
    return wp

jp.justpy(grid_test)
