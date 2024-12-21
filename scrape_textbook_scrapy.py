from scrapy import Request
import os
import scrapy
from scrapy.crawler import CrawlerProcess
import time
import sys
import json


TEXTBOOK_NAME = sys.argv[1]
PROBLEMS_PAGE_NAME = sys.argv[2]
MAX_CHAPTER_NUM = 35
# "chemistry-2e": "exercises",
# "college-physics-2e": "problems-exercises",
# "college-algebra-2e": "review-exercises",  # also 'practice-test
# "principles-economics-3e": "self-check-questions",
# "american-government-3e": "review-questions",
# "us-history": "review-questions",
# "business-law-i-essentials": "assessment-questions",


class ProblemsSpider(scrapy.Spider):
    name = "problems"

    def start_requests(self):
        start_url = f"https://openstax.org/books/{self.textbook_name}/pages/{self.chapter_num}-{self.problems_page_name}"
        print("URL to scrape: ", start_url)
        yield Request(start_url)

    def parse(self, response):
        body_divs = response.css("div.os-hasSolution div.os-problem-container")
        for body_div in body_divs:
            body_text = body_div.get()
            if body_text:
                # print(body_text)
                self.problems_dict[self.chapter_num].append(body_text)
        # spider.crawler.engine.close_spider(self, reason='finished')


class SolutionsSpider(scrapy.Spider):
    name = "solutions"

    def start_requests(self):
        start_url = f"https://openstax.org/books/{self.textbook_name}/pages/chapter-{self.chapter_num}"
        print("URL to scrape: ", start_url)
        yield Request(start_url)

    def parse(self, response):
        body_divs = response.css('div[data-type="solution"] div.os-solution-container')
        for body_div in body_divs:
            body_text = body_div.get()
            if body_text:
                # print(body_text)
                self.solutions_dict[self.chapter_num].append(body_text)


def fetch_output(textbook_name, problems_page_name, chapter_num):
    # output_response = run_spider(
    #     spider=ProblemsSpider,
    #     textbook_name=textbook,
    #     problems_page_name=textbook_solution_dict[textbook],
    #     chapter_num=chapter_num,
    # )
    outputResponse = []
    process = CrawlerProcess()
    for i in range(2):
        process.crawl(
            ProblemsSpider,
            outputResponse=outputResponse,
            textbook_name=textbook_name,
            problems_page_name=problems_page_name,
            chapter_num=i + 1,
        )
    process.start()
    # del process
    # scrapy.project.crawler.engine.close_spider(self, reason='My reason')
    return outputResponse


process = CrawlerProcess()
problems_dict = {}
solutions_dict = {}
for chapter_num in range(1, MAX_CHAPTER_NUM):
    problems_dict[chapter_num] = []
    process.crawl(
        ProblemsSpider,
        problems_dict=problems_dict,
        textbook_name=TEXTBOOK_NAME,
        problems_page_name=PROBLEMS_PAGE_NAME,
        chapter_num=chapter_num,
    )
    solutions_dict[chapter_num] = []
    process.crawl(
        SolutionsSpider,
        solutions_dict=solutions_dict,
        textbook_name=TEXTBOOK_NAME,
        chapter_num=chapter_num,
    )
    time.sleep(3)
process.start()
chapter_num = 0
output_dict = []
while chapter_num in problems_dict and len(problems_dict[chapter_num]) > 0:
    if len(problems_dict[chapter_num]) == len(solutions_dict[chapter_num]):
        for i in range(len(problems_dict[chapter_num])):
            output_dict.append(
                {
                    "chapter_number": chapter_num,
                    "problem": problems_dict[chapter_num][i],
                    "solution": solutions_dict[chapter_num][i],
                }
            )
try:
    os.remove(f"{TEXTBOOK_NAME}.json")
except OSError:
    pass

with open(f"{TEXTBOOK_NAME}.json", "w") as outfile:
    json.dump(output_dict, outfile)
# print(problems_dict)
# print(solutions_dict)
