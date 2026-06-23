import subprocess
import getpass

def create_user():
    # Get username and password from user input
    username = input("Enter the username: ")
    password = getpass.getpass("Enter the password: ")  # Password will be hidden
    
    try:
        # Create the user using the input username and password
        subprocess.run(f'net user {username} {password} /add', check=True, shell=True)
        print(f"User {username} created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

# Call the function to create a user with user input
create_user()