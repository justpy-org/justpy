# Adding HTML to Cells
[Adding HTML to Cells live demo]({{demo_url}}/grid_add_test)

If you want to add an image or specific formatting to a cell in the grid, you can do so by using the `html_columns` attribute. Assign to this attribute a list of the column numbers that should be formatted using HTML.

In the example below, special formatting and an image are added to the `price` column.

```python
import justpy as jp


grid_options = {
    'rowHeight': 200,
    'columnDefs': [
      {'headerName': "Make", 'field': "make"},
      {'headerName': "Model", 'field': "model"},
      {'headerName': "Price", 'field': "price"},
    ],
    'rowData': [
      {'make': "Toyota", 'model': "Celica", 'price': 4},
      {'make': "Ford", 'model': "Mondeo", 'price': '<div class="m-2 text-red-500 text-5xl">3</div>'},
      {'make': "Porsche", 'model': "Boxter", 'price': '<img src="https://www.python.org/static/community_logos/python-powered-h-140x182.png">'}
    ],
}

def grid_add_test():
    wp = jp.WebPage()
    grid = jp.AgGrid(a=wp, options=grid_options)
    grid.html_columns = [2]
    return wp

jp.justpy(grid_add_test)
```
