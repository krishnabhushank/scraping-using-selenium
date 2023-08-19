import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import csv

# Path to the ChromeDriver executable
chromedriver_path = "C:/Post/chromedriver_win32/chromedriver.exe"

# Set up Chrome options
chrome_options = Options()
# chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)
# chrome_options.add_argument('--disable-gpu')  # May be necessary for some systems

# Initialize ChromeDriver
driver = webdriver.Chrome(options=chrome_options)

website_url = "https://www.samsung.com/us/business/home-appliances/home-appliances-accessories/"
driver.get(website_url)


# Function to click the "View More" button and wait for content to load
def click_view_more():
    try:
        print("Clicking for more")
        view_more_button = driver.find_element(By.CLASS_NAME,
                                               "FooterControlBar-controlButton-501421307 FooterControlBar-viewMoreButton-1605513253")
        view_more_button.click()
        return True
    except NoSuchElementException:
        return False


# Function to scroll down to trigger content loading
def scroll_down():
    # Scroll to the end of the page using the End key
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    time.sleep(2)  # Adjust the delay based on the page loading speed


# Click "View More" until no more button is found
while click_view_more():
    time.sleep(5)  # Adjust the delay based on the page loading speed

# Scroll down to load any remaining content
previous_page_height = driver.execute_script("return document.body.scrollHeight")
while True:
    scroll_down()
    time.sleep(5)  # Adjust the delay based on the page loading speed
    current_page_height = driver.execute_script("return document.body.scrollHeight")
    if current_page_height == previous_page_height:
        break
    previous_page_height = current_page_height

page_content = driver.page_source

soup = BeautifulSoup(page_content, "html.parser")

# Find all product cards
product_cards = soup.find_all("section", class_="ProductCard-root-3423567336")
print(f"Number of Products : {len(product_cards)}")

# Specify the CSV file path
csv_file_path = "C:/Users/kkoneru/Downloads/samsung_scrape/ha_accessories.csv"

# Open the CSV file in write mode and create a CSV writer
with open(csv_file_path, mode="w", newline="", encoding="utf-8") as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write the header row
    csv_writer.writerow(["Model", "Product Name", "Price", "Image URL", "Product URL"])

    for product_card in product_cards:
        data_modelcode = product_card["data-modelcode"]

        try:
            product_name = product_card.find("h2", class_="ProductName-title-3949175622").get_text(strip=True)
        except AttributeError:
            product_name = 'NA'

        try:
            price = product_card.find("span", class_="Product-card__price-current-pf").get_text(strip=True)
        except AttributeError:
            price = 'NA'

        # Extract image URL
        try:
            image_url = product_card.find("img", class_="ImageGallery-image-1120567176")["src"]
        except AttributeError:
            image_url = 'NA'
        except KeyError:
            image_url = 'NA'

        # Extract product URL
        try:
            product_url = product_card.find("a", class_="ProductCard-anchorWrapper_img-2277868790")["href"]
            product_url = "https://www.samsung.com" + product_url
        except AttributeError:
            product_url = 'NA'

        print("Data Model Code:", data_modelcode)
        print("Product Name:", product_name)
        print("Price:", price)
        print("Image URL:", image_url)
        print("Product URL:", product_url)

        print("-" * 40)  # Separator between product cards

        # Write the data row
        csv_writer.writerow([data_modelcode, product_name, price, image_url, product_url])

driver.quit()
