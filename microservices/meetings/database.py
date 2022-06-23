from dotenv import load_dotenv
import os

import psycopg2
load_dotenv()

def create_server_connection():
    connection = None
    try:
        connection = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            database=os.getenv("POSTGRES_DATABASE"), 
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            port=os.getenv("POSTGRES_PORT")
        )
        print("PostgresSQL Database connection successful")
    except (Exception, psycopg2.DatabaseError) as err:
        print(f"Error: '{err}'")

    return connection

def create_tables(conn):
    try:
        query = """
            CREATE TABLE IF NOT EXISTS meetings ( 
                id serial PRIMARY KEY, 
                name VARCHAR(255) UNIQUE NOT NULL, 
                category_id INTEGER, 
                category_name VARCHAR(255), 
                participants_username VARCHAR(255) ARRAY, 
                duration_min INTEGER, 
                event_time TIMESTAMP NOT NULL 
            )
            """
        cursor = conn.cursor()
        cursor.execute(query)
        cursor.close()
        conn.commit()
        print("commited successfully")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()