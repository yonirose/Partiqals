# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 12:41:37 2016

@author: jrosenfe
v2
"""

import os
import time

import scrapy
#from scrapy.settings import Settings
from ..items import catsItem

import db_setup as db
from dist.digikey import xpath_select as xp
from dist.digikey import init_pages as init
from utils.misc import replace_illchar
from utils.progress import print_prog

class DigikeyCount(scrapy.Spider):
    name = "digikey_prep"
    custom_settings = {
        'LOG_FILE': os.path.join('..', '..', '..', 'logs',
                                 '%s_scrapy.log' % name)
    }
    open(os.path.join('..', '..', '..', 'logs','%s_scrapy.log' % name), 'w').close()
    
    print('Initializing...', end='\r')
    
    subcats_count = 0
    total_subcats = 0
    start_urls = init.start_urls
    base_path = os.path.join('..', '..', '..', 'dist', 'digikey')
    
    def parse(self, response):
        headers = ['import os', 'import sys',
                   'from collections import defaultdict',
                   'import mycat_tree as mt',
                   '\n\nclass PartTree():',
                   '    cat_tree = defaultdict(dict)']
        with open(os.path.join(self.base_path, 'part_tree_latest.py'), 'wt') as f:
            for header in headers:
                f.write(header+'\n')
        headers = ["myrootcat = ''\n", "mycat = ''\n",
                  "mysubcat = mt.mytree[myrootcat][mycat]\n\n",
                  "subcats = ["]

        for cat in init.cats:
            cat = '/'+cat+'/'
            DigikeyCount.total_subcats += len(response.xpath(xp.PREP_SUBCAT % cat).extract())
        print_prog('Progress', DigikeyCount.subcats_count,
                   DigikeyCount.total_subcats, left_just=15, endwith='\r')

        with open(os.path.join(self.base_path, 'part_tree_latest.py'), 'at') as f:
            for cat in init.cats:
                cat = '/'+cat+'/'
                cat_name = replace_illchar(response.xpath(xp.PREP_CATNAME % cat).extract_first())
                subcat_links = response.xpath(xp.PREP_SUBCAT_LINK % cat).extract()
                subcat_names = response.xpath(xp.PREP_SUBCAT_NAMES % cat).extract()
                
                for header in headers:
                    f.write(' '*4+header)
                
                for subcat_link, subcat_name in zip(subcat_links, subcat_names):
                    f.write(' '*15+"'%s',\n" % replace_illchar(subcat_name))
                    item = catsItem()
                    item['cat_name'] = cat_name
                    item['subcat_name'] = replace_illchar(subcat_name)
                    yield scrapy.Request(url='https://www.digikey.com'+subcat_link,
                                         callback=self.update_counts, meta={'item': item})
                f.write(']\n')
                f.write(' '*4+'mysub_idx = ['+' ,'*(len(subcat_names)-1)+']\n')
                f.write(' '*4+'for idx, subcat in zip(mysub_idx, subcats):\n')
                f.write(' '*8+"cat_tree['%s'][subcat] = {'myrootcat': myrootcat, \
                        'mycat': mycat, 'mysubcat': mysubcat[idx]}\n\n" % cat_name)

    def update_counts(self, response):
        ucat = response.meta['item']['cat_name'] + '__' + response.meta['item']['subcat_name']
        db.cursordb.update_one({'dist': DigikeyCount.name,'ucat': ucat},
                               {'$setOnInsert': {'dist': DigikeyCount.name.split('_')[0],
                                                 'ucat': ucat},
                                '$set': {'start_link': response.url,
                                         'current_link': response.url,
                                         'current_count': 0,
                                         'total_count': int(response.xpath(xp.CAT_COUNT).extract_first().replace(',', '')),
                                         'scan_complete': False}}, upsert=True)

        DigikeyCount.subcats_count += 1
        print_prog('Progress', DigikeyCount.subcats_count,
                   DigikeyCount.total_subcats, left_just=15, endwith='\r')

            
        
