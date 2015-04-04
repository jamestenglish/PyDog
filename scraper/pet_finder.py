#http://www.adoptapet.com/dog-adoption/search/75/miles/67218?sex=f&age=puppy
#https://www.petfinder.com/pet-search?location=67218&animal=dog&primary_breed=&age=baby&age=young&gender=female


import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor


class PetFinderSpider(CrawlSpider):
    name = "pet_finder"
    allowed_domains = ["petfinder.com"]

    def __init__(self, zip_code, results, *args, **kw):
        super(PetFinderSpider, self).__init__(*args, **kw)
        self.start_urls = ["https://www.petfinder.com/pet-search?location={}&animal=dog&primary_breed=&age=baby&age=young&gender=female".format(zip_code)]
        self.results = results

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(allow=('category\.php', ), deny=('subsection\.php', ))),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(allow=('petdetail\/\d+.*', )), callback='parse_item'),
    )

    def parse_item(self, response):
        item = scrapy.Item()
        item['url'] = [response.url]

        name = response.xpath('//h1[@class="museo500"]/text()').extract()[0].split(" ")[-1].replace('!', '')
        item['name'] = name

        breed = response.xpath('//div[@class="blue_highlight no_margin top_margin_xlarge"]/ul/li[1]/text()').extract()[0]
        item['breed'] = breed

        age = response.xpath('//div[@class="blue_highlight no_margin top_margin_xlarge"]/ul/li[3]/text()').extract()[0]
        item['age'] = age

        size = response.xpath('//div[@class="blue_highlight no_margin top_margin_xlarge"]/ul/li[4]/text()').extract()[0]
        item['size'] = size

        desc = response.xpath('//div[@class="info_box row"]/div[1]/p[1]/text()').extract()[0]
        item['desc'] = desc

        img = response.xpath('//div[@class="large_image"]/img[1]/@src').extract()[0]
        item['img'] = img

        agency = response.xpath('//span[@class="hdr-14px-bold"]/text()').extract()[0]
        item['agency'] = agency

        self.results.add(item)
