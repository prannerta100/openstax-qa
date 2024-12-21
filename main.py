# from openai_xml_parser import xml_to_latex

import json

# define spider
import os
import scrapy
import scrapy.crawler as crawler
import logging
from scrapy.utils.log import configure_logging
from multiprocessing import Process, Queue
from twisted.internet import reactor

# 'chemistry-2e', ,
textbook_solution_dict = {
    "chemistry-2e": "exercises",
    # "college-physics-2e": "problems-exercises",
    # "college-algebra-2e": "review-exercises",  # also 'practice-test
    # "principles-economics-3e": "self-check-questions",
    # "american-government-3e": "review-questions",
    # "us-history": "review-questions",
    # "business-law-i-essentials": "assessment-questions",
}
for textbook_name in textbook_solution_dict.keys():
    try:
        os.remove(textbook_name)
    except OSError:
        pass

    class JsonWriterPipeline(object):
        def __init__(self):
            self.file = None

        def open_spider(self, spider):
            self.file = open("scrape_result.jl", "w")

        def close_spider(self, spider):
            self.file.close()

        def process_item(self, item, spider):
            json_string = json.dumps(dict(item)) + "n"
            self.file.write(json_string)
            return item

    class ProblemsSpider(scrapy.Spider):
        name = "quotes"
        start_urls = [
            f"https://openstax.org/books/{textbook_name}/pages/{chapter_num}-{textbook_solution_dict[textbook_name]}"
            for chapter_num in range(1, 2)
        ]
        custom_settings = {
            "LOG_LEVEL": logging.WARNING,
            "ITEM_PIPELINES": {"__main__.JsonWriterPipeline": 1},  # Used for pipeline 1
            "FEED_FORMAT": "json",  # Used for pipeline 2
            "FEED_URI": f"{textbook_name}.json",  # Used for pipeline 2
        }

        def parse(self, response):
            # body_divs = response.css('div[data-type="example"] div.body')
            body_divs = response.css("div.os-hasSolution div.os-problem-container p")
            for body_div in body_divs:
                # Extract all text within the selected div
                # body_text = body_div.css('::text').getall()
                body_text = body_div.get()
                yield {"problem_text": body_text.strip() if body_text else None}

    class SolutionsSpider(scrapy.Spider):
        name = "quotes"
        start_urls = [
            f"https://openstax.org/books/{textbook_name}/pages/chapter-{chapter_num}"
            for chapter_num in range(1, 2)
        ]
        custom_settings = {
            "LOG_LEVEL": logging.WARNING,
            "ITEM_PIPELINES": {"__main__.JsonWriterPipeline": 1},  # Used for pipeline 1
            "FEED_FORMAT": "json",  # Used for pipeline 2
            "FEED_URI": f"{textbook_name}.json",  # Used for pipeline 2
        }

        def parse(self, response):
            # body_divs = response.css('div[data-type="example"] div.body')
            body_divs = response.css(
                'div[data-type="solution"] div.os-solution-container p'
            )
            for body_div in body_divs:
                # Extract all text within the selected div
                # body_text = body_div.css('::text').getall()
                body_text = body_div.get()
                if body_text:
                    yield {"solution_text": body_text.strip() if body_text else None}

    # the wrapper to make it run more times
    def run_spider(spider):
        def f(q):
            try:
                runner = crawler.CrawlerRunner()
                deferred = runner.crawl(spider)
                deferred.addBoth(lambda _: reactor.stop())
                reactor.run()
                q.put(None)
            except Exception as e:
                q.put(e)

        q = Queue()
        p = Process(target=f, args=(q,))
        p.start()
        result = q.get()
        p.join()

        if result is not None:
            raise result

    configure_logging()
    print("first run:")
    run_spider(ProblemsSpider)
    run_spider(SolutionsSpider)
    lines_seen = set()  # holds lines already seen
    outfile_name = f"{textbook_name}_sorted.json"
    try:
        os.remove(outfile_name)
    except OSError:
        pass
    outfile = open(outfile_name, "w")
    for line in open(f"{textbook_name}.json", "r"):
        if line not in lines_seen:  # not a duplicate
            outfile.write(line)
            lines_seen.add(line)
    outfile.close()
