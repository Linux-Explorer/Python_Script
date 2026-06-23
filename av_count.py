import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Hide root window
Tk().withdraw()

print("Select your Excel file")
file_path = askopenfilename(filetypes=[("Excel Files", "*.xlsx *.xls")])

if not file_path:
    print("No file selected.")
    exit()

# Read Excel
df = pd.read_excel(file_path)

# Check if column exists
if "Full group name" not in df.columns:
    print("Column 'Full group name' not found.")
    exit()

# Extract second level group
def extract_group(x):
    try:
        parts = str(x).split("/")
        if len(parts) >= 2:
            return parts[1].strip()
        return "Unknown"
    except:
        return "Unknown"

df["Group"] = df["Full group name"].apply(extract_group)

# Count occurrences
result = df["Group"].value_counts().reset_index()
result.columns = ["Group", "Count"]

# Save output
output_file = "processed_groups.xlsx"
result.to_excel(output_file, index=False)

print(f"\nProcessed file saved as: {output_file}")
print(result)