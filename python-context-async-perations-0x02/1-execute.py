#!/usr/bin/python3
"""
A reusable class-based context manager that executes a query
and manages both the database connection and query execution.
"""

import sqlite3

DB_FILE = "users.db"


class ExecuteQuery:
    """Custom context manager that executes a given SQL query automatically."""
    
    def __init__(self, db_file, query, params=None):
        """
        Initialize the context manager.
        
        :param db_file: Path to the SQLite database file
        :param query: SQL query string
        :param params: Optional parameters for parameterized queries (tuple)
        """
        self.db_file = db_file
        self.query = query
        self.params = params or ()
        self.conn = None
        self.result = None

    def __enter__(self):
        """Open connection, execute query, and return results."""
        self.conn = sqlite3.connect(self.db_file)
        cursor = self.conn.cursor()
        cursor.execute(self.query, self.params)
        self.result = cursor.fetchall()
        return self.result  # The result is available as the 'as' variable

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the connection automatically."""
        if self.conn:
            self.conn.close()
            print("[LOG] Database connection closed.")
        # Do not suppress exceptions
        return False


# --- Example Usage ---
if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    with ExecuteQuery(DB_FILE, query, params) as results:
        print("--- Query Results ---")
        for row in results:
            print(row)
