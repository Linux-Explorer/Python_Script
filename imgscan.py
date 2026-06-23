import os

# Function to count image files
def count_images(directory):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
    image_count = 0

    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(file.lower().endswith(ext) for ext in image_extensions):
                image_count += 1
    
    return image_count

# Set the directory you want to scan (e.g., C: or D: drive on Windows or /home/user on Linux)
directory_to_scan = 'C:\\'  # Change this to the path you want to scan
image_count = count_images(directory_to_scan)

print(f'Total number of images in "{directory_to_scan}": {image_count}')
