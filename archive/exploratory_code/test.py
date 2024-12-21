import scrapy
import scrapy.crawler as crawler
from multiprocessing import Process, Queue
from twisted.internet import reactor

ANSWER_LIST = {}
# your spider
class QuotesSpider(scrapy.Spider):
    name = "quotes"

    start_urls = ['http://quotes.toscrape.com/tag/humor/']
    def parse(self, response):
        response.css("div.os-hasSolution div.os-problem-container p")
        # for quote in response.css('div.quote'):
            # global ANSWER_LIST
            # print(quote.css('span.text::text').extract_first())
            # self.outputResponse["text"] = (quote.css('span.text::text').extract_first())


def f(q, spider):
    try:
        runner = crawler.CrawlerRunner()
        deferred = runner.crawl(spider)
        deferred.addBoth(lambda _: reactor.stop())
        reactor.run()
        q.put(None)
    except Exception as e:
        q.put(e)

    return q


# the wrapper to make it run more times
def run_spider(spider):
    q = Queue()
    p = Process(target=f, args=(q, spider))
    p.start()
    result = q.get()
    p.join()

    if result is not None:
        raise result


if __name__ == "__main__":
    print('first run:')
    run_spider(QuotesSpider)
    # print(ANSWER_LIST)
    # print('\nsecond run:')
    # run_spider(QuotesSpider)
