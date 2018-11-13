import csv
import asyncio
import aiohttp
import async_timeout
from scrapy.http import HtmlResponse

results = []

async def fetch(session,url):
    with async_timeout.timeout(30):
        async with session.get(url) as response:
            return await response.text()

def parse(url,body):
    response = HtmlResponse(url=url,body=body)
    for repository in response.css('li.public'):
        name = repository.css('div h3 a::text').re_first('\s+(.+)\s*')
        update_time = repository.css('relative-time::attr(datetime)').extract_first()
        results.append((name,update_time))

async def task(url):
    async with aiohttp.ClientSession() as session:
        content = await fetch(session,url)
        parse(url,content.encode('utf8'))

def main():
    loop = asyncio.get_event_loop()
    url_list = [
            'https://github.com/shiyanlou?before=Y3Vyc29yOnYyOpK5MjAxNy0wNi0wNlQxNzozNjoxNSswODowMM4FkpW2&tab=repositories',
            'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNy0wNi0wN1QwNjoxOTo1NyswODowMM4FkpYw&tab=repositories',
            'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNS0wMS0yNVQxMTozMTowNyswODowMM4Bxrsx&tab=repositories',
            'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNC0xMS0yMFQxMzowMzo1MiswODowMM4BjkvL&tab=repositories']
    tasks = [task(url) for url in url_list]
    loop.run_until_complete(asyncio.gather(*tasks))
    with open('/home/shiyanlou/shiyanlou-repos.csv','w',newline='') as f:
        writer = csv.writer(f)
        writer.writerows(results)

if __name__ == '__main__':
    main()
