from scrapy import Request

import scrapy
from scrapy.crawler import CrawlerProcess
from multiprocessing import Process, Queue
from twisted.internet import reactor

textbook_solution_dict = {
    "chemistry-2e": "exercises",
    "college-physics-2e": "problems-exercises",
    "college-algebra-2e": "review-exercises",  # also 'practice-test
    "principles-economics-3e": "self-check-questions",
    "american-government-3e": "review-questions",
    "us-history": "review-questions",
    "business-law-i-essentials": "assessment-questions",
}


def run_spider(textbook_name, problems_page_name, chapter_num):
    class ProblemsSpider(scrapy.Spider):
        name = "problems"
        start_urls = [f"https://openstax.org/books/{textbook_name}/pages/{chapter_num}-{problems_page_name}"]

        def parse(self, response):
            body_divs = response.css("div.os-hasSolution div.os-problem-container")
            for body_div in body_divs:
                body_text = body_div.get()
                if body_text:
                    self.outputResponse.append(body_text)
                    yield body_text

    def crawl_webpages(q, spider, outputResponse):
        try:
            runner = scrapy.crawler.CrawlerRunner()
            # global outputResponse
            deferred = runner.crawl(
                spider,
                outputResponse=outputResponse,
            )
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()
            q.put(None)
        except Exception as e:
            q.put(e)

    q = Queue()
    outputResponse = []
    p = Process(target=crawl_webpages, args=(q, ProblemsSpider, outputResponse))
    p.start()
    result = q.get()
    p.join()

    if result is not None:
        raise result

    return outputResponse


if __name__ == "__main__":
    processes = {}
    for textbook in textbook_solution_dict:
        for chapter_number in range(1, 2):
            # output_response = run_spider(
            #     spider=ProblemsSpider,
            #     textbook_name=textbook,
            #     problems_page_name=textbook_solution_dict[textbook],
            #     chapter_num=chapter_num,
            # )
            outputResponseResult = run_spider(
                textbook_name=textbook,
                problems_page_name=textbook_solution_dict[textbook],
                chapter_num=chapter_number,
            )
            print(len(outputResponseResult))
            print(outputResponseResult)
