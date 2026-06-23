import os
import csv

# Define the network path (example: '\\\\NetworkPath\\Movies')
network_path = r'\\192.168.1.17\d$'  # Update this with your network path
# Define the file extensions for movies (you can add more extensions if needed)
movie_extensions = ['.mp4', '.mkv', '.avi', '.mov', '.flv', '.wmv', '.mpg', '.mpeg']

# Specify the path to save the CSV file
csv_file = r'D:\movie_list.csv'

try:
    # Open the CSV file for writing
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Movie Name', 'File Path']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header
        writer.writeheader()

        # Walk through the network directory and scan for movie files
        print(f"Scanning network path: {network_path}")
        for root, dirs, files in os.walk(network_path):
            for file in files:
                # Print all files (debugging purpose)
                print(f"Found file: {file}")
                
                # Check if the file has a movie extension
                if any(file.lower().endswith(ext) for ext in movie_extensions):
                    file_path = os.path.join(root, file)
                    # Write movie name and path to the CSV file
                    writer.writerow({'Movie Name': file, 'File Path': file_path})
                    print(f"Found movie file: {file} at {file_path}")

    print(f"Movie list has been saved to {csv_file}")
except Exception as e:
    print(f"Error: {e}")