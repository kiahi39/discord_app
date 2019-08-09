import os
import psycopg2
import datetime
import hashlib

print(os.environ['DATABASE_URL'])

def get_connection():
    dsn = os.environ.get('DATABASE_URL')
    return psycopg2.connect(dsn)

with get_connection() as conn:
    with conn.cursor() as cur:
        #cur.execute('CREATE TABLE LissText (id INTEGER NOT NULL, content TEXT NOT NULL, PRIMARY KEY(id));')
        
        #cur.execute('alter table LissText alter id type CHAR(4);')

        #cur.execute('DELETE FROM LissText;')
        
        #cur.execute('INSERT INTO LissText (id, content) VALUES (%s, %s)', (id0, m))
    
        #cur.execute('CREATE TABLE LissWard (discord_id TEXT NOT NULL, summoner_name TEXT NOT NULL, wards INTEGER DEFAULT 0, PRIMARY KEY(discord_id));')
        #cur.execute('ALTER TABLE LissWard ADD COLUMN last_match_id text;')

        #cur.execute('CREATE TABLE LissTime (discord_id TEXT NOT NULL, content INTEGER NOT NULL, PRIMARY KEY(discord_id));')
        
        
        cur.execute("SELECT * FROM LissWard;")
        for row in cur:
            #row = cur.fetchone()
            print(row)


    conn.commit()



