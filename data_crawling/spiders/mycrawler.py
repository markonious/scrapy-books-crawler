from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class MyCrawlerSpider(CrawlSpider):
    name = "mycrawler"   # <-- this is the name used in `scrapy crawl`
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["http://books.toscrape.com/"]

    rules = (
        Rule(LinkExtractor(allow=r'catalogue/category'), follow=True),
        Rule(LinkExtractor(allow=r'catalogue/.*_.*'), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        yield {
            'title': response.css('div.product_main h1::text').get(),
            'price': response.css('p.price_color::text').get(),
            'availability': response.css('p.availability::text').re_first(r'\w.*\w'),
            'rating': response.css('p.star-rating').attrib['class'].split()[-1],
            'url': response.url
        }
