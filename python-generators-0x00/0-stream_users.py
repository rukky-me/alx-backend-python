#!/usr/bin/python3
"""
This script defines a generator function `stream_users`
that connects to a MySQL database and streams rows one by one
from the `user_data` table using the `yield` keyword.
"""

import mysql.connector  # Import MySQL library that will connect to the database


def stream_users():
    """
    Generator function that fetches rows one by one
    from the user_data table in ALX_prodev database.
    """
    
    # This connect to the MySQL database
  
    connection = mysql.connector.connect(
        host="localhost",     
        user="rukky",           # MySQL username 
        password="",           # MySQL password 
        database="ALX_prodev"  # The database that was created earlier
    )

    # Create a cursor to execute SQL commands
    # The argument dictionary=True makes each row a dictionary (column_name → value)
    cursor = connection.cursor(dictionary=True)

    # Run a SQL query to select all rows from the table
  
    cursor.execute("SELECT * FROM user_data;")

    
    # Loop through the cursor — but only one loop allowed!
    
    # Each iteration of this loop fetches ONE row from the database.
    # Instead of returning all rows at once, we yield them one by one.
    for row in cursor:
        yield row  # Send one row at a time to whoever called this function

    
    # Clean up resources when done
    
    cursor.close()       # This closes the cursor to free up memory
    connection.close()   # This closes the database connection
