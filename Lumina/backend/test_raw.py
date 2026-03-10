import sqlite3
import re

conn = sqlite3.connect('lumilearn.db')
c = conn.cursor()
c.execute("select id from books order by id desc limit 1")
row = c.fetchone()
if not row:
    print("No books")
    exit()

book_id = row[0]
c.execute("select content from chapters where book_id=? order by chapter_number asc limit 3", (book_id,))
for row in c.fetchall():
    print(repr(row[0][:1000]))
    print("---")
