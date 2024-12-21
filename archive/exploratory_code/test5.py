from bs4 import BeautifulSoup
import requests
from openai_xml_parser import xml_to_latex

# Assuming 'html_content' contains the HTML content of the webpage
# You can replace 'html_content' with the actual HTML content string

r = requests.get("https://openstax.org/books/college-physics-2e/pages/1-problems-exercises")
# Parse the HTML content using BeautifulSoup
problem_soup = BeautifulSoup(r.content, 'html.parser')

# Find the <div> tag with class="os-hasSolution"
os_has_solution_divs = problem_soup.find_all('div', class_='os-hasSolution')

for os_has_solution_div in os_has_solution_divs:
    # Find the <div> tag with class="os-problem-container" inside the os_has_solution_div
    os_problem_container_div = os_has_solution_div.find('div', class_='os-problem-container')

    print({os_has_solution_div["id"]: xml_to_latex(str(os_problem_container_div))})
    # Extract the text or other data from the os_problem_container_div
    data = os_problem_container_div #.get_text()
