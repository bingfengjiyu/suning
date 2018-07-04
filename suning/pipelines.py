# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
from suning.items import SuningItem
import json

client=MongoClient()
collection=client["sn"]["sn"]


class SuningPipeline(object):

    def process_item(self, item, spider):
        if isinstance(item,SuningItem):
            print(item)
            collection.insert(dict(item))
            with open("sn.txt","a",encoding="utf-8")as f:
                f.write(json.dumps(dict(item),ensure_ascii=False,indent=4))

        return item
