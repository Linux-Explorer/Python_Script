import os
import fitz  # PyMuPDF
import tkinter as tk
from tkinter import filedialog


def pick_pdf():
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    root.destroy()
    return path


def safe_font_name(name):
    """
    Map PDF font names to PyMuPDF built-in fonts.
    """
    if not name:
        return "helv"

    n = name.lower()

    if "courier" in n or "cour" in n:
        return "cour"
    if "times" in n:
        return "tiro"
    if "symbol" in n:
        return "symb"
    if "zapf" in n or "dingbats" in n:
        return "zadb"

    # Default safe font
    return "helv"


def main():
    print("=== Smart PDF Designation Changer ===\n")

    pdf_path = input("Press Enter to select PDF: ").strip()
    if not pdf_path:
        pdf_path = pick_pdf()

    if not pdf_path or not os.path.isfile(pdf_path):
        print("Invalid PDF path.")
        return

    old_text = input("Enter ANY part of old designation (example: Executive): ").strip()
    new_text = input("Enter NEW designation: ").strip()

    if not old_text or not new_text:
        print("Both old and new text are required.")
        return

    doc = fitz.open(pdf_path)
    found = False

    for page in doc:
        matches = page.search_for(old_text)

        for rect in matches:
            found = True

            # Expand rectangle to cover full old designation area
            rect = fitz.Rect(rect)
            rect.x1 += 180

            blocks = page.get_text("dict")["blocks"]

            pdf_font_name = None
            insert_font_name = "helv"
            font_size = 12
            color = (0, 0, 0)

            for b in blocks:
                if b.get("type") != 0:
                    continue
                for l in b.get("lines", []):
                    for s in l.get("spans", []):
                        span_rect = fitz.Rect(s["bbox"])
                        if rect.intersects(span_rect):
                            pdf_font_name = s.get("font", "")
                            insert_font_name = safe_font_name(pdf_font_name)
                            font_size = s.get("size", 12)
                            color = fitz.sRGB_to_pdf(s.get("color", 0))
                            break

            # Redact old text
            page.add_redact_annot(rect, fill=(1, 1, 1))
            page.apply_redactions()

            # Insert new text with safe font
            result = page.insert_textbox(
                rect,
                new_text,
                fontsize=font_size,
                fontname=insert_font_name,
                color=color,
                align=0
            )

            # If text does not fit, reduce font size slightly
            if result < 0:
                for shrink in [0.5, 1, 1.5, 2, 3]:
                    result = page.insert_textbox(
                        rect,
                        new_text,
                        fontsize=max(6, font_size - shrink),
                        fontname=insert_font_name,
                        color=color,
                        align=0,
                        overlay=True
                    )
                    if result >= 0:
                        break

    if not found:
        print("\nCould not find the text.")
        print("Try entering only one word like: Executive")
        doc.close()
        return

    output = pdf_path.replace(".pdf", "_updated.pdf")
    doc.save(output)
    doc.close()

    print("\nDone!")
    print("Saved as:", output)


if __name__ == "__main__":
    main()