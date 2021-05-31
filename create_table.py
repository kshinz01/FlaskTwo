import sqlite3

# DB setup
connection = sqlite3.connect('data.db')
cursor = connection.cursor()


# Create query
create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS items (name text, price real)"
cursor.execute(create_table)

cursor.execute("INSERT INTO items VALUES ('test', 10.99)")

# DB Clean Up
connection.commit()
connection.close()
