import os
import tkinter as tk
from tkinter import filedialog
from PyPDF2 import PdfReader, PdfWriter
from pdf2docx import Converter
from reportlab.pdfgen import canvas

# ================= INITIAL SETUP =================
root = tk.Tk()
root.withdraw()

print("📂 Select Main PDF File...")
pdf_file = filedialog.askopenfilename(
    title="Select PDF File",
    filetypes=[("PDF Files", "*.pdf")]
)

if not pdf_file:
    print("❌ No file selected.")
    exit()

file_name = os.path.splitext(os.path.basename(pdf_file))[0]


# ================= SAVE DIALOG FUNCTION =================
def get_save_path(default_name, extension):
    save_path = filedialog.asksaveasfilename(
        title="Save As",
        defaultextension=extension,
        initialfile=default_name,
        filetypes=[
            ("PDF Files", "*.pdf"),
            ("Word Files", "*.docx")
        ]
    )
    return save_path


# ================= MENU =================
print("\n========= PROFESSIONAL PDF TOOLKIT =========")
print("1. Split PDF")
print("2. Compress PDF")
print("3. Convert PDF to Word")
print("4. Edit PDF (Add Text)")
print("5. Merge Two PDFs")
print("6. Merge Multiple PDFs")
print("7. Merge All PDFs in Folder")
print("8. Exit")

choice = input("Enter choice (1-8): ")

# ============================================================
# ===================== SPLIT ================================
# ============================================================

if choice == "1":
    reader = PdfReader(pdf_file)
    total_pages = len(reader.pages)

    print(f"Total Pages: {total_pages}")
    start, end = map(int, input("Enter range (1-5): ").split("-"))

    writer = PdfWriter()
    for i in range(start - 1, end):
        writer.add_page(reader.pages[i])

    output_path = get_save_path(f"{file_name}_split", ".pdf")
    if not output_path:
        print("❌ Save cancelled.")
        exit()

    with open(output_path, "wb") as f:
        writer.write(f)

    print(f"✅ File saved at:\n{output_path}")

# ============================================================
# ===================== COMPRESS =============================
# ============================================================

elif choice == "2":
    reader = PdfReader(pdf_file)
    writer = PdfWriter()

    for page in reader.pages:
        page.compress_content_streams()
        writer.add_page(page)

    output_path = get_save_path(f"{file_name}_compressed", ".pdf")
    if not output_path:
        print("❌ Save cancelled.")
        exit()

    with open(output_path, "wb") as f:
        writer.write(f)

    print(f"✅ File saved at:\n{output_path}")

# ============================================================
# ===================== PDF TO WORD ==========================
# ============================================================

elif choice == "3":
    output_path = get_save_path(f"{file_name}", ".docx")
    if not output_path:
        print("❌ Save cancelled.")
        exit()

    cv = Converter(pdf_file)
    cv.convert(output_path)
    cv.close()

    print(f"✅ Word file saved at:\n{output_path}")

# ============================================================
# ===================== EDIT PDF =============================
# ============================================================

elif choice == "4":
    text = input("Enter text to add: ")

    reader = PdfReader(pdf_file)
    writer = PdfWriter()

    temp_overlay = "temp_overlay.pdf"
    c = canvas.Canvas(temp_overlay)
    c.drawString(100, 750, text)
    c.save()

    overlay_reader = PdfReader(temp_overlay)

    first_page = reader.pages[0]
    first_page.merge_page(overlay_reader.pages[0])
    writer.add_page(first_page)

    for i in range(1, len(reader.pages)):
        writer.add_page(reader.pages[i])

    output_path = get_save_path(f"{file_name}_edited", ".pdf")
    if not output_path:
        os.remove(temp_overlay)
        print("❌ Save cancelled.")
        exit()

    with open(output_path, "wb") as f:
        writer.write(f)

    os.remove(temp_overlay)

    print(f"✅ File saved at:\n{output_path}")

# ============================================================
# ===================== MERGE TWO ============================
# ============================================================

elif choice == "5":
    print("📂 Select Second PDF...")
    second_pdf = filedialog.askopenfilename(
        title="Select Second PDF",
        filetypes=[("PDF Files", "*.pdf")]
    )

    if not second_pdf:
        print("❌ No second file selected.")
        exit()

    writer = PdfWriter()

    for page in PdfReader(pdf_file).pages:
        writer.add_page(page)

    for page in PdfReader(second_pdf).pages:
        writer.add_page(page)

    output_path = get_save_path("Merged_Two", ".pdf")
    if not output_path:
        print("❌ Save cancelled.")
        exit()

    with open(output_path, "wb") as f:
        writer.write(f)

    print(f"✅ File saved at:\n{output_path}")

# ============================================================
# ===================== MERGE MULTIPLE =======================
# ============================================================

elif choice == "6":
    print("📂 Select Multiple PDFs...")
    files = filedialog.askopenfilenames(
        title="Select PDFs",
        filetypes=[("PDF Files", "*.pdf")]
    )

    if not files:
        print("❌ No files selected.")
        exit()

    writer = PdfWriter()

    for file in files:
        for page in PdfReader(file).pages:
            writer.add_page(page)

    output_path = get_save_path("Merged_Multiple", ".pdf")
    if not output_path:
        print("❌ Save cancelled.")
        exit()

    with open(output_path, "wb") as f:
        writer.write(f)

    print(f"✅ File saved at:\n{output_path}")

# ============================================================
# ===================== MERGE FOLDER =========================
# ============================================================

elif choice == "7":
    print("📂 Select Folder...")
    folder = filedialog.askdirectory(title="Select Folder Containing PDFs")

    if not folder:
        print("❌ No folder selected.")
        exit()

    writer = PdfWriter()

    for file in sorted(os.listdir(folder)):
        if file.lower().endswith(".pdf"):
            full_path = os.path.join(folder, file)
            for page in PdfReader(full_path).pages:
                writer.add_page(page)

    output_path = get_save_path("Merged_Folder", ".pdf")
    if not output_path:
        print("❌ Save cancelled.")
        exit()

    with open(output_path, "wb") as f:
        writer.write(f)

    print(f"✅ File saved at:\n{output_path}")

# ============================================================

else:
    print("👋 Exiting Toolkit.")