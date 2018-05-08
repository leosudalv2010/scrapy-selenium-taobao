# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem
import pymongo


class NoTitleFilterPipeline(object):
    def process_item(self, item, spider):
        if not item.get('title'):
            raise DropItem('Found item without title')
        else:
            return item


class DuplicateFilterPipeline(object):
    def __init__(self):
        self.title_seen = []

    def process_item(self, item, spider):
        if (item.get('title'), item.get('shop')) in self.title_seen:
            raise DropItem('Found duplicate item')
        else:
            self.title_seen.append((item.get('title'), item.get('shop')))
            return item


class MongoDBPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient('localhost', 27017)
        self.db = self.client['mydb']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[item.collection].insert_one(dict(item))
        return item


