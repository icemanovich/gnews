# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import graphitesend
from scrapy.exceptions import DropItem
import pymongo
import logging


class MongoPipeLine(object):

    """ Graphite """
    g = None

    def __init__(self, db_host, db_port, db_name, yandex_item, graphite):
        """

        :param db_host: str
        :param db_port: str|int
        :param db_name: str
        :param yandex_item: dict
        :param graphite: dict
        """
        self.mongo_host = db_host
        self.mongo_port = db_port
        self.mongo_db = db_name

        self.collection_subject = yandex_item['YANDEX_SUBJECTS']
        self.collection_donor = yandex_item['YANDEX_DONORS']

        self.g = graphitesend.init(
            graphite_server=graphite['GRAPHITE_HOST'],
            graphite_port=graphite['GRAPHITE_PORT'],
            system_name='',
            prefix='yanews',
            suffix='.sum'
        )

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
            },
            graphite={
                'GRAPHITE_HOST': crawler.settings.get('GRAPHITE_HOST', 'graphite.prod'),
                'GRAPHITE_PORT': crawler.settings.get('GRAPHITE_PORT', 2003)
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
            logging.warning("Duplicate item {0}".format(item['link']))
            return None
        else:
            self.db[collection_name].insert(dict(item))

        self.g.send('item.{0}'.format(item_type), 1)

        return item
