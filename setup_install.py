import os
import subprocess
import sys
import ctypes

# ===============================
# CONFIGURATION
# ===============================

NETWORK_SHARE = r"\\192.168.0.2\IT Infra\application\SAP Setups\Sap Updated Setup 17.05.2023\7_70\BD_NW_7.0_Presentation_7.70_Comp._1_\PRES1\GUI\Windows\Win32"
SETUP_FILE = "SetupAll.exe"

USERNAME = "KORES-INDIA\\koresadmin"   # ⚠ Try this format
PASSWORD = "K0r3s@!@#"

# ===============================
# ADMIN CHECK
# ===============================

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    print("Run as Administrator.")
    sys.exit()

# ===============================
# CONNECT TO SHARE (NO DRIVE LETTER)
# ===============================

def connect_share():

    print("Clearing old SMB sessions...")

    # Remove ALL previous connections
    subprocess.run(["net", "use", "*", "/delete", "/y"],
                   stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL)

    print("Connecting to network share...")

    try:
        subprocess.run(
            ["net", "use", NETWORK_SHARE, PASSWORD, f"/user:{USERNAME}"],
            check=True
        )
        print("Connected successfully.")
    except subprocess.CalledProcessError as e:
        print("Connection failed.")
        print(e)
        sys.exit()

# ===============================
# INSTALL SAP
# ===============================

def install_sap():

    installer_path = os.path.join(NETWORK_SHARE, SETUP_FILE)

    if not os.path.exists(installer_path):
        print("Installer not found.")
        sys.exit()

    print("Starting SAP installation...")

    try:
        subprocess.run(
            [installer_path, "/silent", "/norestart"],
            check=True
        )
        print("SAP Installed Successfully.")
    except subprocess.CalledProcessError as e:
        print("Installation Failed.")
        print(e)

# ===============================
# MAIN
# ===============================

if __name__ == "__main__":
    connect_share()
    install_sap()