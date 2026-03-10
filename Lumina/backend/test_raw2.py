import sqlite3
import re

conn = sqlite3.connect('lumilearn.db')
c = conn.cursor()
c.execute("select id from books order by id desc limit 1")
row = c.fetchone()
if not row:
    print("No books")
    exit(0)
book_id = row[0]
c.execute("select content from chapters where book_id=?", (book_id,))
text = ""
for row in c.fetchall():
    text += row[0] + "\n"

print("Searching for Chapter 2...")
matches = re.finditer(r'.{0,50}chapter 2.{0,50}', text, re.IGNORECASE)
for m in matches:
    print(repr(m.group(0)))

print("\nSearching for large numbers like '2\\n'...")
matches2 = re.finditer(r'\n2\n.{0,50}', text)
for m in matches2:
    print(repr(m.group(0)))
