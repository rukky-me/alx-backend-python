#!/usr/bin/python3
"""
This script defines a decorator that logs SQL queries before execution.
It uses an already existing SQLite database named 'users.db'.
"""

import sqlite3
import functools

# --- Decorator Definition ---
def log_queries(func):
    """
    A decorator that logs the SQL query before executing the function.
    """
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the query argument (can be passed positionally or by name)
        query = None
        if args:  # positional argument
            query = args[0]
        elif "query" in kwargs:  # keyword argument
            query = kwargs["query"]

        # Log the SQL query before execution
        if query:
            print(f"[LOG] About to execute SQL query: {query}")
        else:
            print("[LOG] No SQL query provided.")
        
        # Execute the original function
        try:
            result = func(*args, **kwargs)
            print("[LOG] Query executed successfully.\n")
            return result
        except Exception as e:
            print(f"[LOG] Error executing query: {e}\n")
            raise

    return wrapper


# --- Function that runs a query ---
@log_queries
def fetch_all_users(query):
    """
    Fetches all users from the existing 'users.db' database.
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# Test Run 
if __name__ == "__main__":
    users = fetch_all_users(query="SELECT * FROM users")
    print("Users in database:")
    for user in users:
        print(user)
