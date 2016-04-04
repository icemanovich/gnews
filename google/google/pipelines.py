# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem


class GoogleJsonPipeLine(object):

    def __init__(self):
        self.file = open('google_data.json', 'w')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()


class MongoPipeLine(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.collection_name = settings['MONGO_COLLECTION']

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(dict(item))
        return item
    # def __init__(self):
    #     connection = pymongo.MongoClient(
    #         settings['MONGO_SERVER'],
    #         settings['MONGO_PORT']
    #     )
    #     db = connection[settings['MONGO_DB']]
    #     self.collection = db[settings['MONGO_COLLECTION']]
    #
    # def process_item(self, item, spider):
    #     valid = True
    #     for data in item:
    #         if not data:
    #             valid = False
    #             raise DropItem("Missing {0}!".format(data))
    #     if valid:
    #         self.collection.insert(dict(item))
    #         # log.msg("Question added to MongoDB database!",
    #         #         level=log.DEBUG, spider=spider)
    #     return item
