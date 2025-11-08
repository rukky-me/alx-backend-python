#!/usr/bin/python3
"""
Simulate fetching paginated data lazily using a generator.
"""

import seed  

# Function: Fetch one "page" of users

def paginate_users(page_size, offset):
    """
    Fetch one page of users from the user_data table.

    Args:
        page_size (int): Number of users to fetch in one page.
        offset (int): Starting point (like 'skip' in pagination).

    Returns:
        list: A list of user dictionaries (rows from the DB).
    """
    # Connect to your MySQL database
    connection = seed.connect_to_prodev()

    # Using dictionary=True makes cursor return each row as a dictionary
    cursor = connection.cursor(dictionary=True)

    # SQL: fetch page_size number of rows, starting at offset
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")

    # Get all rows for this page
    rows = cursor.fetchall()

    # Close the connection to free resources
    connection.close()

    # Return this batch of rows
    return rows


# Generator Function: Lazily paginate user
def lazy_pagination(page_size):
    """
    Lazily fetch user data from the DB one page at a time.
    Only one loop is allowed.
    Uses yield to send data one batch at a time.

    Args:
        page_size (int): Number of rows per page.

    Yields:
        list: A page (list) of user records.
    """
    offset = 0  # start from the first record

    while True:  # only ONE loop
        # Fetch one page of users
        page = paginate_users(page_size, offset)

        # If no data is returned, we've reached the end
        if not page:
            break

        # Yield (pause here) and send page back to the caller
        yield page

        # Move to next set of rows
        offset += page_size
