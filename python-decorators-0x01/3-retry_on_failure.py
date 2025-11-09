#!/usr/bin/python3
"""
A decorator example that retries database operations automatically
when transient errors occur.
"""

import time
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


# Retry decorator 
def retry_on_failure(retries=3, delay=2):
    """
    Decorator that retries a function if it fails due to transient errors.
    retries: number of attempts
    delay: seconds to wait between retries
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, retries + 1):
                try:
                    # Try running the function
                    result =
