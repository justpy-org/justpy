import justpy as jp
import sqlite3
import pandas as pd

# Download the database file to the local directory
# from: https://elimintz.github.io/chinook.db, originally from https://www.sqlitetutorial.net/
con = sqlite3.connect('chinook.db')
table_names = ['albums', 'artists', 'customers', 'sqlite_sequence', 'employees', 'genres', 'invoices', 'invoice_items',
          'media_types', 'playlists', 'playlist_track', 'tracks', 'sqlite_stat1']

tables = {}
for table_name in table_names:
    tables[table_name] = pd.read_sql_query(f"SELECT * from {table_name}", con)


def selected_event(self, msg):
    new_grid = tables[msg.value].jp.ag_grid(temp=True)
    msg.page.g.options.columnDefs = new_grid.options.columnDefs
    msg.page.g.options.rowData = new_grid.options.rowData

def row_selected(self, msg):
    print(msg)
    if msg.selected:
        # temp_grid = pd.read_sql_query(f"SELECT * from invoices WHERE customerid = {msg.data.CustomerId}", con).jp.ag_grid(temp=True)
        temp_grid = pd.read_sql_query(f"SELECT customerid, invoiceid, invoicedate, total from invoices WHERE customerid = {msg.data.CustomerId}", con).jp.ag_grid(temp=True)
        self.invoices.options.rowData = temp_grid.options.rowData
        self.invoices.options.columnDefs = temp_grid.options.columnDefs
        # self.auto_size = False


def db_test():
    wp = jp.WebPage()
    # table_name = request.query_params.get('table', 'albums')
    d = jp.Div(classes='flex', a=wp)
    customers = tables['customers'].jp.ag_grid(a=d, style='height: 90vh; width: 47%; margin: 0.25rem; padding: 0.25rem;')
    customers.options.pagination = True
    customers.options.paginationAutoPageSize = True
    customers.options.rowSelection = 'single'
    customers.on('rowSelected', row_selected)
    invoices = tables['invoices'].jp.ag_grid(a=d, style='height: 90vh; width: 47%; margin: 0.25rem; padding: 0.25rem;')
    invoices.options.pagination = True
    invoices.options.paginationAutoPageSize = True
    customers.invoices = invoices
    return wp


jp.justpy(db_test)
