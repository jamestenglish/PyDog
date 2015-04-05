import scrapy


class Dog(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    breed = scrapy.Field()
    age = scrapy.Field()
    size = scrapy.Field()
    desc = scrapy.Field()
    img = scrapy.Field()
    agency = scrapy.Field()
