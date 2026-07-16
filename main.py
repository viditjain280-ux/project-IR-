import tkinter as tk
from tkinter import filedialog, messagebox
import sqlite3
from PyPDF2 import PdfReader
import tempfile
import os


window = tk.Tk()
window.title("PDF Analyzer using SQLite")
window.geometry("900x650")
window.resizable(False, False)


connection = sqlite3.connect("pdf_database.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS pdf_files(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    file_name TEXT,

    pdf_data BLOB

)

""")

connection.commit()


selected_file = ""


title = tk.Label(
    window,
    text="PDF ANALYZER",
    font=("Arial",20,"bold","underline"),
    fg="darkblue"
)

title.pack(pady=10)


file_label = tk.Label(

    window,

    text="No PDF Selected",

    font=("Arial",11),

    fg="red"

)

file_label.pack()


result_box = tk.Text(

    window,

    width=105,

    height=24,

    font=("Consolas",10)

)

result_box.pack(pady=15)



def choose_pdf():

    global selected_file

    selected_file = filedialog.askopenfilename(

        filetypes=[("PDF Files","*.pdf")]

    )

    if selected_file:

        file_label.config(

            text=selected_file,

            fg="black"

        )


def store_pdf():

    global selected_file

    if selected_file == "":

        messagebox.showerror(

            "Error",

            "Please Select a PDF First"

        )

        return

    with open(selected_file,"rb") as file:

        pdf = file.read()

    cursor.execute(

        """

        INSERT INTO pdf_files(file_name,pdf_data)

        VALUES(?,?)

        """,

        (

            os.path.basename(selected_file),

            pdf

        )

    )

    connection.commit()

    messagebox.showinfo(

        "Success",

        "PDF Stored Successfully in SQLite Database"

    )


def retrieve_pdf():

    cursor.execute("""

    SELECT pdf_data

    FROM pdf_files

    ORDER BY id DESC

    LIMIT 1

    """)

    data = cursor.fetchone()

    if data is None:

        return None

    temp = tempfile.NamedTemporaryFile(

        delete=False,

        suffix=".pdf"

    )

    temp.write(data[0])

    temp.close()

    return temp.name


def display_content():

    path = retrieve_pdf()

    if path is None:

        messagebox.showerror(

            "Error",

            "Database is Empty"

        )

        return

    result_box.delete(1.0,tk.END)

    result_box.insert(

        tk.END,

        "=========== PDF CONTENT ===========\n\n"

    )

    reader = PdfReader(path)

    page_number = 1

    for page in reader.pages:

        result_box.insert(

            tk.END,

            f"\n------------ PAGE {page_number} ------------\n\n"

        )

        text = page.extract_text()

        if text:

            result_box.insert(

                tk.END,

                text

            )

        else:

            result_box.insert(

                tk.END,

                "No Text Found"

            )

        result_box.insert(

            tk.END,

            "\n\n"

        )

        page_number += 1

    os.remove(path)

def analyze_pdf():

    path = retrieve_pdf()

    if path is None:

        messagebox.showerror(
            "Error",
            "Database is Empty"
        )

        return

    result_box.delete(1.0, tk.END)

    reader = PdfReader(path)

    metadata = reader.metadata

    result_box.insert(
        tk.END,
        "=========== PDF STRUCTURE ===========\n\n"
    )

    result_box.insert(
        tk.END,
        f"Total Pages : {len(reader.pages)}\n\n"
    )


    title = metadata.title if metadata and metadata.title else "Not Available"
    author = metadata.author if metadata and metadata.author else "Not Available"

    producer = (
        metadata.get("/Producer", "Not Available")
        if metadata else "Not Available"
    )

    creator = (
        metadata.get("/Creator", "Not Available")
        if metadata else "Not Available"
    )

    result_box.insert(tk.END, f"Title    : {title}\n")
    result_box.insert(tk.END, f"Author   : {author}\n")
    result_box.insert(tk.END, f"Producer : {producer}\n")
    result_box.insert(tk.END, f"Creator  : {creator}\n\n")

    result_box.insert(
        tk.END,
        "=============================================\n\n"
    )


    for i, page in enumerate(reader.pages):

        result_box.insert(
            tk.END,
            f"Page Number : {i+1}\n"
        )

        result_box.insert(
            tk.END,
            f"Width  : {page.mediabox.width}\n"
        )

        result_box.insert(
            tk.END,
            f"Height : {page.mediabox.height}\n"
        )

        text = page.extract_text()

        if text:

            result_box.insert(
                tk.END,
                "Contains Text : Yes\n"
            )

            result_box.insert(
                tk.END,
                f"Characters    : {len(text)}\n"
            )

        else:

            result_box.insert(
                tk.END,
                "Contains Text : No\n"
            )

            result_box.insert(
                tk.END,
                "Characters    : 0\n"
            )

        result_box.insert(
            tk.END,
            "---------------------------------------------\n"
        )

    os.remove(path)
def close_application():

    connection.close()

    window.destroy()

close_button = tk.Button(
    window,
    text="Close",
    bg="red",
    fg="white",
    command=close_application
)

close_button.place(x=800, y=600)

button_frame = tk.Frame(window)

button_frame.pack(pady=10)
choose_button = tk.Button(
    button_frame,
    text="Choose PDF",
    width=18,
    bg="lightblue",
    command=choose_pdf
)

choose_button.pack(side=tk.LEFT, padx=5)

store_button = tk.Button(
    button_frame,
    text="Store PDF",
    width=18,
    bg="lightgreen",
    command=store_pdf
)

store_button.pack(side=tk.LEFT, padx=5)


display_button = tk.Button(
    button_frame,
    text="Display PDF Content",
    width=18,
    bg="lightyellow",
    command=display_content
)

display_button.pack(side=tk.LEFT, padx=5)

analyze_button = tk.Button(
    button_frame,
    text="Analyze PDF Structure",
    width=18,
    bg="orange",
    command=analyze_pdf
)

analyze_button.pack(side=tk.LEFT, padx=5)


def close_application():

    connection.close()

    window.destroy()

window.protocol(
    "WM_DELETE_WINDOW",
    close_application
)

window.mainloop()