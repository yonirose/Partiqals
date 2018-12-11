# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class CatsItem(scrapy.Item):
    cat_name = scrapy.Field()
    subcat_names = scrapy.Field()
    subcat_links = scrapy.Field()

    
class PartsItem(scrapy.Item):
    part_num = scrapy.Field()
    manufac = scrapy.Field()
    
