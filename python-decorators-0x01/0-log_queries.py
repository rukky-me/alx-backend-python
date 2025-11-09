#!/usr/bin/python3
"""
A simple example showing how to use a decorator to log SQL queries.
"""

import sqlite3
import functools
import os

DB_FILE = "users.db"


# --- Setup function to create database and sample data ---
def setup_database():
    """Create an SQLite database with a 'users' table and sample entries."""
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    print(f"Setting up new database: {DB_FILE}")

    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL
            )
        """)
        sample_data = [
            ("John Doe", "john@example.com"),
            ("Jane Lee", "jane@example.com"),
            ("Carlos Brown", "carlos@example.com")
        ]
        cursor.executemany(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            sample_data
        )
    print("Database setup complete.\n")


# --- Decorator to log SQL queries ---
def log_queries(func):
    """Decorator that logs an SQL query before executing the function."""
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        query = kwargs.get("query") or (args[0] if args else None)
        if query:
            print(f"[LOG] Executing SQL Query: {query}")
        else:
            print("[LOG] No query found.")
        
        try:
            result = func(*args, **kwargs)
            print("[LOG] Query executed successfully.\n")
            return result
        except Exception as e:
            print(f"[LOG] Error executing query: {e}")
            raise
    
    return wrapper


# --- Function using the decorator ---
@log_queries
def fetch_all_users(query):
    """Fetch all records from the 'users' table."""
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()


# --- Main Execution ---
if __name__ == "__main__":
    setup_database()
    print("--- Fetching data using decorated function ---")
    users = fetch_all_users(query="SELECT * FROM users")

    print("--- Results ---")
    for user in users:
        print(user)
