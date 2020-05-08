# Displaying Database Tables and Query Results

In the example below we use both pandas and ag-Grid to display database tables from an sqlite database.

!!! warning
    For the example to work you need to download the [chinook sqlite database](https://elimintz.github.io/chinook.db) and put it in the directory from which you are running the program. The file is a copy of the one found on https://www.sqlitetutorial.net/ which is an excellent resource for learning sqlite.

The program uses pandas ability to load a frame with the result of a SQL query. This is done using [`read_sql_query`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_sql_query.html).

Once the data is in a pandas frame, we use the JustPy pandas extension to create an AgGrid.

The program also has an additional request handler under the route '/city' which runs the following SQL command per request:
```sqlite
SELECT DISTINCT city, country, customerid from customers ORDER BY country
```

Again, the result is loaded into a pandas frame and using the pandas extension, an AgGrid is created.

After the tables are displayed, the user can then filter and sort the data further using ag-Grid's capabilities.  

```python
import justpy as jp
import sqlite3
import pandas as pd

# Download the database file to the local directory
# from: https://elimintz.github.io/chinook.db, originally from https://www.sqlitetutorial.net/
db_con = sqlite3.connect('chinook.db')
table_names = ['albums', 'artists', 'customers', 'sqlite_sequence', 'employees', 'genres', 'invoices', 'invoice_items',
          'media_types', 'playlists', 'playlist_track', 'tracks', 'sqlite_stat1']

tables = {}
for table_name in table_names:
    tables[table_name] = pd.read_sql_query(f"SELECT * from {table_name}", db_con)


def selected_event(self, msg):
    # Runs when a table name is selected
    # Create a new grid and use its column and row definitions for grid already on page
    new_grid = tables[msg.value].jp.ag_grid(temp=True)
    msg.page.g.options.columnDefs = new_grid.options.columnDefs
    msg.page.g.options.rowData = new_grid.options.rowData


def db_test(request):
    wp = jp.QuasarPage()
    table_name = request.query_params.get('table', 'albums')
    s = jp.QSelect(options=table_names, a=wp, label="Select Table", outlined=True, input=selected_event,
                   style='width: 350px; margin: 0.25rem; padding: 0.25rem;', value=table_name)
    g = tables[table_name].jp.ag_grid(a=wp, style='height: 90vh; width: 99%; margin: 0.25rem; padding: 0.25rem;')
    g.options.pagination = True
    g.options.paginationAutoPageSize = True
    wp.g = g
    return wp

@jp.SetRoute('/city')
def city_test():
    wp = jp.WebPage()
    g = pd.read_sql_query("SELECT DISTINCT city, country, customerid from customers ORDER BY country", db_con).jp.ag_grid(a=wp)
    g.style = 'height: 99vh; width: 450px; margin: 0.25rem; padding: 0.25rem;'
    return wp

jp.justpy(db_test)

```

