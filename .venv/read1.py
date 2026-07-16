from PyPDF2 import PdfReader , PdfWriter

reader = PdfReader("sample1.pdf")
print(f"Pages: {len(reader.pages)}")
print(reader.pages[0].extract_text())

# ---- WRITE (copy pages + add a blank page) ----
writer = PdfWriter()
for page in reader.pages:
    writer.add_page(page)
writer.add_blank_page(width=612, height=792)

with open("output.pdf", "wb") as f:
    writer.write(f)
