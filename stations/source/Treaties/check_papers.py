import psycopg
conn = psycopg.connect("postgresql://root:POSTGRES_PASSWORD@POSTGRES_HOST:POSTGRES_PORT/treaties")
cur = conn.cursor()
cur.execute("SELECT id, title, length(full_text) as chars FROM papers ORDER BY id")
rows = cur.fetchall()
if rows:
    for r in rows:
        print(f"  ID={r[0]}  title={r[1]}  chars={r[2]}")
else:
    print("No papers in database")
cur.close()
conn.close()
