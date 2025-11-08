#!/usr/bin/python3
"""
This script defines two generator functions:
1. stream_users_in_batches(batch_size) - fetches data in batches.
2. batch_processing(batch_size) - filters each batch for users over age 25.
"""

import mysql.connector   # Library to connect Python with MySQL


# FUNCTION: Stream users from DB in batches

def stream_users_in_batches(batch_size):
    """
    Generator that fetches rows from user_data table in batches.
    Each yield returns a list of dictionaries (a batch).
    """
    # Connect to the MySQL database
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ALX_prodev"
    )

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data;")  # Fetch all rows from table

    # Create an empty list to temporarily hold rows (a batch)
    batch = []

    # Loop through each row returned by MySQL
    for row in cursor:
        batch.append(row)               # Add rows to the batch
        if len(batch) == batch_size:    # When batch reaches the target size
            yield batch                 # Yield sends out the batch
            batch = []                  # Empty the batch list for next group

    # After the loop ends, there may be leftover rows smaller than batch_size
    if batch:                           # so if there's a partial batch left
        yield batch                     # Yield the remaining users

    # Close database connection and cursor
    cursor.close()
    connection.close()


# FUNCTION: Process (filter) each batch

def batch_processing(batch_size):
    """
    Generator that filters users over age 25 from each batch.
    Uses the stream_users_in_batches generator for data input.
    """
    # Loop through each batch from the streaming generator
    for batch in stream_users_in_batches(batch_size):
        # Create a new list of users whose age is greater than 25
        filtered_batch = [user for user in batch if user['age'] > 25]

        # Yield the filtered result (a batch of users over 25)
        yield filtered_batch
