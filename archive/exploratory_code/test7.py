import re
from bs4 import BeautifulSoup
import requests

# Target URL
url = "https://open.oregonstate.education/?search_term&per_page=50&sort_by=last_updated#catalog"

# Send a GET request to the URL
response = requests.get(url, verify=False)

# Parse HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Find all <a> tags
links = soup.find_all("div", href=True, class_="book_info")
print(links)

# Filter relevant links using regular expression
pattern = re.compile(r"https://open.oregonstate.education/?search_term&per_page=50&sort_by=last_updated#catalog[\w-]+")
subpage_urls = [link["href"] for link in links if pattern.match(link["href"])]

# Print subpage URLs
# for subpage_url in subpage_urls:
#     print(subpage_url)

