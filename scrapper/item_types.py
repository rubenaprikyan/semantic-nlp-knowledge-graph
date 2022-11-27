import scrapy


class UncategorizedItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    source = scrapy.Field()


class CategorizedItem(scrapy.Item):
    parent = scrapy.Field()
    category = scrapy.Field()
    content = scrapy.Field()
    source = scrapy.Field()
