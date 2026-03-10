import sqlite3
import re

conn = sqlite3.connect('lumilearn.db')
c = conn.cursor()
c.execute("select id from books order by id desc limit 1")
row = c.fetchone()
if not row:
    exit()

book_id = row[0]
c.execute("select content from chapters where book_id=?", (book_id,))
text = ""
for row in c.fetchall():
    text += row[0] + "\n"

matches = re.finditer(r'.{0,50}chapter\s+2.{0,50}', text, re.IGNORECASE)
with open("test_out.utf8.txt", "w", encoding="utf-8") as f:
    for m in matches:
        f.write(repr(m.group(0)) + "\n")

    f.write("\n\nAlso looking for just '2\\n' or similar structure near 'Variables':\n")
    matches2 = re.finditer(r'.{0,50}Variables and Simple Data Types.{0,50}', text, re.IGNORECASE)
    for m in matches2:
        f.write(repr(m.group(0)) + "\n")
