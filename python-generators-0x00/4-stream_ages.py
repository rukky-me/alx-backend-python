#!/usr/bin/python3
"""
Compute the average user age using a memory-efficient generator.
"""

import seed  # import helper functions for DB connection

# 1️⃣ Generator: Stream user ages one by one

def stream_user_ages():
    """
    Generator function that yields user ages one by one from the database.
    Uses only one loop.
    """
    # Connect to the ALX_prodev database
    connection = seed.connect_to_prodev()

    # Create a cursor that returns normal tuples (not dictionaries)
    cursor = connection.cursor()

    # Execute SQL query to fetch all ages from the user_data table
    cursor.execute("SELECT age FROM user_data")

    # Loop over each row and yield the 'age' value
    for (age,) in cursor:
        yield age  # send each age one by one to whoever calls this generator

    # Close DB connection to free up resources
    connection.close()



# Consumer: Compute the average age efficiently

def compute_average_age():
    """
    Consumes the generator and computes the average user age
    without loading all data into memory.
    """
    total_age = 0  # accumulator for sum of ages
    count = 0      # counter for number of users

    # Loop over the generator (this is the 2nd and final loop)
    for age in stream_user_ages():
        total_age += age
        count += 1

    # Handle case when no users exist
    if count == 0:
        print("No users found.")
        return

    # Calculate the average
    average_age = total_age / count

    # Print result rounded to 2 decimal places
    print(f"Average age of users: {average_age:.2f}")


# This runs the script

if __name__ == "__main__":
    compute_average_age()
