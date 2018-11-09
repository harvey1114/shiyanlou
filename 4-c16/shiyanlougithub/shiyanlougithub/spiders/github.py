# -*- coding: utf-8 -*-
import scrapy
from shiyanlougithub.items import RepositoryItem


class GithubSpider(scrapy.Spider):
    name = 'github'
    allowed_domains = ['github.com']
    start_urls = [
	'https://github.com/shiyanlou?before=Y3Vyc29yOnYyOpK5MjAxNy0wNi0wNlQxNzozNjoxNSswODowMM4FkpW2&tab=repositories',
        'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNy0wNi0wN1QwNjoxOTo1NyswODowMM4FkpYw&tab=repositories',
        'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNS0wMS0yNVQxMTozMTowNyswODowMM4Bxrsx&tab=repositories',
        'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNC0xMS0yMFQxMzowMzo1MiswODowMM4BjkvL&tab=repositories']


    def parse(self, response):
        for repository in response.css('div#user-repositories-list ul li'):
            item = RepositoryItem({
                'name':repository.css('div h3 a::text').re_first('\s+(.+)\s*'),
                'update_time':repository.css('relative-time::attr(datetime)').extract_first()
                })
            yield item

