import winreg
import ctypes

# Registry path for Run history
RUN_MRU = r"Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU"

try:
    # Open registry key
    key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        RUN_MRU,
        0,
        winreg.KEY_ALL_ACCESS
    )

    # Get all values
    values = []
    i = 0

    while True:
        try:
            value = winreg.EnumValue(key, i)
            values.append(value[0])
            i += 1
        except OSError:
            break

    # Delete all except (Default) and MRUList
    for value_name in values:
        if value_name not in ("MRUList", ""):
            try:
                winreg.DeleteValue(key, value_name)
                print(f"Deleted: {value_name}")
            except Exception as e:
                print(f"Failed to delete {value_name}: {e}")

    winreg.CloseKey(key)

    # Restart Explorer
    ctypes.windll.user32.MessageBoxW(
        0,
        "Run history cleared successfully!",
        "Success",
        0
    )

except Exception as e:
    ctypes.windll.user32.MessageBoxW(
        0,
        f"Error:\n{e}",
        "Error",
        0
    )