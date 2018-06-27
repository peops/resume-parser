import contextlib
import sqlite3
import argparse

#MAIN
parser = argparse.ArgumentParser('Setup a database to store name data')
parser.add_argument('path_to_crawl_db', help='Path to the database used to store names, e.g names.db')

args = parser.parse_args()

with sqlite3.connect(args.path_to_crawl_db) as conn:
    with contextlib.closing(conn.cursor()) as curs:
        curs.execute("CREATE TABLE IF NOT EXISTS malenames (name TEXT PRIMARY KEY ON CONFLICT IGNORE)")
        curs.execute("CREATE TABLE IF NOT EXISTS femalenames (name TEXT PRIMARY KEY ON CONFLICT IGNORE)")
        curs.execute("CREATE TABLE IF NOT EXISTS surnames (name TEXT PRIMARY KEY ON CONFLICT IGNORE)")
        curs.execute("CREATE TABLE IF NOT EXISTS locations (location TEXT PRIMARY KEY ON CONFLICT IGNORE)")
        conn.commit()
