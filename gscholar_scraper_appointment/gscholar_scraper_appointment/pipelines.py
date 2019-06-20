# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging

logger = logging.getLogger('scrapy')

# we set the default values in this pipeline step
class DefaultValuesForItem(object):
    def process_item(self, item, spider):
        # if isinstance(item, items.GScholarItem):
        #     item.setdefault('updated_at', ctime())
        return item
