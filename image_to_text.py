from PIL import Image
import numpy as np

# Define the characters to represent different brightness levels
ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

# Function to resize the image
def resize_image(image, new_width=100):
    width, height = image.size
    aspect_ratio = height/width
    new_height = int(aspect_ratio * new_width)
    resized_image = image.resize((new_width, new_height))
    return resized_image

# Function to convert image to grayscale
def grayscale_image(image):
    return image.convert("L")  # "L" stands for grayscale

# Function to convert grayscale image to ASCII
def grayscale_to_ascii(image):
    pixels = np.array(image)  # Convert image to numpy array
    ascii_str = ""
    
    for pixel in pixels:
        for value in pixel:
            ascii_str += ASCII_CHARS[value // 25]  # Divide by 25 to get a value between 0 and len(ASCII_CHARS)-1
        ascii_str += "\n"
    
    return ascii_str

# Function to generate ASCII art
def generate_ascii_art(image_path, new_width=100):
    try:
        image = Image.open(image_path)
    except Exception as e:
        print(e)
        return None

    # Resize image, convert to grayscale, and convert to ASCII
    image = resize_image(image, new_width)
    image = grayscale_image(image)
    ascii_art = grayscale_to_ascii(image)

    return ascii_art

# Main function
if __name__ == "__main__":
    image_path = "D:\Screenshot (9).png"  # Change this to your image path
    ascii_art = generate_ascii_art(image_path, new_width=100)
    
    if ascii_art:
        print(ascii_art)
        with open("output_ascii_art.txt", "w") as f:
            f.write(ascii_art)
        print("ASCII art saved to 'output_ascii_art.txt'")