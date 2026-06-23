import os
import sys
import subprocess
import ctypes
from pathlib import Path

TEMP_DIR = Path(r"C:\Temp")
TEMP_DIR.mkdir(parents=True, exist_ok=True)

def is_admin() -> bool:
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False

def run_cmd(cmd: list[str]) -> int:
    print("\nRunning:", " ".join(cmd))
    p = subprocess.run(cmd, shell=False)
    return p.returncode

def install_msi(msi_path: str, log_path: str, msi_props: dict | None = None) -> int:
    if msi_props is None:
        msi_props = {}

    props = []
    for k, v in msi_props.items():
        # Example: SERVER=10.0.0.10
        props.append(f'{k}={v}')

    cmd = [
        "msiexec", "/i", msi_path,
        "/qn",               # silent
        "/norestart",        # do not restart automatically
        "/L*v", log_path     # verbose log
    ] + props

    return run_cmd(cmd)

def install_exe(exe_path: str, args: list[str], log_path: str | None = None) -> int:
    # Some installers support /s /quiet /qn etc. (depends on package)
    cmd = [exe_path] + args
    # If your EXE supports log switch, add it here
    # Example: cmd += ["/log", str(log_path)]
    return run_cmd(cmd)

def file_exists_or_exit(path: str, name: str):
    if not Path(path).exists():
        print(f"ERROR: {name} not found at: {path}")
        sys.exit(1)

def main():
    if not is_admin():
        print("ERROR: Please run this script as Administrator.")
        sys.exit(1)

    # -----------------------------
    # ✅ SET YOUR INSTALLER PATHS
    # -----------------------------
    # Typical: klnagent.msi for Network Agent
    NETWORK_AGENT_INSTALLER = r"C:\Users\itsupport\Desktop\Av Setup\Network Agent.exe"

    # Kaspersky Security package could be .msi or .exe depending on what you have
    SECURITY_INSTALLER = r"C:\Users\itsupport\Desktop\Av Setup\Packages\setup_kes.exe"   # change if you have .exe

    # Optional: properties for Network Agent MSI (depends on your org package)
    # Common example in many environments:
    #   SERVER=KSC server IP/DNS
    # NOTE: property names can vary by build/package. Use your org’s official install guide.
    NETWORK_AGENT_MSI_PROPS = {
        # "SERVER": "10.0.0.10",
        # "USESSL": "1",
        # "PORT": "14000",
    }

    # Optional: properties for Security MSI (often managed by KSC; may need none)
    SECURITY_MSI_PROPS = {
        # Example placeholders (only if your package requires):
        # "EULA": "1"
    }

    file_exists_or_exit(NETWORK_AGENT_INSTALLER, "Network Agent installer")
    file_exists_or_exit(SECURITY_INSTALLER, "Security installer")

    na_log = str(TEMP_DIR / "kaspersky_network_agent_install.log")
    sec_log = str(TEMP_DIR / "kaspersky_security_install.log")

    print("=== Installing Kaspersky Network Agent ===")
    if NETWORK_AGENT_INSTALLER.lower().endswith(".msi"):
        code = install_msi(NETWORK_AGENT_INSTALLER, na_log, NETWORK_AGENT_MSI_PROPS)
    else:
        # If you have Network Agent as EXE:
        # Adjust silent args as per your installer documentation
        code = install_exe(NETWORK_AGENT_INSTALLER, args=["/s"], log_path=na_log)

    if code != 0:
        print(f"FAILED: Network Agent install returned code {code}")
        print(f"Check log: {na_log}")
        sys.exit(code)

    print("\n=== Installing Kaspersky Security Package ===")
    if SECURITY_INSTALLER.lower().endswith(".msi"):
        code = install_msi(SECURITY_INSTALLER, sec_log, SECURITY_MSI_PROPS)
    else:
        # If your Security package is EXE:
        # Common patterns: /s, /silent, /quiet, /qn (varies!)
        # Replace args with the right ones for your package.
        code = install_exe(SECURITY_INSTALLER, args=["/s"], log_path=sec_log)

    if code != 0:
        print(f"FAILED: Security package install returned code {code}")
        print(f"Check log: {sec_log}")
        sys.exit(code)

    print("\n✅ DONE: Kaspersky Network Agent + Security package installed successfully.")
    print(f"Logs:\n- {na_log}\n- {sec_log}")

if __name__ == "__main__":
    main()
