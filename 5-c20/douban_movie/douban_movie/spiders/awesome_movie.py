# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule,CrawlSpider
from scrapy.linkextractors import LinkExtractor
from douban_movie.items import MovieItem


class AwesomeMovieSpider(CrawlSpider):
    name = 'awesome-movie'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/subject/3011091/']

    rules = (
        Rule(LinkExtractor(restrict_css='div.recommendations-bd dl dt a'),callback='parse_page',follow=True),
    )

    def parse_movie_item(self,response):
        item = MovieItem()
        item['score'] = response.css('strong.rating_num::text').extract_first()
        #if float(item['score']) > 8.0:
        item['url'] = response.url
        item['name'] = response.css('div#content h1 span::text').extract_first()
        item['summary'] = response.xpath('//span[@property="v:summary"]/text()').extract_first()
        return item

    def parse_start_url(self,response):
        yield self.parse_movie_item(response)

    def parse_page(self,response):
        yield self.parse_movie_item(response)

        
