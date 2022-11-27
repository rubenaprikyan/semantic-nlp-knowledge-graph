import scrapy
from bs4 import BeautifulSoup
from item_types import UncategorizedItem


class PhysicsPostSpider(scrapy.Spider):
    name = "posts"

    def start_requests(self):
        pages_count = 12
        urls = ["https://www.weltderphysik.de/service/suche"]
        paginated_url = "https://www.weltderphysik.de/service/suche/?tx_solr%5Bpage%5D={page}"

        for i in range(2, pages_count):
            urls.append(paginated_url.format(page=i))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for item in response.css('.teaser-text'):
            post = [item.css('a::text').get(), item.css('a::attr(href)').get()]
            yield self.request_page(link=post[1], title=post[0])

    def request_page(self, link, title):
        return scrapy.Request(
            "https://www.weltderphysik.de" + link,
            callback=self.parse_page,
            cb_kwargs=dict(title=title, link="https://www.weltderphysik.de" + link)
        )

    def parse_page(self, response, title, link):
        text = self.stripText(response.css(".ce-bodytext"))
        item = UncategorizedItem()
        item['title'] = title
        item['content'] = text
        item['source'] = link

        return item

    @staticmethod
    def stripText(selector):
        soup = BeautifulSoup(selector.get())
        striped = ""
        for line in soup.get_text().strip().splitlines():
            striped += line
            striped += " "
        return striped
