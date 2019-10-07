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
        o.series[0] = jp.Dict({'name': values[0], 'data': values[1:]})
        o.series[0].dataLabels.enabled = True
        self.row_selected = msg.rowIndex
        self.row_chart.show = True
    elif self.row_selected == msg.rowIndex:
        self.row_chart.show = False

def grid_test():
    wp = jp.WebPage()
    row_chart = jp.HighCharts(a=wp)
    row_chart.options.chart.type = 'bar'
    row_chart.options.yAxis.title.text = '%'
    row_chart.options.series = [None]
    row_chart.show = False
    grid = wm_df.jp.ag_grid(a=wp)
    grid.row_chart = row_chart
    grid.on('rowSelected', row_selected)
    grid.options.columnDefs[0].checkboxSelection = True
    return wp

jp.justpy(grid_test)

style = 'height: 80vh; width: 99%; margin: 0.25rem; padding: 0.25rem;'

# grid = wm.jp.ag_grid(a=wp)
# grid = jp.AgGrid(a=wp)
#     grid.load_pandas_frame(wm_df)
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

def grid_test1():
    wp = jp.WebPage()
    grid = jp.AgGrid(a=wp, options=grid_options, style='height: 200px; width: 300px; margin: 0.25em')
    for col_def in grid.options.columnDefs:
        col_def.editable = True
    grid.options.columnDefs[1].cellClass = ['text-2xl','text-red-500','hover:bg-blue-500']
    return wp

# jp.justpy(grid_test)

s1 = """
 paginationAutoPageSize: true,
    pagination: false,
 columnDefs: [
      {headerName: "Make", field: "make", checkboxSelection: true},
      {headerName: "Model", field: "model", cellClass: ['text-2xl','text-red-500','hover:bg-blue-500']},
      {headerName: "Price", field: "price", editable: true}
    ],
"""


def grid_test():
    wp = jp.WebPage()
    for theme in ['ag-theme-balham', 'ag-theme-balham-dark', 'ag-theme-material']:
        grid = jp.AgGrid(a=wp, options=grid_options, theme=theme)
    return wp

    # grid = jp.AgGrid(a=wp, classes='m-2 p-2', style='height: 500px; width: 500px', auto_size=True, options=grid_options, theme='ag-theme-balham')


    # print(grid.options)
    # grid.options = grid_options
    # grid.load_pandas_frame(df)
    # grid.options.rowHeight = 25
    # for col in grid.options.columnDefs:
        # col.width = 150
        # col.editable = True
        # col.autoHeight = True
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

