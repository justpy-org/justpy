# Using Pandas to Create Grids

## Loading a Frame into a Grid

The AgGrid method `load_pandas_frame(df)` makes it simple to load data from a pandas frame into a grid.

The example below reads a CSV file into a pandas frame and then uses the grid to display the data. The data shows the percentage of women in each college major per year.

!!! warning
    To run the example below you will need to have pandas installed.

```python
import justpy as jp
import pandas as pd

wm_df = pd.read_csv('https://elimintz.github.io/women_majors.csv').round(2)

def grid_test16():
    wp = jp.WebPage()
    grid = jp.AgGrid(a=wp)
    grid.load_pandas_frame(wm_df)
    return wp

jp.justpy(grid_test16)
```

Mouseover one of the column headers and click on the "three horizontal lines" <i class="fas fa-bars"></i> icon that appears to the right of the column name. You can now filter the data in the column. By clicking the arrows in the column heading you can sort the grid according to the values in the column.

## Pandas Extension

JustPy comes with a pandas extension that makes loading panadas frames into a grid compatible with the Pandas syntax.
The program below is equivalent to the one above:

### load women_majors.csv with pandas
```python
import justpy as jp
import pandas as pd

wm_df = pd.read_csv('https://elimintz.github.io/women_majors.csv').round(2)

def grid_test17():
    wp = jp.WebPage()
    wm_df.jp.ag_grid(a=wp)
    return wp

jp.justpy(grid_test17)
```

The JustPy functionality is added to pandas under the namespace "jp". The `ag_grid` method creates a grid based on the frame's data and returns an instance of AgGrid.

The grid can be further modified after it is created:

### load women_majors.csv with pandas and modify after creation
```python
import justpy as jp
import pandas as pd

wm_df = pd.read_csv('https://elimintz.github.io/women_majors.csv').round(2)

def grid_test18():
    wp = jp.WebPage()
    grid = wm_df.jp.ag_grid(a=wp)
    grid.options.pagination = True
    grid.options.paginationAutoPageSize = True
    grid.options.columnDefs[0].cellClass = ['text-white', 'bg-blue-500', 'hover:bg-blue-200']
    for col_def in grid.options.columnDefs[1:]:
        col_def.cellClassRules = {
            'font-bold': 'x < 20',
            'bg-red-300': 'x < 20',
            'bg-yellow-300': 'x >= 20 && x < 50',
            'bg-green-300': 'x >= 50'
        }
    return wp

jp.justpy(grid_test18)
```

The example above sets the grid to be paginated instead of scrolled. The data is formatted so that any number under 20 is in a bold font and the background of the cell is red. Cells with values between 20 and 50 receive a background of yellow and those above 50 are green.

The [ag-Grid documentation](https://www.ag-grid.com/documentation-main/documentation.php) is extensive and should be consulted for the features that the grid support.
