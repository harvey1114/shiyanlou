# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import redis
import json


class FlaskDocPipeline(object):
    def process_item(self, item, spider):
        p1 = re.compile(r'<[^>]+>')
        content = re.sub(p1,'',item['text'])
        p2 = re.compile(r'\s+')
        item['text'] = re.sub(p2,' ',content)
        str = json.dumps(item,default=lambda obj:obj.__dict__)
        self.redis.lpush("flask_doc:items",str)
        return item

    def open_spider(self,spider):
        self.redis = redis.StrictRedis(host='localhost',port=6379,db=0)


