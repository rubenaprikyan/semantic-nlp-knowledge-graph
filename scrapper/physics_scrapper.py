import scrapy
from bs4 import BeautifulSoup


class ContentItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()


class PhysicsPostSpider(scrapy.Spider):
    name = "posts"

    def start_requests(self):
        pages_count = 23
        urls = ["https://www.weltderphysik.de/service/suche"]
        paginated_url = "https://www.weltderphysik.de/service/suche/?tx_solr%5Bpage%5D={page}"

        for i in range(2, pages_count):
            urls.append(paginated_url.format(page=i))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        count = 0
        for item in response.css('.teaser-text'):
            post = [item.css('a::text').get(), item.css('a::attr(href)').get()]
            count += 1
            yield self.request_page(link=post[1], title=post[0])

    def request_page(self, link, title):
        return scrapy.Request(
            "https://www.weltderphysik.de" + link,
            callback=self.parse_page,
            cb_kwargs=dict(title=title)
        )

    def parse_page(self, response, title):
        text = self.stripText(response.css(".ce-bodytext"))
        item = ContentItem()
        item['title'] = title
        item['content'] = text

        return item

    @staticmethod
    def stripText(selector):
        soup = BeautifulSoup(selector.get())
        return soup.get_text().strip()
