import sqlite3

connection = sqlite3.connect("pdf_database.db")
cursor = connection.cursor()

cursor.execute("SELECT pdf_data FROM pdf_files WHERE id=1")

data = cursor.fetchone()[0]

with open("output.pdf","wb") as file:
    file.write(data)

connection.close()

print("PDF Retrieved Successfully!")