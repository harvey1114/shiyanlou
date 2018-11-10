# -*- coding: utf-8 -*-
import scrapy
from shiyanlou.items import RepositoryItem


class GithubSpider(scrapy.Spider):
    name = 'github'
    allowed_domains = ['github.com']
    start_urls = ['https://github.com/shiyanlou?tab=repositories']

    def parse(self, response):
        for repository in response.css('div#user-repositories-list ul li'):
            item = RepositoryItem({
                'name':repository.css('div h3 a::text').re_first('\s+(.+)\s*')
                })
            yield item
        text1 = response.xpath('//div[@class="pagination"]/a[1]/text()').extract_first()
        if text1 == 'Next':
            url = response.xpath('//div[@class="pagination"]/a[1]/@href').extract_first()
            yield scrapy.Request(url=url,callback=self.parse)
        elif text1 == 'Previous':
            url = response.xpath('//div[@class="pagination"]/a[2]/@href').extract_first()
            if url is not None:
                yield scrapy.Request(url=url,callback=self.parse)
