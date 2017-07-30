# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ThreadItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    posts = scrapy.Field()

class PostItem(scrapy.Item):
    number = scrapy.Field()
    name = scrapy.Field()
    date = scrapy.Field()
    uid = scrapy.Field()
    message = scrapy.Field()
