import json
import numpy as np

import requests
from bs4 import BeautifulSoup
from openai_xml_parser import xml_to_latex


MAX_CHAPTER_NUM = 50
CHAPTER_KEYWORD_DICTIONARY = {"english": "chapter", "polish": "rozdzial", "spanish": "capitulo"}


def scrape_textbook_id_unmatched(textbook_name, problems_page_name_list, language="english"):
    chapter_keyword = CHAPTER_KEYWORD_DICTIONARY.get(language)
    output_json = []
    for chapter_num in range(1, MAX_CHAPTER_NUM+1):
        print(f"Scraping Chapter {chapter_num} in {textbook_name}")
        problems_list = []
        problem_id_list = []
        for problems_page_name in problems_page_name_list:
            problems_request = requests.get(f"https://openstax.org/books/{textbook_name}/pages/{chapter_num}-{problems_page_name}")
            # Parse the HTML content using BeautifulSoup
            problems_soup = BeautifulSoup(problems_request.content, 'html.parser')
            os_hasSolution_divs = problems_soup.find_all('div', class_='os-hasSolution')
            for os_hasSolution_div in os_hasSolution_divs:
                os_problem_container_div = os_hasSolution_div.find('div', class_='os-problem-container')
                problem_id_list.append(os_hasSolution_div["id"])
                problems_list.append((str(os_problem_container_div)))
        solutions_request = requests.get(f"https://openstax.org/books/{textbook_name}/pages/{chapter_keyword}-{chapter_num}")
        solutions_soup = BeautifulSoup(solutions_request.content, 'html.parser')
        os_solution_divs = solutions_soup.find_all('div', attrs={'data-type': 'solution'})
        solutions_list = []
        # print(os_solution_divs[0])
        # print("\n \n")
        for os_solution_div in os_solution_divs:
            os_solution_div_solution_container = os_solution_div.find('div', class_='os-solution-container')
            solutions_list.append((str(os_solution_div_solution_container)))
        # print(len(np.unique(solutions_list)))
        # print(list(np.unique(solutions_list)))
        if len(problems_list) == 0:
            break
        if len(problems_list) <= len(solutions_list):
            solutions_list = solutions_list[-len(problems_list):]
            for i in range(len(problem_id_list)):
                output_json.append({"chapter_number": chapter_num, "id": problem_id_list[i], "problem": problems_list[i], "solution": solutions_list[i]})
        else:
            problems_list = problems_list[:len(solutions_list)]
            problem_id_list = problem_id_list[:len(solutions_list)]
            for i in range(len(problem_id_list)):
                output_json.append({"chapter_number": chapter_num, "id": problem_id_list[i], "problem": problems_list[i], "solution": solutions_list[i]})

    outfile = f"./datasets/{textbook_name}.json"
    with open(outfile, "w") as f:
        json.dump(output_json, f)
    return output_json


# def scrape_textbook_id_match(textbook_name, problems_page_name):
#     output_json = []
#     for chapter_num in range(1, MAX_CHAPTER_NUM+1):
#         problems_request = requests.get(f"https://openstax.org/books/{textbook_name}/pages/{chapter_num}-{problems_page_name}")
#         # Parse the HTML content using BeautifulSoup
#         problems_soup = BeautifulSoup(problems_request.content, 'html.parser')
#         os_hasSolution_divs = problems_soup.find_all('div', class_='os-hasSolution')
#         if len(os_hasSolution_divs) == 0:
#             break
#         else:
#             print(len(os_hasSolution_divs))
#         problems_dict = {}
#         print(os_hasSolution_divs[0])
#         print("\n \n")
#         for os_hasSolution_div in os_hasSolution_divs[:1]:
#             os_problem_container_div = os_hasSolution_div.find('div', class_='os-problem-container')
#             problems_dict[os_hasSolution_div["id"]] = xml_to_latex(str(os_problem_container_div))
#         solutions_request = requests.get(f"https://openstax.org/books/{textbook_name}/pages/capitulo-{chapter_num}")
#         solutions_soup = BeautifulSoup(solutions_request.content, 'html.parser')
#         os_solution_divs = solutions_soup.find_all('div', attrs={'data-type': 'solution'})
#         solutions_dict = {}
#         print(os_solution_divs[0])
#         print("\n \n")
#         for os_solution_div in os_solution_divs[:1]:
#             os_solution_div_solution_container = os_solution_div.find('div', class_='os-solution-container')
#             solutions_dict[os_solution_div["id"][:-9]] = xml_to_latex(str(os_solution_div_solution_container))
#         print(solutions_dict)
#         for problem_id in problems_dict:
#             if problem_id in solutions_dict:
#                 output_json.append({"chapter_number": chapter_num, "id": problem_id, "problem": problems_dict[problem_id], "solution": solutions_dict[problem_id]})
#     outfile = f"./datasets/{textbook_name}.json"
#     with open(outfile, "w") as f:
#         json.dump(output_json, f)
#     return output_json