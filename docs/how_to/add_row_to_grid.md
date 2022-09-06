# How to Add a Row to a Grid

```python
import justpy as jp


grid_options = {
    'defaultColDef': {'filter': True, 'sortable': True, 'resizable': True, 'cellStyle': {'textAlign': 'center'},
                      'headerClass': 'font-bold'},
    'columnDefs': [{'headerName': 'Make', 'field': 'make', 'editable': True},
                   {'headerName': 'Model', 'field': 'model', 'editable': True},
                   {'headerName': 'Price', 'field': 'price', 'editable': True}
                   ],
    'rowData': [{'make': 'Toyota', 'model': 'Celica', 'price': 35000},
                {'make': 'Ford', 'model': 'Mondeo', 'price': 32000},
                {'make': 'Porsche', 'model': 'Boxter', 'price': 72000}]}



def add_row(self, msg):
    self.grid.options.rowData.append({'make': 'Tesla', 'model': 'Roadster', 'price': 95000})


def grid_test_row1():
    wp = jp.WebPage()
    add_row_btn = jp.Button(text='Add Row', classes='m-2 ' + jp.Styles.button_simple, a=wp, click=add_row)
    grid = jp.AgGrid(a=wp, options=grid_options, auto_size=False)
    add_row_btn.grid = grid
    return wp


jp.justpy(grid_test_row1)

```
