import scrapy
from bs4 import BeautifulSoup
from item_types import CategorizedItem


# to get the menu items as category from the html below
"""
    <div class="item-list"><ul><li class="first"><a href="/schuelerlexikon/physik/kapitel/1-die-physik-eine-naturwissenschaft"><span>1 Die Physik - eine Naturwissenschaft</span><span class="meta-info">57 Artikel</span></a></li>
    <li><a href="/schuelerlexikon/physik/kapitel/2-mechanik"><span>2 Mechanik</span><span class="meta-info">161 Artikel</span></a></li>
    <li><a href="/schuelerlexikon/physik/kapitel/3-waermelehre"><span>3 Wärmelehre</span><span class="meta-info">73 Artikel</span></a></li>
    <li><a href="/schuelerlexikon/physik/kapitel/4-elektrizitaetslehre"><span>4 Elektrizitätslehre</span><span class="meta-info">235 Artikel</span></a></li>
    <li><a href="/schuelerlexikon/physik/kapitel/5-optik"><span>5 Optik</span><span class="meta-info">86 Artikel</span></a></li>
    <li><a href="/schuelerlexikon/physik/kapitel/6-atom-und-kernphysik"><span>6 Atom- und Kernphysik</span><span class="meta-info">45 Artikel</span></a></li>
    <li class="last"><a href="/schuelerlexikon/physik/kapitel/7-energie-natur-und-technik"><span>7 Energie in Natur und Technik</span><span class="meta-info">27 Artikel</span></a></li>
    </ul></div>
"""


def get_categories(response, level):
    categories = []
    content = response.css('.content .item-list')[0]
    for a in content.xpath('.//a'):
        text = a.xpath('.//span/text()').get()
        categories.append([text[level:len(text)], a.attrib["href"]])
    return categories


class PhysicsTaggedSpider(scrapy.Spider):
    name = "tagged_posts"

    def start_requests(self):
        base_url = "https://www.lernhelfer.de/schuelerlexikon/physik"
        yield scrapy.Request(url=base_url, callback=self.parse)

    def parse(self, response):
        for category in get_categories(response, 1):
            yield self.request_category(category[1], category[0])

    def request_category(self, link, category):
        return scrapy.Request(
            "https://www.lernhelfer.de" + link,
            callback=self.parse_category_page,
            cb_kwargs=dict(category=category)
        )

    def parse_category_page(self, response, category):
        for c in get_categories(response, 4):
            yield self.request_category_articles(category, c[1], c[0])

    def request_category_articles(self, parent, link, category):
        return scrapy.Request(
            "https://www.lernhelfer.de" + link,
            callback=self.parse_category_articles,
            cb_kwargs=dict(parent=parent, category=category)
        )

    def parse_category_articles(self, response, parent, category):
        articles = get_categories(response, 0)
        for article in articles:
            yield self.request_article(parent, category, article[1])

    def request_article(self, parent, category, link):
        return scrapy.Request(
            "https://www.lernhelfer.de" + link,
            callback=self.parse_article,
            cb_kwargs=dict(parent=parent, category=category, link="https://www.lernhelfer.de" + link)
        )

    def parse_article(self, response, parent, category, link):
        content = ""
        body = response.css('.node-lexicon-article')

        content += self.strip_text(body)

        item = CategorizedItem()
        item['parent'] = parent
        item['category'] = category
        item['content'] = content
        item['source'] = link

        return item


    @staticmethod
    def strip_text(selector):
        soup = BeautifulSoup(selector.get())
        striped = ""
        for line in soup.get_text().strip().splitlines():
            striped += line
            striped += " "
        return striped
