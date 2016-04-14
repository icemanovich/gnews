# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import pymongo


class MongoPipeLine(object):
    def __init__(self, db_host, db_port, db_name, db_subject_name='subjects', db_donor_name='donors'):
        self.mongo_host = db_host
        self.mongo_port = db_port
        self.mongo_db = db_name
        self.collection_subject = db_subject_name
        self.collection_donor = db_donor_name
        self.client = None
        self.db = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            db_host=crawler.settings.get('MONGO_HOST', 'localhost'),
            db_port=crawler.settings.get('MONGO_PORT', '27017'),
            db_name=crawler.settings.get('MONGO_DB', 'yandex'),
            db_subject_name=crawler.settings.get('YANDEX_SUBJECTS', 'subjects'),
            db_donor_name=crawler.settings.get('YANDEX_DONORS', 'donors')
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

        collection_name = self.collection_donor \
            if 'donor' in item.__class__.__name__.lower() \
            else self.collection_subject

        if self.db[collection_name].find({'link': item['link']}).count():
            raise DropItem("Duplicate item {0}".format(item['link']))
        else:
            self.db[collection_name].insert(dict(item))
        return item
