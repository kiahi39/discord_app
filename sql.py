import os
import psycopg2

print(os.environ['DATABASE_URL'])

def get_connection():
    dsn = os.environ.get('DATABASE_URL')
    return psycopg2.connect(dsn)


with get_connection() as conn:
    with conn.cursor() as cur:
        #cur.execute('CREATE TABLE LissText (id INTEGER NOT NULL, content TEXT NOT NULL, PRIMARY KEY(id));')
        
        #cur.execute('alter table LissText alter id type CHAR(4);')

        #cur.execute('DELETE FROM LissText;')

        cur.execute("SELECT * FROM LissText;")
        row = cur.fetchone()
        print(row)
