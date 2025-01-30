import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Create new table with username, phone, email, and password
cursor.execute("""
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    phone TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")
conn.commit()

# print("Database created successfully!")
# conn = sqlite3.connect('users.db')
# cursor = conn.cursor()


# cursor.execute("""
#               SELECT * FROM user """)
# conn.commit()

# columns = cursor.fetchall()

# for column in columns:
#     print(column)

# cursor.execute("PRAGMA table_info(user)")
# columns = cursor.fetchall()
# for column in columns:
#     print(column)

# conn.close()
