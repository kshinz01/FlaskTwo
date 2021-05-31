import sqlite3
from user import User

users = [
    (1, 'ken', 'password'),
    (2, 'test', 'password'),
    (3, 'Jose', 'password'),
    ]


# DB setup
connection = sqlite3.connect('data.db')
cursor = connection.cursor()


# Insert query
insert_query = "INSERT INTO users VALUES (?,?,?)"
cursor.executemany(insert_query, users)


# Select query
select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)


# DB Clean Up
connection.commit()
connection.close()

