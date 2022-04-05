import sqlite3

conn = sqlite3.connect("employees.sqlite")

cursor = conn.cursor()
sql_query = """ CREATE TABLE employee (
    id integer PRIMARY KEY,
    name text NOT NULL,
    email text NOT NULL,
    department text NOT NULL,
    salary integer NOT NULL,
    birth text NOT NULL
)"""

cursor.execute(sql_query)