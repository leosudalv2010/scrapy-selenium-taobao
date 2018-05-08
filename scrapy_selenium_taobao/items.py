# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
import datetime
from scrapy.loader.processors import MapCompose
import re


class ProductItem(Item):
    collection = 'taobao-product-%s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    keyword = Field()
    title = Field(
        input_processor=MapCompose(str.strip),
    )
    price = Field()
    deal = Field(
        input_processor=MapCompose(lambda i: re.search('\d+', i).group()),
    )
    shop = Field()
    location = Field()
    image = Field()
    page = Field()
