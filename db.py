import sqlite3

conn = sqlite3.connect('classroom.db')

cursor = conn.cursor()

# cursor.execute(
#     """
#     CREATE TABLE user (
#       id INTEGER PRIMARY KEY AUTOINCREMENT,
#       username TEXT UNIQUE NOT NULL,
#       password TEXT NOT NULL
#     )
#     """
# )

conn.commit()

conn.close()