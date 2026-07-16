import sqlite3
from PyPDF2 import PdfReader

connection = sqlite3.connect("pdf_database.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS pdf_details(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_name TEXT,
    total_pages INTEGER,
    title TEXT,
    author TEXT
)
""")


reader = PdfReader("sample1.pdf")


pages = len(reader.pages)

metadata = reader.metadata

title = metadata.title if metadata.title else "Not Available"
author = metadata.author if metadata.author else "Not Available"


cursor.execute("""
INSERT INTO pdf_details(file_name,total_pages,title,author)
VALUES(?,?,?,?)
""", ("sample.pdf", pages, title, author))

connection.commit()


cursor.execute("SELECT * FROM pdf_details")

records = cursor.fetchall()

print("\nPDF Information Stored in Database\n")

for row in records:
    print(row)

connection.close()

