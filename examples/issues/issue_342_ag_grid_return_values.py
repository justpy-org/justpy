import justpy as jp
import pandas as pd

grid_options_1 = """
{
    rowSelection: 'multiple',
    defaultColDef: {
        filter: true,
        sortable: true,
        resizable: true,
        cellStyle: {textAlign: 'center'},
        headerClass: 'font-bold'
    }
}
"""
# df1 = <data>
df1 = {}

def issue_342_grid_test(request):

  # ?? how do you get AG-Grid get api information --->
  async def saveGridState(self, msg):
    wp = msg.page
    wp.column_state = await self.grid.run_api('columnApi.getColumnState()', msg.page)


  wp = jp.WebPage()
  wp.selected_rows = {}  # Dictionary holding selected rows
  wp.column_state = {}   # attempt to save the column state from AG-Grid api
  grid = jp.AgGrid(a=wp, options=grid_options_1, style='height: 400px; width: 800px; margin: 0.25em')

  grid.load_pandas_frame(df1)
  wp.rows_div = jp.Pre(text='Use Save Col State btn to save settings', classes='border text-lg', a=wp)
  btn_state = jp.Button(text='Save Col State', classes=jp.Styles.button_simple+' m-2', a=wp, click=saveGridState)
  btn_state.grid = grid
  return wp

from examples.basedemo import Demo

Demo("Issue 342", issue_342_grid_test)
