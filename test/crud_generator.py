
import sqlite3
# https://stackoverflow.com/questions/305378/list-of-tables-db-schema-dump-etc-using-the-python-sqlite3-api
# https://stackoverflow.com/questions/7831371/is-there-a-way-to-get-a-list-of-column-names-in-sqlite/38854129
con = sqlite3.connect('chinook.db')
# cursor = con.cursor()
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# print(cursor.fetchall())

def get_tables(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return [i[0] for i in cursor.fetchall() if not i[0].startswith('sqlite')]

def get_columns(table, conn):
    cursor = conn.execute(f'select * from {table}')
    return [description[0] for description in cursor.description]

for table in get_tables(con):
    print(f'{table}: {get_columns(table,con)}')

