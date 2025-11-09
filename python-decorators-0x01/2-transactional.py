#!/usr/bin/python3
"""
A decorator example that manages database transactions automatically.
"""

import sqlite3
import functools

DB_FILE = "users.db"


# Decorator to provide a database connection 
def with_db_connection(func):
    """Decorator that provides a database connection to a function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect(DB_FILE)
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper


# Decorator to manage transactions 
def transactional(func):
    """Decorator that commits or rolls back database transactions."""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()  # Commit if everything goes well
            print("[LOG] Transaction committed successfully.")
            return result
        except Exception as e:
            conn.rollback()  # Rollback if there’s an error
            print(f"[LOG] Transaction rolled back due to error: {e}")
            raise  # Re-raise the exception so it’s visible
    return wrapper


# Function using both decorators 
@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    """Update a user's email in the database."""
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
    print(f"[LOG] Updated user ID {user_id} with new email: {new_email}")


# Run example 
if __name__ == "__main__":
    update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
