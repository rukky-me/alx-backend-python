#!/usr/bin/python3
"""
Class-based context manager to handle SQLite database connections
automatically

import sqlite3

DB_FILE = "users.db"


# --- Context Manager Class ---
class DatabaseConnection:
    """Context manager for SQLite database connections."""
    
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None
    
    def __enter__(self):
        # Open the database connection and return it
        self.conn = sqlite3.connect(self.db_file)
        return self.conn
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Close the connection automatically
        if self.conn:
            self.conn.close()
            print("[LOG] Database connection closed.")

        
        return False


# --- Main Execution ---
if __name__ == "__main__":
    
    # Use the context manager to perform a query
    with DatabaseConnection(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()

    # Print results
    print("--- Users in database ---")
    for user in users:
        print(user)
