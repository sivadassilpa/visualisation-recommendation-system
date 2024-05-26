import psycopg2

DB_NAME = 'visualisation'
DB_USER = 'postgres'
DB_PASSWORD = 'Silpa@123'
DB_HOST = 'localhost'
DB_PORT = '5432'

def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        print("Connected to PostgreSQL")
        return conn
    except psycopg2.Error as e:
        print("Error connecting to PostgreSQL:", e)

def close_connection(conn, cursor):
    cursor.close()
    conn.close()
    print("Connection to PostgreSQL closed")
