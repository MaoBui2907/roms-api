# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RomsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    link = scrapy.Field()
    title = scrapy.Field()
    logo = scrapy.Field()
    region = scrapy.Field()
    category = scrapy.Field()
    download_url = scrapy.Field()
    pass
