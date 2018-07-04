# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SuningItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    classify=scrapy.Field()
    classify_name=scrapy.Field()
    classify_url=scrapy.Field()
    book_name=scrapy.Field()
    author=scrapy.Field()
    detail_url=scrapy.Field()
    href=scrapy.Field()
    price_url=scrapy.Field()
    price=scrapy.Field()