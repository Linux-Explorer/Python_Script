import subprocess
import datetime

def main():
    today = datetime.date.today()
    start = today.strftime("%Y-%m-%d") + " 00:00:00"
    end = today.strftime("%Y-%m-%d") + " 23:59:59"

    print("\nChecking domain users who changed password today...\n")

    powershell_command = f"""
    Import-Module ActiveDirectory;
    $start = Get-Date "{start}";
    $end = Get-Date "{end}";
    Get-ADUser -Filter * -Properties PasswordLastSet |
    Where-Object {{ $_.PasswordLastSet -ge $start -and $_.PasswordLastSet -le $end }} |
    Select-Object SamAccountName, Name, Enabled, PasswordLastSet |
    Sort-Object PasswordLastSet -Descending |
    Format-Table -AutoSize
    """

    result = subprocess.run(
        ["powershell", "-NoProfile", "-Command", powershell_command],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("❌ Error occurred:\n")
        print(result.stderr)
        print("\nPossible reasons:")
        print("- Not domain joined")
        print("- No AD module installed")
        print("- No permission to read Active Directory")
        return

    print(result.stdout)


if __name__ == "__main__":
    main()
