import os
from typing import Optional

import cv2
import pytesseract
import tkinter as tk
from tkinter import filedialog, messagebox

# 🔧 Set Tesseract path (change if needed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# ---------------------------------------------------
# IMAGE PREPROCESSING
# ---------------------------------------------------
def preprocess_image(image_path: str) -> cv2.Mat:
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)

    if img is None:
        raise ValueError("❌ Unable to read image.")

    # ✅ Handle PNG transparency (RGBA → RGB)
    if len(img.shape) == 3 and img.shape[2] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # ✅ Resize if image is small (improves OCR accuracy)
    height, width = gray.shape
    if width < 1000:
        scale_factor = 2
        gray = cv2.resize(gray, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)

    # ✅ Light blur to remove noise
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    # ✅ Otsu threshold (better for PNG + digital images)
    _, thresh = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    # ✅ Auto invert if background is dark
    if cv2.countNonZero(thresh) > (thresh.size // 2):
        thresh = cv2.bitwise_not(thresh)

    return thresh


# ---------------------------------------------------
# OCR FUNCTION
# ---------------------------------------------------
def ocr_image(image_path: str, lang: str = "eng") -> str:
    if not os.path.exists(image_path):
        raise FileNotFoundError("❌ Image file not found.")

    processed_img = preprocess_image(image_path)

    config = "--oem 3 --psm 6"
    text = pytesseract.image_to_string(processed_img, lang=lang, config=config)

    return text.strip()


# ---------------------------------------------------
# SAVE OUTPUT
# ---------------------------------------------------
def save_text(text: str, output_path: str):
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)


# ---------------------------------------------------
# FILE PICKER
# ---------------------------------------------------
def pick_image():
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    file_path = filedialog.askopenfilename(
        title="Select Image for OCR",
        filetypes=[
            ("Image Files", "*.png *.jpg *.jpeg *.bmp *.tif *.tiff *.webp"),
            ("All Files", "*.*"),
        ],
    )

    root.destroy()
    return file_path


# ---------------------------------------------------
# MAIN
# ---------------------------------------------------
if __name__ == "__main__":

    image_path = pick_image()

    if not image_path:
        print("No image selected. Exiting.")
        exit()

    try:
        print("🔍 Processing image...")
        extracted_text = ocr_image(image_path)

        base, _ = os.path.splitext(image_path)
        output_file = base + "_OCR.txt"

        save_text(extracted_text, output_file)

        messagebox.showinfo("Success", f"✅ OCR Complete!\nSaved to:\n{output_file}")
        print(f"✅ OCR Complete! Saved to: {output_file}")

    except Exception as e:
        messagebox.showerror("Error", str(e))
        print("❌ Error:", e)