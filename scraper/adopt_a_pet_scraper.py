#http://www.adoptapet.com/dog-adoption/search/75/miles/67218?sex=f&age=puppy
#https://www.petfinder.com/pet-search?location=67218&animal=dog&primary_breed=&age=baby&age=young&gender=female


import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
import json
from functools import partial


class AdoptAPetSpider(CrawlSpider):
    name = "adopt_a_pet"
    allowed_domains = ["adoptapet.com"]

    def __init__(self, zip_code, results, *args, **kw):
        super(AdoptAPetSpider, self).__init__(*args, **kw)
        self.start_urls = ["http://www.adoptapet.com/dog-adoption/search/75/miles/{}?sex=f&age=puppy".format(zip_code)]
        self.results = results

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(allow=('category\.php', ), deny=('subsection\.php', ))),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(allow=('pet\/\d+.*', )), callback='parse_ajax'),
    )

    def parse_ajax(self, response):
        pet_id = response.url.split('/')[-2]
        scrapy.Request('https://www.petfinder.com/v1/pets/{}.json?api_key=98719f8ded45b41f3153f5736d55d162'.format(pet_id),
                       callback=partial(self.parse_item, original_response=response))
        pass


    def parse_item(self, response, original_response):
        item = scrapy.Item()
        item['url'] = [original_response.url]
        data = json.loads(response.body)

        data['results'][0]['name']

        name = data['results'][0]['name']
        item['name'] = name

        breed = data['results'][0]['primary_breed']
        item['breed'] = breed

        age = data['results'][0]['age']
        item['age'] = age

        size = data['results'][0]['size']
        item['size'] = size

        desc = data['results'][0]['description']
        item['desc'] = desc

        img = "https://drpem3xzef3kf.cloudfront.net{}".format(data['results'][0]['pet_photo'][0])
        item['img'] = img

        agency = data['results'][0]['shelter_name']
        item['agency'] = agency

        self.results.add(item)
