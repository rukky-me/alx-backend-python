#!/usr/bin/python3
"""
A decorator example that caches database query results
to avoid redundant SQL calls.
"""

import sqlite3
import functools

DB_FILE = "users.db"
query_cache = {}  # Dictionary to hold cached query results


# --- Decorator to provide a database connection ---
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


# --- Cache decorator ---
def cache_query(func):
    """Decorator that caches results of SQL queries to avoid redundant DB calls."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the query argument
        query = kwargs.get("query") or (args[1] if len(args) > 1 else None)

        if not query:
            print("[CACHE] No query found.")
            return
