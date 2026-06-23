from __future__ import annotations

import os
import sys
import subprocess
import shutil
from pathlib import Path
import webbrowser

# IMPORTANT: Use the console URL, not the long auth/authorize URL.
# This will redirect to login only if you are not already signed in.
DEFAULT_URL = "https://ksc.kaspersky.com/"
URL = os.environ.get("KSC_URL", DEFAULT_URL)

# Profile folder where the browser stores cookies/session (so next runs stay logged in)
PROFILE_DIR = Path(os.environ.get("KSC_PROFILE_DIR", str(Path.home() / ".ksc_profile"))).expanduser()
PROFILE_DIR.mkdir(parents=True, exist_ok=True)

# Set this to "1" if you want an app-like window (no tabs/address bar)
APP_MODE = os.environ.get("KSC_APP_MODE", "0") == "1"


def candidate_browsers() -> list[str]:
    """Find Chrome/Edge/Brave executables across OSes."""
    if sys.platform.startswith("win"):
        bases = [os.environ.get("PROGRAMFILES"), os.environ.get("PROGRAMFILES(X86)"), os.environ.get("LOCALAPPDATA")]
        paths = []
        for base in filter(None, bases):
            paths += [
                Path(base) / "Google/Chrome/Application/chrome.exe",
                Path(base) / "Microsoft/Edge/Application/msedge.exe",
                Path(base) / "BraveSoftware/Brave-Browser/Application/brave.exe",
            ]
        return [str(p) for p in paths if p.exists()]

    if sys.platform == "darwin":
        candidates = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
            "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
        ]
        return [c for c in candidates if Path(c).exists()]

    # Linux
    names = ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "microsoft-edge", "brave-browser"]
    found = [shutil.which(n) for n in names]
    return [f for f in found if f]


def open_in_browser(exe: str, url: str) -> bool:
    args = [
        exe,
        f"--user-data-dir={str(PROFILE_DIR)}",
        "--new-window",
        "--start-maximized",
    ]
    if APP_MODE:
        args.append(f"--app={url}")
    else:
        args.append(url)

    try:
        subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception:
        return False


def main() -> None:
    # Prefer Edge/Chrome if available
    for exe in candidate_browsers():
        if open_in_browser(exe, URL):
            print("Opened Kaspersky Cloud Console.")
            print(f"URL: {URL}")
            print(f"Persistent profile: {PROFILE_DIR}")
            print("First run: sign in once in the browser window. Next runs: should open already signed in (until session expires).")
            return

    # Fallback: default browser (may still work if you're signed in there already)
    webbrowser.open(URL)
    print("Opened using your default browser (no dedicated profile found).")


if __name__ == "__main__":
    main()