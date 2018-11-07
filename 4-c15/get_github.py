import scrapy

class GithubSpider(scrapy.Spider):

    name = 'github'

    @property
    def start_urls(self):
        urls = [
                'https://github.com/shiyanlou?before=Y3Vyc29yOnYyOpK5MjAxNy0wNi0wNlQxNzozNjoxNSswODowMM4FkpW2&tab=repositories',
                'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNy0wNi0wN1QwNjoxOTo1NyswODowMM4FkpYw&tab=repositories',
                'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNS0wMS0yNVQxMTozMTowNyswODowMM4Bxrsx&tab=repositories',
                'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNC0xMS0yMFQxMzowMzo1MiswODowMM4BjkvL&tab=repositories'
                ]
        return urls
    
    def parse(self,response):
        for project in response.css('div#user-repositories-list ul li.public'):
            yield{
                "name":project.xpath('./div[@class="d-inline-block mb-1"]/h3/a/text()').re_first('[\s]*(.+)'),
                "update_time":project.xpath('./div[@class="f6 text-gray mt-2"]/relative-time/@datetime').extract_first()
                    }
