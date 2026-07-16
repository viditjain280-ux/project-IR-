from PyPDF2 import PdfReader

reader = PdfReader("output.pdf")

print("Number of Pages:", len(reader.pages))

print("\nMetadata")
print(reader.metadata)

print("\nPage Information")

for i, page in enumerate(reader.pages):
    print("------------------------")
    print("Page:", i+1)
    print("Width :", page.mediabox.width)
    print("Height:", page.mediabox.height)

    text = page.extract_text()

    if text:
        print("Contains Text : Yes")
        print("Characters :", len(text))
    else:
        print("Contains Text : No")