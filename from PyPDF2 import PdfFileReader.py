from PyPDF2 import PdfFileReader
reader = PdfFileReader("sample1.pdf")
print("Number of pages:", len(reader.pages))
page = reader.pages[0]
text = page.extract_text()
print("\ncontent of pdf:\n")
print(text)
