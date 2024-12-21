import requests
from bs4 import BeautifulSoup

problems_request = requests.get(f"https://openstax.org/books/chemistry-2e/pages/1-exercises")
# Parse the HTML content using BeautifulSoup
problems_soup = BeautifulSoup(problems_request.content, 'html.parser')

solutions_request = requests.get(f"https://openstax.org/books/chemistry-2e/pages/chapter-1")
solutions_soup = BeautifulSoup(solutions_request.content, 'html.parser')
os_solution_container_divs = solutions_soup.find_all('div', attrs={'data-type': 'solution'})
print(len(os_solution_container_divs))
print(os_solution_container_divs[0])
print("\n")
print(os_solution_container_divs[1])
print("\n")
print(os_solution_container_divs[2])

# for os_solution_container_div in os_solution_container_divs:
#     solutions_dict[os_solution_container_div["id"]] = xml_to_latex(str(os_solution_container_div))
# for id in problems_dict:
#     if id in solutions_dict:
#         output.append({"chapter_number": chapter_num, "id": id, "problem": problems_dict[id], "solution": solutions_dict[id]})
# print("\n")

