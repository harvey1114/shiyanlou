# -*- coding: utf-8 -*-
import scrapy
from shiyanlou.items import RepositoryItem


class GithubSpider(scrapy.Spider):
    name = 'github'
    allowed_domains = ['github.com']
    start_urls = ['https://github.com/shiyanlou?tab=repositories']
    
    def parse(self, response):
        for repository in response.css('div#user-repositories-list ul li'):
            item = RepositoryItem()
            item['name'] = repository.css('div h3 a::text').re_first('\s+(.+)\s*'),
            item['update_time'] = repository.css('relative-time::attr(datetime)').extract_first(),
            repository_url = response.urljoin(repository.css('div h3 a::attr(href)').extract_first())
            request = scrapy.Request(repository_url,callback=self.parse_detail)
            request.meta['item'] = item
            yield request
            
        text1 = response.xpath('//div[@class="pagination"]/a[1]/text()').extract_first()
        if text1 == 'Next':
            url = response.xpath('//div[@class="pagination"]/a[1]/@href').extract_first()
            yield scrapy.Request(url=url,callback=self.parse)
        elif text1 == 'Previous':
            url = response.xpath('//div[@class="pagination"]/a[2]/@href').extract_first()
            if url is not None:
                yield scrapy.Request(url=url,callback=self.parse)


    def parse_detail(self,response):
        item = response.meta['item']
        if len(response.css('ul.numbers-summary')) != 0:
            item['commits'] = response.css('li.commits a span::text').re_first('\s+(.+)\s+')
            item['branches'] = response.css('ul.numbers-summary li')[1].css('a span::text').re_first('\s+(.+)\s+')
            item['releases'] = response.css('ul.numbers-summary li')[2].css('a span::text').re_first('\s+(.+)\s+')
        else:
            item['commits'],item['branches'],item['releases'] = '0','0','0'
        yield item
