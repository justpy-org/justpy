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

class Issue50:
    """
    Issue 50 example code
    """
    def cell_changed(self, msg):
        """
        react on a changed cell value
        """
        print(msg)
        change_msg=f"'Old value: {msg.oldValue}, New value: {msg.newValue}, Row Index: {msg.rowIndex}, Column ID: {msg.colId}'"
        self.feedback.text=change_msg
        print(change_msg)
        print(f'Row data: {msg.data}')
        # Here you would update your database or Pandas frame etc.
    
    def grid_test(self):
        """
        WebPage to test justpy issue 50
        """
        wp = jp.WebPage()
        self.feedback=jp.Div(a=wp,text="edit a grid cell ...")
        grid = jp.AgGrid(a=wp, options=grid_options, style='height: 200px; width: 300px; margin: 0.25em')
        for col_def in grid.options.columnDefs:
            col_def.editable = True  # You can add this directly to the columnDefs in grid_options
        grid.on('cellValueChanged', self.cell_changed)
        return wp

def issue50_grid_test():
    """
    object oriented wrapper
    """
    issue50=Issue50()
    return issue50.grid_test()

# make me available on the command line and for the demo_browser
from examples.basedemo import Demo
Demo("Issue 50 aggrid cell value changed", issue50_grid_test)
