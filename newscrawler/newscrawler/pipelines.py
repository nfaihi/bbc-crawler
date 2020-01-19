# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import json


class NewscrawlerPipeline(object):
    def __init__(self):
        # create a connection to mongodb
        self.connection = pymongo.MongoClient(
            'localhost',
            27017
        )

        # create the database
        db = self.connection['news']
        # create a collection into the previous database
        self.collection = db['articles']

    def process_item(self, item, spider):
        # write the received data into a json file
        # to compare it with the one created while scraping
        with open('items.json', 'w') as f:
            f.write(json.dumps(item))

        # insert the data into a mongodb database
        for i in range(0, len(item)):
            self.collection.insert(dict(item[str(i)]))
        return item
