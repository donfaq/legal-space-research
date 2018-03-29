import scrapy
from bs4 import BeautifulSoup
import re


class RosPravSpider(scrapy.Spider):
    name = 'rosprav'

    def __init__(self, start_page, last_page, *args, **kwargs):
        super(RosPravSpider, self).__init__(*args, **kwargs)
        self.current_page = int(start_page)
        self.last_page = int(last_page)
        self.base_url = 'https://rospravosudie.com/vidpr-ugolovnoe/etapd-pervaya-instanciya/section-acts/page-{}/'
        self.start_urls = [self.base_url.format(self.current_page)]
        self.pattern = re.compile('\\n|\\t|\\xa0')
        self.article_count = 0


    def parse(self, response):
        self.logger.info('PAGE: {}'.format(response.url))
        # follow text links
        for href in response.css('tr td a::attr(href)'):
            yield response.follow(href, self.parse_text)

        # follow pagination links
        self.current_page = self.current_page + 1
        while self.current_page <= self.last_page:
            yield response.follow(
                self.base_url.format(self.current_page),
                callback=self.parse)

    def parse_text(self, response):
        self.article_count += 1
        self.logger.info('ARTICLE-{count}: {url}'.format(count=self.article_count, url=response.url))
        yield {
            'title': list(map(lambda x: BeautifulSoup(x, 'lxml').get_text(),
            response.css('title::text').extract())),
            'table': list(map(lambda x: re.sub(self.pattern, '', x),
            response.xpath('//table[@class="table table-bordered"]').extract())),
            'body': list(map(lambda x:  BeautifulSoup(re.sub(self.pattern, '', x), 'lxml').get_text(),
            response.css('div#dtextdiv').extract())),
        }
