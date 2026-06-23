import tkinter as tk
from tkinter import messagebox
import subprocess

# ----------------------------
# Function to check AD user
# ----------------------------
def check_user():

    username = entry.get().strip()

    if not username:
        messagebox.showerror("Error", "Please enter username")
        return

    # PowerShell command
    powershell_command = f"""
    Get-ADUser "{username}" -Properties LockedOut,Enabled,BadLogonCount,LastLogonDate,PasswordLastSet,PasswordNeverExpires,AccountExpirationDate,msDS-UserPasswordExpiryTimeComputed |
    Select-Object Name,
    SamAccountName,
    Enabled,
    LockedOut,
    BadLogonCount,
    LastLogonDate,
    PasswordLastSet,
    PasswordNeverExpires,
    AccountExpirationDate,
    @{{
        Name="PasswordExpiry";
        Expression={{[datetime]::FromFileTime($_."msDS-UserPasswordExpiryTimeComputed")}}
    }} |
    Format-List
    """

    try:

        # Hide PowerShell window completely
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        result = subprocess.check_output(
            [
                "powershell",
                "-WindowStyle",
                "Hidden",
                "-Command",
                powershell_command
            ],
            startupinfo=startupinfo,
            text=True
        )

        # Clear old output
        output_box.delete("1.0", tk.END)

        # Show result
        output_box.insert(tk.END, result)

    except subprocess.CalledProcessError:
        messagebox.showerror(
            "User Not Found",
            f"Could not find user: {username}"
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ----------------------------
# GUI
# ----------------------------

root = tk.Tk()
root.title("Active Directory User Checker")
root.geometry("800x600")
root.resizable(False, False)

# Heading
heading = tk.Label(
    root,
    text="Active Directory User Checker",
    font=("Arial", 18, "bold")
)
heading.pack(pady=15)

# Username Label
label = tk.Label(
    root,
    text="Enter Username:",
    font=("Arial", 12)
)
label.pack()

# Username Entry
entry = tk.Entry(
    root,
    width=40,
    font=("Arial", 12)
)
entry.pack(pady=10)

# Search Button
button = tk.Button(
    root,
    text="Check User",
    font=("Arial", 12, "bold"),
    bg="#0078D7",
    fg="white",
    padx=15,
    pady=5,
    command=check_user
)
button.pack(pady=10)

# Output Box
output_box = tk.Text(
    root,
    wrap=tk.WORD,
    font=("Consolas", 11)
)

output_box.pack(
    padx=15,
    pady=15,
    fill="both",
    expand=True
)

# Run GUI
root.mainloop()