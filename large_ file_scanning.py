import os

# ===== SETTINGS =====
SEARCH_PATH = "C:\\"   # Change path if needed
TOP_RESULTS = 20       # Number of largest files to show
# ====================

large_files = []


def format_size(size):
    """Convert bytes to readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"


print(f"\nScanning for large files in: {SEARCH_PATH}")
print("Please wait...\n")

for root, dirs, files in os.walk(SEARCH_PATH):
    for file in files:
        try:
            filepath = os.path.join(root, file)
            size = os.path.getsize(filepath)

            large_files.append((size, filepath))

        except:
            pass


# Sort largest first
large_files.sort(reverse=True)

print("\n===== LARGEST FILES =====\n")

for size, filepath in large_files[:TOP_RESULTS]:
    print(f"{format_size(size):>10} | {filepath}")

print("\nScan completed.")