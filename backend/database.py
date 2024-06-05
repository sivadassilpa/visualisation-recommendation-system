import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
        )
        print("Connected to PostgreSQL")
        return conn
    except psycopg2.Error as e:
        print("Error connecting to PostgreSQL:", e)


def close_connection(conn, cursor):
    cursor.close()
    conn.close()
    print("Connection to PostgreSQL closed")
