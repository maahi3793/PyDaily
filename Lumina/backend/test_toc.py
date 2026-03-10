import sqlite3
import fitz

conn = sqlite3.connect('lumilearn.db')
c = conn.cursor()
c.execute("select id, filename from books order by id desc limit 1")
row = c.fetchone()
if not row: exit()

book_id, filename = row
pdf_path = f"C:/Users/reach/.gemini/antigravity/scratch/relaunchpython/Lumina/backend/uploads/{filename}"

doc = fitz.open(pdf_path)
toc = doc.get_toc()
print(f"TOC entries: {len(toc)}")
for item in toc[:15]:
    print(item)
