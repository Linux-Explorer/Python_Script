import platform

def get_windows_users():
    import wmi
    c = wmi.WMI()

    # Fetching all users (including domain accounts)
    users = c.query("SELECT Name, FullName, Disabled, Lockout, LocalAccount FROM Win32_UserAccount")

    user_list = []
    for u in users:
        user_list.append({
            "username": u.Name,
            "full_name": (u.FullName or ""),
            "disabled": bool(u.Disabled),
            "locked": bool(u.Lockout),
        })

    return user_list

def get_linux_users():
    # Basic Linux local users from /etc/passwd (filters out system users by UID >= 1000)
    users = []
    with open("/etc/passwd", "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split(":")
            if len(parts) < 3:
                continue
            name = parts[0]
            uid = int(parts[2])
            if uid >= 1000 and name not in ("nobody",):
                users.append({"username": name})
    return users

def count_and_list_users():
    os_platform = platform.system().lower()

    if os_platform == "windows":
        user_list = get_windows_users()
    elif os_platform == "linux":
        user_list = get_linux_users()
    else:
        print("Unsupported platform!")
        return []

    return user_list

# Get and print users + count
users = count_and_list_users()

print(f"Number of users on this PC: {len(users)}")
print("\nUsers:")
for i, u in enumerate(users, start=1):
    # Windows has more fields; Linux only username
    extra = ""
    if "full_name" in u:
        extra = f" | Full Name: {u['full_name']} | Disabled: {u['disabled']} | Locked: {u['locked']}"
    print(f"{i}. {u['username']}{extra}")
