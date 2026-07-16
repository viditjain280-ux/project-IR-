import sqlite3

# Connect Database
connection = sqlite3.connect("pdf_database.db")
cursor = connection.cursor()

# Create Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS pdf_files(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_name TEXT,
    pdf_data BLOB
)
""")

# Read PDF as Binary
with open("sample1.pdf", "rb") as file:
    pdf = file.read()

# Insert PDF
cursor.execute(
    "INSERT INTO pdf_files(file_name,pdf_data) VALUES(?,?)",
    ("sample.pdf", pdf)
)

connection.commit()
connection.close()

print("PDF Stored Successfully!")