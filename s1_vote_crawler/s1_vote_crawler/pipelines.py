# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

class S1VoteCrawlerPipeline(object):
    def process_item(self, item, spider):
        item_string = json.dumps(str(item).replace('\r\n', ' ').replace('\n', ' ').decode("unicode_escape").encode('utf-8'))
        with open('test.txt', "a") as f:
            f.write(item_string)
            f.write('\r\n')
        # print item_string
        return item
