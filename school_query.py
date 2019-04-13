import csv, sqlite3

with sqlite3.connect('washington.db') as conn:
    cur = conn.cursor()
