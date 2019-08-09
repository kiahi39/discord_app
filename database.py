
import os
import psycopg2
import hashlib

def get_connection():
    dsn = os.environ.get('DATABASE_URL')
    return psycopg2.connect(dsn)

def insert(sql_str, input_tuple):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql_str, input_tuple)
        conn.commit()

def execute(sql_str, input_tuple):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql_str, input_tuple)