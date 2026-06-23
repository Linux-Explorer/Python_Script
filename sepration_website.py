from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# List of websites to check
websites = [
    "https://engineering.kores.in/",
    "https://pharma.kores.in/",
    "https://foundry.kores.in/",
    "https://ba.kores.in/",
    "https://futuristicsecurities.com/index.html",
    "https://koresindia.in/",
    "https://kores.in/"
]

# Set up the WebDriver (Chrome in this case)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Loop through each website and open it in a new tab
for index, website in enumerate(websites):
    if index == 0:
        # Open the first website in the first tab
        driver.get(website)
    else:
        # Open each subsequent website in a new tab
        driver.execute_script(f"window.open('{website}', '_blank');")
    time.sleep(2)  # Add a small delay to ensure the tabs open smoothly

# Keep the browser open for a while to check the tabs
time.sleep(10)  # Adjust time if necessary before closing the browser

# Close the browser after the time delay
driver.quit()
