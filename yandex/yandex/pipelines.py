# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import logging
from statistics import Statistics
# from scrapy.exceptions import DropItem


class MongoPipeLine(object):
    """
    Save collected items into MongoDb
    """

    def __init__(self, db_host, db_port, db_name, yandex_item):
        """
        :param db_host: str
        :param db_port: str|int
        :param db_name: str
        :param yandex_item: dict
        """
        self.mongo_host = db_host
        self.mongo_port = db_port
        self.mongo_db = db_name

        self.collection_subject = yandex_item['YANDEX_SUBJECTS']
        self.collection_donor = yandex_item['YANDEX_DONORS']

        self.client = None
        self.db = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            db_host=crawler.settings.get('MONGO_HOST', 'localhost'),
            db_port=crawler.settings.get('MONGO_PORT', '27017'),
            db_name=crawler.settings.get('MONGO_DB', 'yandex'),
            yandex_item={
                'YANDEX_SUBJECTS': crawler.settings.get('YANDEX_SUBJECTS', 'subjects'),
                'YANDEX_DONORS': crawler.settings.get('YANDEX_DONORS', 'donors')
            }
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
        item_type = 'subject'
        collection_name = self.collection_subject

        if 'donor' in item.__class__.__name__.lower():
            collection_name = self.collection_donor
            item_type = 'donor'

        if self.db[collection_name].find({'link': item['link']}).count():
            '''
            Output all object - too much
            raise DropItem("Duplicate item {0}".format(item['link']))
            '''
            raise DropItem("Duplicate item {0}".format(item['link']))
            # logging.warning("Duplicate item {0}".format(item['link']))
            # return None

        else:
            self.db[collection_name].insert(dict(item))

        Statistics.init().send('saved.{0}'.format(item_type), 1)

        return item
