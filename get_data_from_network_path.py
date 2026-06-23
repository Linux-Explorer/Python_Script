import os
import subprocess
import getpass

def run_cmd(cmd: str):
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()

def build_unc(target: str, share: str) -> str:
    target = target.strip().strip("\\/")
    share = share.strip().strip("\\/")
    return rf"\\{target}\{share}"

def main():
    print("\n==============================")
    print("   REMOTE SHARE ACCESS TOOL")
    print("==============================")

    target = input("Enter destination IP/PC name (e.g. 192.168.1.35): ").strip()
    share = input("Enter share name (e.g. d$ or sharedfolder): ").strip()

    if not target or not share:
        print("❌ Destination or share cannot be empty.")
        return

    remote_path = build_unc(target, share)

    print("\n------------------------------")
    print(f"Destination Share: {remote_path}")
    print("------------------------------\n")

    username = input(r'Enter username (e.g. PCNAME\Administrator or Administrator): ').strip()
    password = getpass.getpass("Enter password: ")

    print("\nConnecting...\n")
    rc, out, err = run_cmd(f'net use "{remote_path}" /user:"{username}" "{password}"')

    if rc != 0:
        print("Connection Failed ❌")
        if out:
            print(out)
        if err:
            print(err)
        return

    print("Connected Successfully ✅")
    print(f"Connected To  ✅ {remote_path}")
    print(f"Connected As  ✅ {username}\n")

    print("Listing (top-level) files/folders:\n")
    try:
        for root, dirs, files in os.walk(remote_path):
            for d in dirs:
                print("DIR :", os.path.join(root, d))
            for f in files:
                print("FILE:", os.path.join(root, f))
            break  # remove this line if you want full recursive listing
    except Exception as e:
        print("Error reading files:", e)

    # Disconnect silently
    run_cmd(f'net use "{remote_path}" /delete')

    print(f"\nDisconnected Safely ✅ from {remote_path}\n")

if __name__ == "__main__":
    main()
