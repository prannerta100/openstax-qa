import matplotlib.pyplot as plt
# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import unquote
# import numpy as np
# import mathml2latex
#
# ENGLISH_TEXTBOOKS = [
#     "https://openstax.org/books/algebra-and-trigonometry-2e",
#     "https://openstax.org/books/american-government-3e",
#     "https://openstax.org/books/anatomy-and-physiology-2e",
#     "https://openstax.org/books/astronomy-2e",
#     "https://openstax.org/books/biology-2e",
#     "https://openstax.org/books/biology-ap-courses",
#     "https://openstax.org/books/business-ethics",
#     "https://openstax.org/books/business-law-i-essentials",
#     "https://openstax.org/books/calculus-volume-1",
#     "https://openstax.org/books/calculus-volume-2",
#     "https://openstax.org/books/calculus-volume-3",
#     "https://openstax.org/books/chemistry-2e",
#     "https://openstax.org/books/chemistry-atoms-first-2e",
#     "https://openstax.org/books/college-algebra-2e",
#     "https://openstax.org/books/college-algebra-corequisite-support-2e",
#     "https://openstax.org/books/college-physics-2e",
#     "https://openstax.org/books/college-physics-ap-courses-2e",
#     "https://openstax.org/books/concepts-biology",
#     "https://openstax.org/books/contemporary-mathematics",
#     "https://openstax.org/books/elementary-algebra-2e",
#     "https://openstax.org/books/entrepreneurship",
#     "https://openstax.org/books/intermediate-algebra-2e",
#     "https://openstax.org/books/introduction-anthropology",
#     "https://openstax.org/books/introduction-business",
#     "https://openstax.org/books/introduction-intellectual-property",
#     "https://openstax.org/books/introduction-philosophy",
#     "https://openstax.org/books/introduction-political-science",
#     "https://openstax.org/books/introduction-sociology-3e",
#     "https://openstax.org/books/introductory-business-statistics",
#     "https://openstax.org/books/introductory-business-statistics-2e",
#     "https://openstax.org/books/introductory-statistics",
#     "https://openstax.org/books/introductory-statistics-2e",
#     "https://openstax.org/books/microbiology",
#     "https://openstax.org/books/organic-chemistry",
#     "https://openstax.org/books/organizational-behavior",
#     "https://openstax.org/books/physics",
#     "https://openstax.org/books/prealgebra-2e",
#     "https://openstax.org/books/precalculus-2e",
#     "https://openstax.org/books/principles-economics-3e",
#     "https://openstax.org/books/principles-finance",
#     "https://openstax.org/books/principles-financial-accounting",
#     "https://openstax.org/books/principles-macroeconomics-3e",
#     "https://openstax.org/books/principles-management",
#     "https://openstax.org/books/principles-managerial-accounting",
#     "https://openstax.org/books/principles-marketing",
#     "https://openstax.org/books/principles-microeconomics-3e",
#     "https://openstax.org/books/psychology-2e",
#     "https://openstax.org/books/statistics",
#     "https://openstax.org/books/university-physics-volume-1",
#     "https://openstax.org/books/university-physics-volume-2",
#     "https://openstax.org/books/university-physics-volume-3",
#     "https://openstax.org/books/us-history",
#     "https://openstax.org/books/world-history-volume-1",
#     "https://openstax.org/books/world-history-volume-2",
#     "https://openstax.org/books/writing-guide",
# ]
#
# ENGLISH_TEXTBOOKS_WITH_SOLUTIONS = [
#     "algebra-and-trigonometry-2e",
#     "american-government-3e",
#     "business-ethics",
#     "business-law-i-essentials",
#     "calculus-volume-1",
#     "calculus-volume-2",
#     "calculus-volume-3",
#     "chemistry-2e",
#     "chemistry-atoms-first-2e",
#     "college-algebra-2e",
#     "college-algebra-corequisite-support-2e",
#     "college-physics-2e",
#     "college-physics-ap-courses-2e",
#     "contemporary-mathematics",
#     "elementary-algebra-2e",
#     "intermediate-algebra-2e",
#     "introduction-intellectual-property",
#     "introduction-sociology-3e",
#     "microbiology",
#     "organic-chemistry",
#     "prealgebra-2e",
#     "precalculus-2e",
#     "principles-economics-3e",
#     "principles-financial-accounting",
#     "principles-macroeconomics-3e",
#     "principles-managerial-accounting",
#     "principles-marketing",
#     "principles-microeconomics-3e",
#     "university-physics-volume-1",
#     "university-physics-volume-2",
#     "university-physics-volume-3",
#     "us-history",
# ]
#
#
# SPANISH_TEXTBOOKS = [
#     "https://openstax.org/books/física-universitaria-volumen-1",
#     "https://openstax.org/books/física-universitaria-volumen-2",
#     "https://openstax.org/books/física-universitaria-volumen-3",
#     "https://openstax.org/books/química-2ed",
#     "https://openstax.org/books/química-comenzando-átomos-2ed",
#     "https://openstax.org/books/introducción-estadística-empresarial",
#     "https://openstax.org/books/cálculo-volumen-1",
#     "https://openstax.org/books/cálculo-volumen-2",
#     "https://openstax.org/books/cálculo-volumen-3",
#     "https://openstax.org/books/introducción-estadística",
#     "https://openstax.org/books/precálculo-2ed",
# ]
#
# SPANISH_TEXTBOOKS_WITH_SOLUTIONS = [
#     "física-universitaria-volumen-1",
#     "física-universitaria-volumen-2",
#     "física-universitaria-volumen-3",
#     "química-2ed",
#     "química-comenzando-átomos-2ed",
#     "cálculo-volumen-1",
#     "cálculo-volumen-2",
#     "cálculo-volumen-3",
#     "precálculo-2ed",
# ]
#
# POLISH_TEXTBOOKS = [
#     "https://openstax.org/books/fizyka-dla-szkół-wyższych-tom-1",
#     "https://openstax.org/books/fizyka-dla-szkół-wyższych-tom-2",
#     "https://openstax.org/books/fizyka-dla-szkół-wyższych-tom-3",
#     "https://openstax.org/books/psychologia-polska",
#     "https://openstax.org/books/mikroekonomia-podstawy",
#     "https://openstax.org/books/makroekonomia-podstawy",
# ]
#
# POLISH_TEXTBOOKS_WITH_SOLUTIONS = [
#     "fizyka-dla-szkół-wyższych-tom-1",
#     "fizyka-dla-szkół-wyższych-tom-2",
#     "fizyka-dla-szkół-wyższych-tom-3",
#     "mikroekonomia-podstawy",
#     "makroekonomia-podstawy",
# ]
#
#
#
# # Complex XML text
# complex_xml = '''<div class=\"os-problem-container\">\n        <p id=\"import-auto-id2441236\">A 63.0-kg sprinter starts a race with an acceleration of <span class=\"os-math-in-para\"><math display=\"inline\"><semantics><mrow><mrow><mrow><mrow><mn>4</mn><mtext>.</mtext><mtext>20 m</mtext><msup><mtext>/s</mtext><mrow><mn>2</mn></mrow></msup></mrow></mrow></mrow></mrow><annotation-xml encoding=\"MathML-Content\"><mrow><mrow><mrow><mn>4</mn><mtext>.</mtext><mtext>20 m</mtext><msup><mtext>/s</mtext><mrow><mn>2</mn></mrow></msup></mrow></mrow></mrow></annotation-xml></semantics></math></span>. What is the net external force on him?</p></div>'''
#
# # Parse the complex XML text
# soup = BeautifulSoup(complex_xml, 'html.parser')
#
# # Extract text content
# text_content = soup.get_text()
#
# # Convert MathML to LaTeX notation
# text_content = mathml2latex(text_content)
#
# print(text_content)

import pandas as pd

df = pd.read_csv("dataset_sizes.csv", header=None)
df.columns = ["num_pages", "name"]
df["name"] = df["name"].apply(lambda x: x.split("/")[1].split(".")[0])
df["num_pages"] = df["num_pages"].astype(int)
df.index = df["name"]
# plt.xticks(rotation='vertical')
df.sort_values(by="num_pages", inplace=True)
plt.barh(df["name"], df["num_pages"])
plt.show()