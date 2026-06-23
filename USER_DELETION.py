import subprocess
import ctypes
import sys
import tkinter as tk
from tkinter import simpledialog, messagebox


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def user_exists(username):
    result = subprocess.run(
        ["net", "user", username],
        capture_output=True,
        text=True
    )
    return result.returncode == 0


def delete_user(username):
    result = subprocess.run(
        ["net", "user", username, "/delete"],
        capture_output=True,
        text=True
    )
    return result.returncode == 0, result.stderr


def main():
    if not is_admin():
        messagebox.showerror("Error", "Please run this script as Administrator.")
        sys.exit(1)

    root = tk.Tk()
    root.withdraw()  # Hide main window

    username = simpledialog.askstring("Delete User", "Enter username to delete:")

    if not username:
        messagebox.showinfo("Cancelled", "No username entered.")
        return

    if not user_exists(username):
        messagebox.showerror("Error", f"User '{username}' does not exist.")
        return

    success, error = delete_user(username)

    if success:
        messagebox.showinfo("Success", f"User '{username}' deleted successfully.")
    else:
        messagebox.showerror("Failed", f"Could not delete user.\n\n{error}")


if __name__ == "__main__":
    main()
