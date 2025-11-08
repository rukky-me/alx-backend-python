#!/usr/bin/python3

import mysql.connector
from mysql.connector import Error
import csv
import uuid



"""
seed.py
This script connects to MySQL, creates a database and table, 
(optionally inserts CSV data), and uses a generator to stream rows one by one.
"""

# CONNECT TO MYSQL SERVER (without specifying any database)

def connect_db():
    """
    Connects to the MySQL server.
    Returns a connection object or None if connection fails.
    """
    try:
        conn = mysql.connector.connect(
            host="localhost",   # local MySQL server
            user="rukky",       # updated username
            password="" # updated password
        )
        print("Connected to MySQL server (no database).")
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


# CREATE DATABASE IF IT DOESN'T EXIST

def create_database(connection):
    """
    Creates the 'ALX_prodev' database if it does not exist.
    """
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
    connection.commit()
    print("Database 'ALX_prodev' created or already exists.")
    cursor.close()


# CONNECT TO SPECIFIC DATABASE (ALX_prodev)

def connect_to_prodev():
    """
    Connects to the ALX_prodev database.
    """
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="rukky",        # updated username
            password="",# updated password
            database="ALX_prodev"
        )
        print("Connected to ALX_prodev database.")
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# CREATE TABLE user_data IF NOT EXISTS

def create_table(connection):
    """
    Creates a 'user_data' table if it doesn't exist already.
    """
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            age DECIMAL NOT NULL
        );
    """)
    connection.commit()
    print("Table 'user_data' created successfully.")
    cursor.close()



# INSERT DATA FROM CSV FILE INTO THE TABLE

def insert_data(connection, csv_file):
    """
    Reads data from a CSV file and inserts it into user_data table.
    Uses INSERT IGNORE to avoid duplicate entries.
    """
    cursor = connection.cursor()
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cursor.execute("""
                INSERT IGNORE INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s);
            """, (row['user_id'], row['name'], row['email'], row['age']))
    connection.commit()
    print("Data inserted successfully from CSV.")
    cursor.close()



# GENERATOR FUNCTION TO STREAM USERS ONE BY ONE

def stream_users(connection):
    """
    A generator that fetches rows from user_data table one at a time.
    Useful for handling large datasets without using too much memory.
    """
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data;")

    for row in cursor:
        yield row

    cursor.close()



# MAIN EXECUTION FLOW

if __name__ == "__main__":
    print("🔌 Connecting to MySQL...")
    conn = connect_db()
    if conn:
        create_database(conn)
        conn.close()

    print("Connecting to ALX_prodev...")
    conn = connect_to_prodev()
    if conn:
        create_table(conn)
        
        print("Streaming rows from user_data:")
        for user in stream_users(conn):
            print(user)
        
        conn.close()
        print("Done! All tasks completed successfully.")
