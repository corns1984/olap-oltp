import sqlite3
import sys

if len(sys.argv) != 3:
    print('Usage: python3 sql.py DATABASE "SQL QUERY"')
    raise SystemExit(2)

db, query = sys.argv[1], sys.argv[2]
conn = sqlite3.connect(db)
conn.execute("PRAGMA foreign_keys = ON")

try:
    cursor = conn.execute(query)
    if cursor.description:
        columns = [col[0] for col in cursor.description]
        print(" | ".join(columns))
        for row in cursor.fetchall():
            print(" | ".join(str(value) for value in row))
    else:
        conn.commit()
        print(f"Query executed; rows affected: {cursor.rowcount}")
except sqlite3.Error as exc:
    print(f"SQL ERROR: {exc}")
    raise SystemExit(1)
finally:
    conn.close()
