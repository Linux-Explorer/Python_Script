import requests

# List of websites to check
websites = [
    "https://engineering.kores.in/",
    "https://pharma.kores.in/",
    "https://foundry.kores.in/",
    "https://ba.kores.in/",
    "https://futuristicsecurities.com/index.html",
    "https://koresindia.in/",
    "https://kores.in/",
    "https://viveda.com/",
    "https://vivubijou.com/"
]

# Function to check if the website is working
def check_website(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Website '{url}' is working correctly.")
        else:
            print(f"Website '{url}' returned a non-success status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Website '{url}' is not reachable. Error: {e}")

# Check all the websites
for website in websites:
    check_website(website)
