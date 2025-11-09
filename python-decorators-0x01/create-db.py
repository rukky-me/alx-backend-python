import sqlite3

# Connect to (or create) the database file
conn = sqlite3.connect("users.db")

# Create a cursor to execute SQL statements
cursor = conn.cursor()

# Create the 'users' table if it doesn’t exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
)
""")

# Commit changes and close connection
conn.commit()
conn.close()

print("Database and 'users' table created successfully!")
