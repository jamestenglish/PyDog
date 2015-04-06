from rq.decorators import job
from redis_queue import q
from db import db
import sys
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, project, signals
from scrapers.adopt_a_pet_scraper import AdoptAPetSpider
from scrapers.pet_finder_api import PetFinderApi
from scrapy.utils.project import get_project_settings
from pprint import pprint
import settings

from billiard import Process
from billiard.queues import JoinableQueue


def remove_ids(ids_to_remove):
    for mongo_id in ids_to_remove:
        db.dogs.remove({'_id': mongo_id})


def add_items(items_to_add):
    for item in items_to_add:
        db.dogs.insert(dict(item))


@job(queue=q)
def scrape(job_id):
    try:
        zip_code = settings.ZIP_CODE
        scrape_results = _scrape(zip_code)
        scrape_results = collapse_duplicates(scrape_results)
        db_dogs = list(db.dogs.find({}))

        ids_to_remove = get_ids_to_remove(scrape_results, db_dogs)
        print("Removing {}".format(len(ids_to_remove)))
        items_to_add = get_items_to_add(scrape_results, db_dogs)
        print("Adding {}".format(len(items_to_add)))

        remove_ids(ids_to_remove)
        add_items(items_to_add)
        print("Done")

        update = {'$set': {'done': True,
                           'percent': 100}}
        db.jobs.update({'job_id': job_id}, update)

    except:  # if ANYTHING goes wrong with the job we want to update the job db
        error_str = sys.exc_info()[0]
        pprint(sys.exc_info())
        update = {'$set': {
            'done': True,
            'percent': 100,
            'error': error_str
        }}
        db.jobs.update({'job_id': job_id}, update)


class UrlCrawlerScript(Process):
        def __init__(self, spider, result_queue):
            Process.__init__(self)
            settings = get_project_settings()
            self.crawler = Crawler(settings)
            self.result_queue = result_queue

            if not hasattr(project, 'crawler'):
                self.crawler.install()
                self.crawler.configure()
                self.crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
                self.crawler.signals.connect(self._item, signal=signals.item_scraped)

            self.spider = spider

        def _item(self, item, response, spider):
            self.result_queue.put(item)

        def run(self):
            self.crawler.crawl(self.spider)
            self.crawler.start()
            reactor.run()


def _scrape(zip_code):
    print("Running Adopt A Pet")
    results = _scrape_spider(AdoptAPetSpider(zip_code))
    print("Done")

    print("Running Pet Finder")
    pet_finder_api = PetFinderApi(zip_code)
    print("Done")
    results.extend(pet_finder_api.find_dog_items())

    return results


def _scrape_spider(spider):
    results_queue = JoinableQueue()
    crawler = UrlCrawlerScript(spider, results_queue)
    crawler.start()
    crawler.join()

    results = []

    while not results_queue.empty():
        item = results_queue.get()
        results_queue.task_done()
        results.append(item)

    return results


def get_ids_to_remove(results, db_results):
    results_hash = create_duplicates_hash(results)
    db_hash = create_duplicates_hash(db_results)

    results_key_set = set(results_hash.keys())
    db_key_set = set(db_hash.keys())

    difference = db_key_set.difference(results_key_set)

    ids_to_remove = []
    for key in difference:
        ids_to_remove.append(db_hash[key][0]['_id'])

    return ids_to_remove


def get_items_to_add(results, db_results):
    results_hash = create_duplicates_hash(results)
    db_hash = create_duplicates_hash(db_results)

    results_key_set = set(results_hash.keys())
    db_key_set = set(db_hash.keys())

    difference = results_key_set.difference(db_key_set)

    items_to_add = []
    for key in difference:
        items_to_add.extend(results_hash[key])

    return items_to_add


def collapse_duplicates(results):
    duplicates_hash = create_duplicates_hash(results)

    collapsed = []
    for key, items in duplicates_hash.iteritems():
        if len(items) == 1:
            collapsed.extend(items)
        else:
            urls = []
            for item in items:
                urls.extend(item['url'])

            item = items[0]
            item['url'] = urls
            collapsed.append(item)

    return collapsed


def create_duplicates_hash(results):
    duplicates_hash = {}
    for item in results:
        key = "{}|{}".format(item['name'], item['agency'][:15])
        if key not in duplicates_hash:
            duplicates_hash[key] = []

        duplicates_hash[key].append(item)

    return duplicates_hash