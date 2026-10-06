import os
import psycopg2


def connect_to_database():
    try:
        connection = psycopg2.connect(
            dbname=os.getenv("DB_NAME", "tempDB"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"),
        )
        return connection
    except psycopg2.Error as exc:
        print("Database connection failed:", exc)
        return None
