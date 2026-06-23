import subprocess

def create_user(username, password):
    try:
        command = ["net", "user", username, password, "/add"]

        result = subprocess.run(
            command,
            text=True,
            capture_output=True,
            check=False
        )

        print("\n--- OUTPUT ---")
        print(result.stdout)
        print(result.stderr)

        if result.returncode == 0:
            print(f"\nUser '{username}' created successfully.")
        else:
            print("\nUser creation failed.")

    except Exception as e:
        print("Exception:", str(e))


username = input("Enter username: ")
password = input("Enter password: ")

create_user(username, password)