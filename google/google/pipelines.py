# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymongo
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
    """
    Save collected data into MongoDB
    """

    def __init__(self, db_host, db_port, db_name, db_collection):
        self.mongo_host = db_host
        self.mongo_port = db_port
        self.mongo_db = db_name
        self.collection_name = db_collection
        self.client = None
        self.db = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            db_host=crawler.settings.get('MONGO_HOST', 'localhost'),
            db_port=crawler.settings.get('MONGO_PORT', '27017'),
            db_name=crawler.settings.get('MONGO_DB', 'google'),
            db_collection=crawler.settings.get('MONGO_COLLECTION', 'news')
        )

    def open_spider(self, spider):
        if not self.mongo_host:
            raise Exception

        self.client = pymongo.MongoClient(self.mongo_host)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        """
        Filter duplicated items and save it into DB
        """

        if self.db[self.collection_name].find({'url': item['url']}).count():
            raise DropItem("Duplicate item {0}".format(item['url']))
        else:
            self.db[self.collection_name].insert(dict(item))

        return item
