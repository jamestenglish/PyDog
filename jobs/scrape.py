from rq.decorators import job
from redis_queue import q
from db import db
import sys
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from scraper.adopt_a_pet_scraper import AdoptAPetSpider
from scraper.pet_finder import PetFinderSpider
from scrapy.utils.project import get_project_settings
from Queue import Queue


def setup_adopt_a_pet(zip_code, results_queue):
    spider = AdoptAPetSpider(zip_code=zip_code, results=results_queue)
    settings = get_project_settings()
    crawler = Crawler(settings)
    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()


def setup_pet_finder(zip_code, results_queue):
    spider = PetFinderSpider(zip_code=zip_code, results=results_queue)
    settings = get_project_settings()
    crawler = Crawler(settings)
    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    crawler.configure()
    crawler.crawl(spider)
    crawler.start()

@job(queue=q)
def scrape(job_id):
    try:
        _scrape()

    except:  # if ANYTHING goes wrong with the job we want to update the job db
        error_str = sys.exc_info()[0]
        update = {'$set': {
            'done': True,
            'percent': 100,
            'error': error_str
        }}
        db.find_one_and_update({'job_id', job_id}, update)
    pass


def _scrape():
    results_queue = Queue()
    zip_code = 67218

    setup_adopt_a_pet(zip_code, results_queue)
    setup_pet_finder(zip_code, results_queue)

    log.start()
    reactor.run()  # the script will block here until the spider_closed signal was sent

    results = []

    while not results_queue.empty():
        results.append(results_queue.get())

    return results