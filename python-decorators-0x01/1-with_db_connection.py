#!/usr/bin/python3
"""
A decorator that automatically handles opening and closing
the SQLite database connection for any function.
"""

import sqlite3
import functools

DB_FILE = "users.db"


# --- Decorator Definition ---
def with_db_connection(func):
    """Decorator that opens a DB connection, passes it to the function, and closes it afterward."""
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 1. Open the database connection
        conn = sqlite3.connect(DB_FILE)
        try:
            # 2. Pass the connection to the decorated function
            result = func(conn, *args, **kwargs)
            return result
        finally:
            # 3. Always close the connection (even if an error occurs)
            conn.close()
            print("[LOG] Database connection closed.\n")
    
    return wrapper


# --- Function using the decorator ---
@with_db_connection
def get_user_by_id(conn, user_id):
    """Fetch a single user by ID from the users table."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


# --- Main Test ---
if __name__ == "__main__":
    user = get_user_by_id(user_id=1)
    print("Fetched user:", user)
