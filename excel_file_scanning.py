import os
import string
from concurrent.futures import ThreadPoolExecutor, as_completed

EXCEL_EXTENSIONS = {'.xls', '.xlsx', '.xlsm', '.xlsb'}

# Folders to skip (very slow / permission-heavy)
SKIP_FOLDERS = {
    "C:\\Windows",
    "C:\\Program Files",
    "C:\\Program Files (x86)",
    "C:\\System Volume Information",
    "C:\\$Recycle.Bin"
}


def is_excel(file):
    return os.path.splitext(file)[1].lower() in EXCEL_EXTENSIONS


def scan_drive(drive):
    count = 0

    for root, dirs, files in os.walk(drive):
        # Skip heavy folders early
        if any(root.startswith(skip) for skip in SKIP_FOLDERS):
            continue

        for file in files:
            if is_excel(file):
                count += 1

    print(f"Done scanning {drive} -> {count} files found")
    return count


def get_drives():
    drives = []
    for letter in string.ascii_uppercase:
        drive = f"{letter}:\\"
        if os.path.exists(drive):
            drives.append(drive)
    return drives


if __name__ == "__main__":
    drives = get_drives()
    print("Detected drives:", drives)

    total = 0

    # Run each drive in parallel
    with ThreadPoolExecutor(max_workers=len(drives)) as executor:
        futures = {executor.submit(scan_drive, d): d for d in drives}

        for future in as_completed(futures):
            total += future.result()

    print("\n======================")
    print(f"TOTAL Excel files found: {total}")
    print("======================")