import os
import psycopg2
import datetime
import hashlib

print(os.environ['DATABASE_URL'])

def get_connection():
    dsn = os.environ.get('DATABASE_URL')
    return psycopg2.connect(dsn)

def hash4(dat):
    hs = hashlib.md5(dat.encode()).hexdigest()
    hs = hs[:4]
    return hs


text = [
            "{0}は{1}の間 氷漬けにされていました.",
            "{0}は{1}間ずっと狂ったようにモンスターを狩り続けていました.",
            "{0}は{1}の時間を有意義に過ごしました.",
            "{0}は{1}間の記憶がないようです.",
            "{0}は{1}前まで元気でした.",
            "{0}は右クリックを夢中で押していただけなのに{1}が経過していました.",
            "{0}は睡眠時間を{1}失いました.",
            "{0}は{1} なにも食べていません.",
            "{0}が静かになるまで{1}かかりました.",
            "{0}は{1}も勉強してえらい.",
            "{0}が{1}ずっと部屋から出てきません.",
            
        ]

with get_connection() as conn:
    with conn.cursor() as cur:
        #cur.execute('CREATE TABLE LissText (id INTEGER NOT NULL, content TEXT NOT NULL, PRIMARY KEY(id));')
        
        #cur.execute('alter table LissText alter id type CHAR(4);')

        #cur.execute('DELETE FROM LissText;')
        for m in text:
            id0 = hash4(datetime.datetime.now().strftime('%Y/%m/%d/%H:%M:%S'))
            cur.execute('INSERT INTO LissText (id, content) VALUES (%s, %s)', (id0, m))
    

        '''
        cur.execute("SELECT * FROM LissText;")
        row = cur.fetchone()
        print(row)
        '''

    conn.commit()



