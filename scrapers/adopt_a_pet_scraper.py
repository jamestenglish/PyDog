from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapers.models.dog import Dog


class AdoptAPetSpider(CrawlSpider):
    name = "adopt_a_pet"
    allowed_domains = ["adoptapet.com"]

    def __init__(self, zip_code, *args, **kw):
        super(AdoptAPetSpider, self).__init__(*args, **kw)
        self.start_urls = ["http://www.adoptapet.com/dog-adoption/search/75/miles/{}?sex=f&age=puppy".format(zip_code)]
        # self.results_queue = results_queue

    rules = (
        Rule(LinkExtractor(allow=('pet/\d+.*', )), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = Dog()
        item['url'] = [response.url]
        self.log("####{}".format(response.url))
        self.log("@@@@{}".format(self.start_urls[0]))
        if response.url == self.start_urls[0]:
            self.log("!!!!skip!")
            return

        name = response.xpath('//h1[@class="museo500"]/text()').extract()[0].split(" ")[-1].replace('!', '')
        item['name'] = name

        breed = response.xpath('//div[@class="blue_highlight no_margin top_margin_xlarge"]/ul/li[1]/text()').extract()[0]
        item['breed'] = breed

        age = response.xpath('//div[@class="blue_highlight no_margin top_margin_xlarge"]/ul/li[3]/text()').extract()[0]
        item['age'] = age

        size = response.xpath('//div[@class="blue_highlight no_margin top_margin_xlarge"]/ul/li[4]/text()').extract()[0]
        item['size'] = size

        try:
            desc = response.xpath('//div[@class="info_box row"]/div[1]/p[1]/text()').extract()[0]
            item['desc'] = desc
        except:
            try:
                desc = response.xpath('//div[@class="info_box row"]//div[@class="body"]/text()').extract()[0]
                item['desc'] = desc
            except:
                item['desc'] = ''

        img = response.xpath('//div[@class="large_image"]/img[1]/@src').extract()[0]
        item['img'] = img

        agency = response.xpath('//span[@class="hdr-14px-bold"]/text()').extract()[0]
        item['agency'] = agency

        yield item
