# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class catsItem(scrapy.Item):
    cat_name = scrapy.Field()
    subcat_name = scrapy.Field()
    
class partsItem(scrapy.Item):
    part_num = scrapy.Field()
    manufac = scrapy.Field()
    
