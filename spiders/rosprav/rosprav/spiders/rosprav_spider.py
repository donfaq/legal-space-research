import scrapy
from bs4 import BeautifulSoup
import re


class RosPravSpider(scrapy.Spider):
    name = 'rosprav'
    start_urls = [
        'https://rospravosudie.com/vidpr-ugolovnoe/etapd-pervaya-instanciya/section-acts'
    ]
    page = 1
    pattern = re.compile('\\n|\\t|\\xa0')

    def parse(self, response):
        last_page = int(
            response.css('div.pagination li a::text').extract()[-1])
        self.log('LAST_PAGE: {}'.format(last_page))

        # follow text links
        for href in response.css('tr td a::attr(href)'):
            yield response.follow(href, self.parse_text)

        # follow pagination links
        self.page = self.page + 1
        while self.page <= last_page:
            yield response.follow(
                '{}/page-{}'.format(self.start_urls[0], self.page),
                callback=self.parse)

    def parse_text(self, response):
        yield {
            'title': list(map(lambda x: BeautifulSoup(x, 'lxml').get_text(),
            response.css('title::text').extract())),
            'table': list(map(lambda x: re.sub(self.pattern, '', x),
            response.xpath('//table[@class="table table-bordered"]').extract())),
            'body': list(map(lambda x:  BeautifulSoup(re.sub(self.pattern, '', x), 'lxml').get_text(),
            response.css('div#dtextdiv').extract())),
        }
