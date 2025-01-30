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

cursor.execute("""
INSERT INTO user(username, phone, email, password) VALUES (username,phone,email,password)  
""")



conn.commit()
conn.close()
print("Database updated successfully!")
