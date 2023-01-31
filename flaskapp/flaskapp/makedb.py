import csv
import sqlite3

conn = sqlite3.connect('database.db')

with open('schema.sql') as f:
    conn.executescript(f.read())

cur = conn.cursor()
"""cur.execute("INSERT INTO users (username, password, firstname, lastname, email) VALUES (?, ?, ?, ?, ?)", ('sample_username', 'sample@pa$$word', 'sample_first', 'sample_last', 'sample@email.com'))
"""
conn.commit()
conn.close()
