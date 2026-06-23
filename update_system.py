import subprocess

def pending_updates():
    cmd = [
        "powershell",
        "-Command",
        "(New-Object -ComObject Microsoft.Update.Session).CreateUpdateSearcher().Search('IsInstalled=0').Updates.Count"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    output = result.stdout.strip()

    print("\nPending Updates:", output if output else "0 or unavailable")


pending_updates()