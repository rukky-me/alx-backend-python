import sqlite3
import functools

# Decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Get the query argument (assuming it's passed as a positional or keyword argument)
        query = kwargs.get('query') if 'query' in kwargs else args[0] if args else None
        if query:
            print(f"Executing SQL Query: {query}")
        else:
            print("No SQL query found.")
        # Execute the original function
        result = func(*args, **kwargs)
        return result
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
