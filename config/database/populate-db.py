import os
import pandas as pd
import contextlib
import sqlite3


# MAIN
malenames = "data/malenames.csv"
femalenames = "data/femalenames.csv"
surnames = "data/surnames.csv"

if not (os.path.exists(malenames) or os.path.exists(femalenames) or os.path.exists(surnames)):
    print('name database does not exist')
    exit(1)

malenames = pd.read_csv(malenames)
femalenames = pd.read_csv(femalenames)
surnames = pd.read_csv(surnames)

with sqlite3.connect("names.db") as conn:
    conn.execute("PRAGMA busy_timeout = 30000")
    conn.row_factory = sqlite3.Row
    urls_to_exclude = set()

    with contextlib.closing(conn.cursor()) as curs:
        for i, row in malenames.iterrows():
            curs.execute("INSERT INTO malenames VALUES (?)", (row[0],))
        for i, row in femalenames.iterrows():
            curs.execute("INSERT INTO femalenames VALUES (?)", (row[0],))
        for i, row in surnames.iterrows():
            curs.execute("INSERT INTO surnames VALUES (?)", (row[0],))

print("Populated DB")