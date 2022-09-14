import justpy as jp
import sqlite3
import pandas as pd
import os
from jpcore.download import Download

# Download the database file to the $HOME/.justpy directory
# from: https://elimintz.github.io/chinook.db, originally from https://www.sqlitetutorial.net/

dbname = "chinook.db"
url = f"https://elimintz.github.io/{dbname}"
os.makedirs(Download.get_cache_path(), exist_ok=True)
filePath = f"{Download.get_cache_path()}/{dbname}"
Download.download_file(url, dbname, target_directory=Download.get_cache_path())

db_con = sqlite3.connect(filePath)
table_names = [
    "albums",
    "artists",
    "customers",
    "sqlite_sequence",
    "employees",
    "genres",
    "invoices",
    "invoice_items",
    "media_types",
    "playlists",
    "playlist_track",
    "tracks",
    "sqlite_stat1",
]

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
    table_name = request.query_params.get("table", "albums")
    s = jp.QSelect(
        options=table_names,
        a=wp,
        label="Select Table",
        outlined=True,
        input=selected_event,
        style="width: 350px; margin: 0.25rem; padding: 0.25rem;",
        value=table_name,
    )
    g = tables[table_name].jp.ag_grid(
        a=wp, style="height: 90vh; width: 99%; margin: 0.25rem; padding: 0.25rem;"
    )
    g.options.pagination = True
    g.options.paginationAutoPageSize = True
    wp.g = g
    return wp


@jp.SetRoute("/city")
def city_test():
    wp = jp.WebPage()
    g = pd.read_sql_query(
        "SELECT DISTINCT city, country, customerid from customers ORDER BY country",
        db_con,
    ).jp.ag_grid(a=wp)
    g.style = "height: 99vh; width: 450px; margin: 0.25rem; padding: 0.25rem;"
    return wp


from examples.basedemo import Demo

Demo("database test", db_test)
