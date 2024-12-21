from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import time

# Define the Chrome webdriver options
options = webdriver.ChromeOptions()
options.add_argument("--headless") # Set the Chrome webdriver to run in headless mode for scalability

# By default, Selenium waits for all resources to download before taking actions.
# However, we don't need it as the page is populated with dynamically generated JavaScript code.
options.page_load_strategy = "none"

# Pass the defined options objects to initialize the web driver
driver = Chrome(options=options)
# Set an implicit wait of 5 seconds to allow time for elements to appear before throwing an exception
driver.implicitly_wait(5)

url = "https://openstax.org/subjects/business"

driver.get(url)
time.sleep(5)

content = driver.find_elements(By.CSS_SELECTOR, "div[class*='books'")
print(content)

# for category in ["business", "science"]:
#     url = f"https://openstax.org/subjects/{category}"
#     print(url)
#     r = requests.get(url)
#     soup = BeautifulSoup(r.content, 'html.parser')
#     print(r.content)
#     book_title_divs = soup.find_all('div', class_='books')
#     # print(len(book_title_divs))
#     for book_title_div in book_title_divs:
#         book_link = book_title_div.find("a")["href"]
#         # print(book_link)
