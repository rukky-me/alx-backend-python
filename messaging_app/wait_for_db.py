import time
import sys
import MySQLdb
import os

host = os.getenv("MYSQL_HOST", "db")
user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")
database = os.getenv("MYSQL_DATABASE")
port = int(os.getenv("MYSQL_PORT", 3306))

while True:
    try:
        conn = MySQLdb.connect(
            host=host,
            user=user,
            passwd=password,
            db=database,
            port=port,
        )
        conn.close()
        print("Database is ready!")
        break
    except MySQLdb.OperationalError:
        print("Waiting for database...")
        time.sleep(2)
