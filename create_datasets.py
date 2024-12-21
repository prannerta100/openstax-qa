import os
import time
import json
from scraper_utils import scrape_textbook_id_unmatched
from postprocessing_utils import clean_string

textbook_dict_english = {
    "chemistry-2e": ["exercises"],
    "college-algebra-2e":  ["review-exercises"],
    "principles-economics-3e":  ["self-check-questions"],
    "american-government-3e":  ["review-questions"],
    "us-history":  ["review-questions"],
    "business-law-i-essentials":  ["assessment-questions"],
    "college-physics-2e": ["problems-exercises"],
    "microbiology": ["multiple-choice", "true-false", "matching", "fill-in-the-blank", "short-answer"],
    "university-physics-volume-1": ["conceptual-questions", "problems", "additional-problems", "challenge-problems"],
    "university-physics-volume-2": ["conceptual-questions", "problems", "additional-problems", "challenge-problems"],
    "university-physics-volume-3": ["conceptual-questions", "problems", "additional-problems", "challenge-problems"],
    "algebra-and-trigonometry-2e": ["review-exercises", "practice-test"],
    "business-ethics": ["assessment-questions"],
    "calculus-volume-1": ["review-exercises"],
    "calculus-volume-2": ["review-exercises"],
    "calculus-volume-3": ["review-exercises"],
    "chemistry-atoms-first-2e": ["exercises"],
    "college-algebra-corequisite-support-2e": ["review-exercises", "practice-test"],
    "college-physics-ap-courses-2e": ["problems-exercises"],
    "contemporary-mathematics": [],
    "elementary-algebra-2e": ["review-exercises", "practice-test"],
    "intermediate-algebra-2e": ["review-exercises", "practice-test"],
    "introduction-intellectual-property": ["assessment-questions"],
    "introduction-sociology-3e": ["section-quiz", "short-answer"],
    "organic-chemistry": [],
    "prealgebra-2e": ["review-exercises", "practice-test"],
    "precalculus-2e": ["review-exercises", "practice-test"],
    "principles-financial-accounting": ["multiple-choice", "questions"],
    "principles-macroeconomics-3e": ["self-check-questions"],
    "principles-managerial-accounting": ["multiple-choice", "questions"],
    "principles-marketing": [],
    "principles-microeconomics-3e": ["self-check-questions"]
}

textbook_dict_polish = {
    "fizyka-dla-szkół-wyższych-tom-1": ["pytania", "zadania", "zadania-dodatkowe", "zadania-trudniejsze"],
    "fizyka-dla-szkół-wyższych-tom-2": ["pytania", "zadania", "zadania-dodatkowe", "zadania-trudniejsze"],
    "fizyka-dla-szkół-wyższych-tom-3": ["pytania", "zadania", "zadania-dodatkowe", "zadania-trudniejsze"],
    "mikroekonomia-podstawy": ["pytania-sprawdzajace"],
    "makroekonomia-podstawy": ["pytania-sprawdzajace"]
}

textbook_dict_spanish = {
    "física-universitaria-volumen-1": ["preguntas-conceptuales", "problemas", "problemas-adicionales", "problemas-de-desafio"],
    "física-universitaria-volumen-2": ["preguntas-conceptuales", "problemas", "problemas-adicionales", "problemas-de-desafio"],
    "física-universitaria-volumen-3": ["preguntas-conceptuales", "problemas", "problemas-adicionales", "problemas-de-desafio"],
    "química-2ed": ["ejercicios"],
    "química-comenzando-átomos-2ed": ["ejercicios"],
    "cálculo-volumen-1": ["ejercicios-de-repaso"],
    "cálculo-volumen-2": ["ejercicios-de-repaso"],
    "cálculo-volumen-3": ["ejercicios-de-repaso"],
    "precálculo-2ed": ["ejercicios-de-repaso", "examen-de-practica"],
}

# cnt = 0
# for textbook in textbook_dict_spanish:
#     if len(textbook_dict_spanish[textbook]) > 0:
#         try:
#             scrape_textbook_id_unmatched(textbook, textbook_dict_spanish[textbook], language="spanish")
#             cnt += 1
#             time.sleep(3)
#         except RuntimeError as e:
#             print(e)
#
# cnt = 0
# for textbook in textbook_dict_polish:
#     if len(textbook_dict_polish[textbook]) > 0:
#         try:
#             scrape_textbook_id_unmatched(textbook, textbook_dict_polish[textbook], language="polish")
#             cnt += 1
#             time.sleep(3)
#         except RuntimeError as e:
#             print(e)

# cnt = 0
# for textbook in textbook_dict_english:
#     if len(textbook_dict_english[textbook]) > 0:
#         try:
#             scrape_textbook_id_unmatched(textbook, textbook_dict_english[textbook], language="english")
#             cnt += 1
#             time.sleep(3)
#         except RuntimeError as e:
#             print(e)

languages = ["english", "spanish", "polish"]
language_code_dict = {"english": "en", "spanish": "es", "polish": "pl"}
new_json = []
for language in languages:
    folder = "datasets/" + language + "/"
    for filename in os.listdir(folder):
        with open(folder + filename) as fp:
            json_file = json.loads(fp.read())
        for entry in json_file:
            new_json.append({
                "language": language_code_dict[language],
                "book": filename.split(".")[0],
                "chapter_number": entry["chapter_number"],
                "id": entry["id"],
                "problem": entry["problem"],
                "problem_cleaned": clean_string(entry["problem"]),
                "solution": entry["solution"],
                "solution_cleaned": clean_string(entry["solution"])
            })
with open("openstax_processed_data.json", "w") as fp:
    json.dump(new_json, fp)
