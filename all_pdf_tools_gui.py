import os
import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PyPDF2 import PdfReader, PdfWriter
from pdf2docx import Converter
from docx2pdf import convert
from reportlab.pdfgen import canvas
from PIL import Image

# --------------------------
# CONFIG
# --------------------------
BG = "#1e1e1e"
FG = "white"
BTN = "#2d2d2d"
ACCENT = "#00c6ff"

def create_output(path):
    folder = os.path.join(os.path.dirname(path), "PDF_Output")
    os.makedirs(folder, exist_ok=True)
    return folder

# --------------------------
# FUNCTIONS
# --------------------------

def merge_pdf():
    files = filedialog.askopenfilenames(filetypes=[("PDF", "*.pdf")])
    if not files: return
    writer = PdfWriter()
    for file in files:
        reader = PdfReader(file)
        for page in reader.pages:
            writer.add_page(page)
    out = os.path.join(create_output(files[0]), "merged.pdf")
    with open(out, "wb") as f:
        writer.write(f)
    messagebox.showinfo("Done", f"Merged saved:\n{out}")

def split_pdf():
    file = filedialog.askopenfilename(filetypes=[("PDF", "*.pdf")])
    if not file: return
    reader = PdfReader(file)
    total = len(reader.pages)
    choice = simpledialog.askstring("Split",
        "1- Range\n2- Specific\n3- Split All")
    name = os.path.splitext(os.path.basename(file))[0]
    outfolder = create_output(file)

    if choice == "1":
        r = simpledialog.askstring("Range", "Example: 1-5")
        s,e = map(int,r.split("-"))
        writer = PdfWriter()
        for i in range(s-1,e):
            writer.add_page(reader.pages[i])
        out = os.path.join(outfolder,f"{name}_range.pdf")
        with open(out,"wb") as f: writer.write(f)

    elif choice == "2":
        p = simpledialog.askstring("Pages","2,4,6")
        writer = PdfWriter()
        for x in p.split(","):
            writer.add_page(reader.pages[int(x.strip())-1])
        out = os.path.join(outfolder,f"{name}_selected.pdf")
        with open(out,"wb") as f: writer.write(f)

    elif choice == "3":
        for i in range(total):
            writer = PdfWriter()
            writer.add_page(reader.pages[i])
            out = os.path.join(outfolder,f"{name}_{i+1}.pdf")
            with open(out,"wb") as f: writer.write(f)

    messagebox.showinfo("Done","Split completed")

def remove_pages():
    file = filedialog.askopenfilename(filetypes=[("PDF","*.pdf")])
    if not file: return
    reader = PdfReader(file)
    writer = PdfWriter()
    remove = simpledialog.askstring("Remove","Pages to remove (2,4)")
    rem = [int(x.strip())-1 for x in remove.split(",")]
    for i in range(len(reader.pages)):
        if i not in rem:
            writer.add_page(reader.pages[i])
    out = os.path.join(create_output(file),"removed.pdf")
    with open(out,"wb") as f: writer.write(f)
    messagebox.showinfo("Done","Pages removed")

def compress_pdf():
    file = filedialog.askopenfilename(filetypes=[("PDF","*.pdf")])
    if not file: return
    reader = PdfReader(file)
    writer = PdfWriter()
    for p in reader.pages:
        p.compress_content_streams()
        writer.add_page(p)
    out = os.path.join(create_output(file),"compressed.pdf")
    with open(out,"wb") as f: writer.write(f)
    messagebox.showinfo("Done","Compressed")

def pdf_to_word():
    file = filedialog.askopenfilename(filetypes=[("PDF","*.pdf")])
    if not file: return
    out = os.path.join(create_output(file),"converted.docx")
    cv = Converter(file)
    cv.convert(out)
    cv.close()
    messagebox.showinfo("Done","Converted to Word")

def word_to_pdf():
    file = filedialog.askopenfilename(filetypes=[("Word","*.docx")])
    if not file: return
    out = os.path.join(create_output(file),"converted.pdf")
    convert(file,out)
    messagebox.showinfo("Done","Converted to PDF")

def add_watermark():
    file = filedialog.askopenfilename(filetypes=[("PDF","*.pdf")])
    if not file: return
    text = simpledialog.askstring("Watermark","Enter text")
    reader = PdfReader(file)
    writer = PdfWriter()
    temp="wm.pdf"
    c=canvas.Canvas(temp)
    c.drawString(200,400,text)
    c.save()
    wm = PdfReader(temp)
    for p in reader.pages:
        p.merge_page(wm.pages[0])
        writer.add_page(p)
    out=os.path.join(create_output(file),"watermarked.pdf")
    with open(out,"wb") as f: writer.write(f)
    os.remove(temp)
    messagebox.showinfo("Done","Watermark added")

def rotate_pdf():
    file = filedialog.askopenfilename(filetypes=[("PDF","*.pdf")])
    if not file: return
    degree = int(simpledialog.askstring("Rotate","Enter 90/180/270"))
    reader = PdfReader(file)
    writer = PdfWriter()
    for p in reader.pages:
        p.rotate(degree)
        writer.add_page(p)
    out=os.path.join(create_output(file),"rotated.pdf")
    with open(out,"wb") as f: writer.write(f)
    messagebox.showinfo("Done","Rotated")

def protect_pdf():
    file = filedialog.askopenfilename(filetypes=[("PDF","*.pdf")])
    if not file: return
    pwd = simpledialog.askstring("Password","Enter password")
    reader = PdfReader(file)
    writer = PdfWriter()
    for p in reader.pages:
        writer.add_page(p)
    writer.encrypt(pwd)
    out=os.path.join(create_output(file),"protected.pdf")
    with open(out,"wb") as f: writer.write(f)
    messagebox.showinfo("Done","Protected")

def unlock_pdf():
    file = filedialog.askopenfilename(filetypes=[("PDF","*.pdf")])
    if not file: return
    pwd = simpledialog.askstring("Password","Enter password")
    reader = PdfReader(file)
    reader.decrypt(pwd)
    writer = PdfWriter()
    for p in reader.pages:
        writer.add_page(p)
    out=os.path.join(create_output(file),"unlocked.pdf")
    with open(out,"wb") as f: writer.write(f)
    messagebox.showinfo("Done","Unlocked")

def jpg_to_pdf():
    files = filedialog.askopenfilenames(filetypes=[("Images","*.jpg;*.png")])
    if not files: return
    images = [Image.open(f).convert("RGB") for f in files]
    out = os.path.join(create_output(files[0]),"images.pdf")
    images[0].save(out,save_all=True,append_images=images[1:])
    messagebox.showinfo("Done","Images converted")

# --------------------------
# UI
# --------------------------
app = tk.Tk()
app.title("Enterprise PDF Suite")
app.geometry("800x600")
app.configure(bg=BG)

sidebar = tk.Frame(app,bg="#111",width=200)
sidebar.pack(side="left",fill="y")

content = tk.Frame(app,bg=BG)
content.pack(side="right",expand=True,fill="both")

def add_button(text,command):
    tk.Button(content,text=text,bg=BTN,fg=FG,
              activebackground=ACCENT,
              width=25,height=2,
              command=command).pack(pady=8)

# Sidebar Label
tk.Label(sidebar,text="PDF SUITE",
         bg="#111",fg=ACCENT,
         font=("Arial",18,"bold")).pack(pady=20)

# Add Buttons
tools = [
("Merge PDF",merge_pdf),
("Split PDF",split_pdf),
("Remove Pages",remove_pages),
("Compress PDF",compress_pdf),
("PDF to Word",pdf_to_word),
("Word to PDF",word_to_pdf),
("Add Watermark",add_watermark),
("Rotate PDF",rotate_pdf),
("Protect PDF",protect_pdf),
("Unlock PDF",unlock_pdf),
("JPG to PDF",jpg_to_pdf),
]

for t in tools:
    add_button(t[0],t[1])

tk.Button(content,text="Exit",bg="red",fg="white",
          command=app.quit,width=20).pack(pady=20)

app.mainloop()