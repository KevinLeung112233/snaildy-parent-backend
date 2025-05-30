# db_checker.py
import os
import time
import psycopg2
from psycopg2 import OperationalError


def check_db_connection():
    dbname = os.getenv('DATABASE_NAME', 'snaildy-parent-db')
    user = os.getenv('DATABASE_USER', 'kevinleung')
    password = os.getenv('DATABASE_PASSWORD', 'Snaildy2025!D')
    host = os.getenv('DATABASE_HOST', 'db')
    port = os.getenv('DATABASE_PORT', '5432')

    while True:
        try:
            conn = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
            conn.close()
            print("Database is ready!")
            return True
        except OperationalError:
            print("Database not ready, waiting...")
            time.sleep(1)


if __name__ == "__main__":
    check_db_connection()
