import psycopg2
import database as db

with db.get_connection() as conn:
    with conn.cursor() as cur:
        cur.execute('SELECT EXISTS(SELECT summoner_name FROM LissWard WHERE discord_id = %s);', (str(188650510205714433), ))
        print(cur)
        for row in cur:
            print(row[0])

        cur.execute('SELECT summoner_name FROM LissWard WHERE discord_id = %s;', (str(188650510205714434), ))
        print(cur)
        for row in cur:
            print(row is None)