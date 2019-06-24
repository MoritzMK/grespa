# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
from appointment_comparer.scraper.scraper.spiders.author_details import AuthorDetailsSpider
import json
import os
import errno

logger = logging.getLogger('scrapy')

# we set the default values in this pipeline step
class DefaultValuesForItem(object):
    def process_item(self, item, spider):
        # if isinstance(item, items.GScholarItem):
        #     item.setdefault('updated_at', ctime())
        return item

class JsonWriterPipeline(object):

    def __init__(self, data_path):
        self.data_path = data_path

    def from_crawler(cls, crawler):
        data_path = crawler.settings.get("SCRAPED_AUTHORS_PATH")
        return cls(data_path)


    def open_spider(self, spider):
        if not self.checkSpider(spider):
            return
        path = self.data_path.format(spider.author_id)
        if not os.path.exists(os.path.dirname(path)):
            try:
                os.makedirs(os.path.dirname(path))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        self.file = open(path, 'w')

    def process_item(self, item, spider):
        if not self.checkSpider(spider):
            return item
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item

    def close_spider(self, spider):
        if not self.checkSpider(spider):
            return
        self.file.close()

    def checkSpider(self, spider):
        return spider.name == AuthorDetailsSpider.name
