import sqlite3
import functools

# This define the decorator
def log_queries(func):
    """A decorator that logs the SQL query before executing the function."""
    
    # This use functools.wraps to preserve metadata of the original function
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the query argument from the function call
        # This function can accept query either as a positional or keyword argument.
        
        if args:  # if query is passed positionally
            query = args[0]
        else:     # if query is passed as a keyword argument
            query = kwargs.get("query", None)
        
        # Log (print) the query before running
        print(f"[LOG] Executing SQL Query: {query}")
        
        # Execute the original function
        result = func(*args, **kwargs)
        
        # Optionally log after execution
        print("[LOG] Query executed successfully.\n")
        
        return result
    
    return wrapper  # return the wrapped version

# This apply the decorator to a function that runs a query
@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Step 8: Call the function to test it
users = fetch_all_users(query="SELECT * FROM users")
print(users)
