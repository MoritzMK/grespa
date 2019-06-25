# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import re
import urllib.parse

import scrapy
from scrapy.item import Item, Field
from scrapy.loader.processors import TakeFirst, MapCompose

class GScholarItem(Item):
    pass

class AuthorItem(GScholarItem):
    # general author info, when searched with label:biology e.g.
    id = scrapy.Field(output_processor=TakeFirst())
    fields_of_study = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    description = scrapy.Field(output_processor=TakeFirst())
    cited = scrapy.Field(output_processor=TakeFirst(),
                         input_processor=MapCompose(lambda input: re.match('.*([0-9]+)', input).group(1) if input else None))

    # cites table
    cited = scrapy.Field(output_processor=TakeFirst())
    cited_5y = scrapy.Field(output_processor=TakeFirst())
    h_index = scrapy.Field(output_processor=TakeFirst())
    h_index_5y = scrapy.Field(output_processor=TakeFirst())
    i10_index = scrapy.Field(output_processor=TakeFirst())
    i10_index_5y = scrapy.Field(output_processor=TakeFirst())

    # cites diagram
    cite_year_values = scrapy.Field()

    # authors image url
    image_url = scrapy.Field(output_processor=TakeFirst())

class DocItem(GScholarItem):
    title = scrapy.Field(output_processor = TakeFirst())
    id = scrapy.Field(input_processor = MapCompose(lambda i: i.split(':')[-1]),output_processor = TakeFirst())
    authors = scrapy.Field(input_processor = MapCompose(lambda s: s.split(',')))
    published_in = scrapy.Field(output_processor = TakeFirst())
    year = scrapy.Field(output_processor = TakeFirst())
    cite_count = scrapy.Field(input_processor = MapCompose(lambda i : i.strip()),output_processor = TakeFirst())

class VenueItem(GScholarItem):
    title = scrapy.Field(output_processor = TakeFirst())