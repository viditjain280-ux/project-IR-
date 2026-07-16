from PyPDF2 import PdfFileReader
reader = PdfFileReader("sample.pdf")
print("Number of pages:", len(reader.pages))
page = reader.pages[0]
print("page.extract_text()")
