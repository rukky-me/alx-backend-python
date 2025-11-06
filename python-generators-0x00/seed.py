import mysql.connector
from mysql.connector import Error
import csv
import uuid


#This conects to MYSQL to the server
def connect_db():
    """
    Connects to the MySQL server (not a specific database yet).
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password"
        )
        if connection.is_connected():
            print("Connected to MySQL server")
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None


#This creates database if it does not already exist
def create_database(connection):
    """
    Creates the database ALX_prodev if it does not exist.
    """
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        print("Database 'ALX_prodev' ensured to exist.")
    except Error as e:
        print(f"Error creating database: {e}")


#This connects to ALX_prodev DATABASE

def connect_to_prodev():
    """
    Connects directly to the ALX_prodev database.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",
            database="ALX_prodev"
        )
        if connection.is_connected():
            print("Connected to 'ALX_prodev' database.")
            return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev: {e}")
        return None


#CREATE user_data TABLE

def create_table(connection):
    """
    Creates the user_data table if it does not exist.
    """
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                age DECIMAL(3, 0) NOT NULL,
                INDEX (user_id)
            );
        """)
        connection.commit()
        print("Table 'user_data' ensured to exist.")
    except Error as e:
        print(f"Error creating table: {e}")



#INSERT DATA FROM CSV

def insert_data(connection, csv_file_path):
    """
    Inserts data from CSV file into the user_data table if not already present.
    """
    try:
        cursor = connection.cursor()
        with open(csv_file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                user_id = str(uuid.uuid4())
                cursor.execute("""
                    INSERT IGNORE INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, row["name"], row["email"], row["age"]))
        connection.commit()
        print("Data inserted successfully from CSV.")
    except Error as e:
        print(f"Error inserting data: {e}")


# GENERATOR TO STREAM ROWS

def stream_user_data(connection):
    """
    Generator that streams user rows one by one.
    """
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data;")
        for row in cursor:
            yield row  # Yield one row at a time (memory-efficient)
    except Error as e:
        print(f"Error streaming data: {e}")


#This is the MAIN execution, it streams user data 

if __name__ == "__main__":
    # Step 1: Connect to MySQL server
    conn = connect_db()

    if conn:
        # Step 2: Create database
        create_database(conn)
        conn.close()

        # Step 3: Connect to ALX_prodev DB
        db_conn = connect_to_prodev()

        # Step 4: Create table
        create_table(db_conn)

        # Step 5: Insert CSV data (path to your CSV file)
        insert_data(db_conn, "user_data.csv")

        # Step 6: Use generator to stream data
        print("\n--- Streaming user data row by row ---")
        for user in stream_user_data(db_conn):
            print(user)

        db_conn.close()
