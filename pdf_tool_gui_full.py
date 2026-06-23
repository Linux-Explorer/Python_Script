import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PyPDF2 import PdfReader, PdfWriter
from pdf2docx import Converter
from reportlab.pdfgen import canvas

# -----------------------------
# Helper Function
# -----------------------------
def create_output_folder(pdf_path):
    base_dir = os.path.dirname(pdf_path)
    output_folder = os.path.join(base_dir, "PDF_Output")
    os.makedirs(output_folder, exist_ok=True)
    return output_folder

# -----------------------------
# Select PDF
# -----------------------------
def select_pdf():
    file = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file:
        selected_file.set(file)

# -----------------------------
# Split PDF
# -----------------------------
def split_pdf():
    pdf_file = selected_file.get()
    if not pdf_file:
        messagebox.showerror("Error", "Please select a PDF file first.")
        return

    reader = PdfReader(pdf_file)
    total_pages = len(reader.pages)
    output_folder = create_output_folder(pdf_file)
    file_name = os.path.splitext(os.path.basename(pdf_file))[0]

    option = simpledialog.askstring(
        "Split Option",
        "Choose Split Option:\n"
        "1 - Range (1-6)\n"
        "2 - Specific Pages (2,4,7)\n"
        "3 - Split All\n"
        "4 - Every N Pages"
    )

    if option == "1":
        page_range = simpledialog.askstring("Range", "Enter range (Example: 1-6)")
        start, end = map(int, page_range.split("-"))

        writer = PdfWriter()
        for i in range(start - 1, end):
            writer.add_page(reader.pages[i])

        output_path = os.path.join(output_folder, f"{file_name}_pages_{start}_to_{end}.pdf")
        with open(output_path, "wb") as f:
            writer.write(f)

    elif option == "2":
        pages = simpledialog.askstring("Pages", "Enter pages (Example: 2,4,7)")
        page_numbers = [int(p.strip()) - 1 for p in pages.split(",")]

        writer = PdfWriter()
        for page_num in page_numbers:
            writer.add_page(reader.pages[page_num])

        output_path = os.path.join(output_folder, f"{file_name}_selected_pages.pdf")
        with open(output_path, "wb") as f:
            writer.write(f)

    elif option == "3":
        for i in range(total_pages):
            writer = PdfWriter()
            writer.add_page(reader.pages[i])

            output_path = os.path.join(output_folder, f"{file_name}_page_{i+1}.pdf")
            with open(output_path, "wb") as f:
                writer.write(f)

    elif option == "4":
        n = int(simpledialog.askstring("Split Every N", "Enter number of pages per file:"))

        for i in range(0, total_pages, n):
            writer = PdfWriter()
            for j in range(i, min(i + n, total_pages)):
                writer.add_page(reader.pages[j])

            output_path = os.path.join(
                output_folder,
                f"{file_name}_pages_{i+1}_to_{min(i+n, total_pages)}.pdf"
            )

            with open(output_path, "wb") as f:
                writer.write(f)

    else:
        messagebox.showerror("Error", "Invalid option selected.")
        return

    messagebox.showinfo("Success", f"Split completed!\nSaved in:\n{output_folder}")

# -----------------------------
# Compress PDF
# -----------------------------
def compress_pdf():
    pdf_file = selected_file.get()
    if not pdf_file:
        messagebox.showerror("Error", "Please select a PDF file first.")
        return

    reader = PdfReader(pdf_file)
    writer = PdfWriter()
    output_folder = create_output_folder(pdf_file)
    file_name = os.path.splitext(os.path.basename(pdf_file))[0]

    for page in reader.pages:
        page.compress_content_streams()
        writer.add_page(page)

    output_path = os.path.join(output_folder, f"{file_name}_compressed.pdf")

    with open(output_path, "wb") as f:
        writer.write(f)

    messagebox.showinfo("Success", f"Compressed file saved in:\n{output_path}")

# -----------------------------
# PDF to Word
# -----------------------------
def pdf_to_word():
    pdf_file = selected_file.get()
    if not pdf_file:
        messagebox.showerror("Error", "Please select a PDF file first.")
        return

    output_folder = create_output_folder(pdf_file)
    file_name = os.path.splitext(os.path.basename(pdf_file))[0]
    output_path = os.path.join(output_folder, f"{file_name}.docx")

    cv = Converter(pdf_file)
    cv.convert(output_path)
    cv.close()

    messagebox.showinfo("Success", f"Word file saved in:\n{output_path}")

# -----------------------------
# Edit PDF
# -----------------------------
def edit_pdf():
    pdf_file = selected_file.get()
    if not pdf_file:
        messagebox.showerror("Error", "Please select a PDF file first.")
        return

    text = simpledialog.askstring("Add Text", "Enter text to add on first page:")

    reader = PdfReader(pdf_file)
    writer = PdfWriter()
    output_folder = create_output_folder(pdf_file)
    file_name = os.path.splitext(os.path.basename(pdf_file))[0]

    overlay_path = os.path.join(output_folder, "temp_overlay.pdf")
    c = canvas.Canvas(overlay_path)
    c.drawString(100, 750, text)
    c.save()

    overlay_reader = PdfReader(overlay_path)

    first_page = reader.pages[0]
    first_page.merge_page(overlay_reader.pages[0])
    writer.add_page(first_page)

    for i in range(1, len(reader.pages)):
        writer.add_page(reader.pages[i])

    output_path = os.path.join(output_folder, f"{file_name}_edited.pdf")

    with open(output_path, "wb") as f:
        writer.write(f)

    os.remove(overlay_path)

    messagebox.showinfo("Success", f"Edited file saved in:\n{output_path}")

# -----------------------------
# GUI Layout
# -----------------------------
app = tk.Tk()
app.title("Professional PDF Tool")
app.geometry("450x350")
app.resizable(False, False)

selected_file = tk.StringVar()

tk.Label(app, text="Selected PDF:", font=("Arial", 10)).pack(pady=5)
tk.Entry(app, textvariable=selected_file, width=50).pack()

tk.Button(app, text="Browse PDF", command=select_pdf, width=20).pack(pady=10)

tk.Button(app, text="Split PDF", command=split_pdf, width=25).pack(pady=5)
tk.Button(app, text="Compress PDF", command=compress_pdf, width=25).pack(pady=5)
tk.Button(app, text="Convert PDF to Word", command=pdf_to_word, width=25).pack(pady=5)
tk.Button(app, text="Edit PDF (Add Text)", command=edit_pdf, width=25).pack(pady=5)

tk.Button(app, text="Exit", command=app.quit, width=15, bg="red", fg="white").pack(pady=15)

app.mainloop()