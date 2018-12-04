# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 12:41:37 2016

@author: jrosenfe
v2
"""

import os
from urllib.parse import urljoin, urlparse
from collections import defaultdict
import pickle

import scrapy
#from ..items import CatsItem

import db_setup as db
from dist.digikey import xpath_select as xp
from dist.digikey import init_pages as init
from utils.misc import replace_illchar
from utils.progress import print_prog

import logging
log = logging.getLogger('scrapy.Spider')


class DigiekeyCount(scrapy.Spider):
    name = "digikey_prepnew"
    custom_settings = {
        'LOG_FILE': os.path.join('..', '..', '..', 'logs',
                                 f'{name}_scrapy.log')
    }
    open(os.path.join('..', '..', '..', 'logs', f'{name}_scrapy.log'),
                      'w').close()
    
    current_count = 0
    total_subcats = len(init.cats)
    base_path = os.path.join('..', '..', '..', 'dist', name.split('_')[0])
    cat_tree = defaultdict(set)
    base_url = init.start_url[0]
    start_urls = init.start_url
    print('Initializing...', end='\r')

    def cat_required(self, link):
        for ignore_cat in init.ignore_cats:
            if ignore_cat in link:
                return False
        return True
    
    def update_prog(self, prog_bar=True):
        counts = db.prepdb.find_one({'dist': self.name.split('_')[0],
                                     'current_count': {'$exists': 1}})
        if prog_bar:
            print_prog(self.name+' progress', counts['current_count'],
                       counts['total_count'], left_just=20, endwith='\r')
        return (counts['current_count'], counts['total_count'])
    
    def parse(self, response):
        first_count = 1
        if not db.prepdb.find_one():
            for cat in init.cats:
                subcat_names = response.xpath(xp.INIT_SUBCAT_NAMES % f'/{cat}').extract()
                subcat_links = response.xpath(xp.INIT_SUBCAT_LINKS % f'/{cat}').extract()
                
                for subcat_name, subcat_link in zip(subcat_names, subcat_links):
                    if self.cat_required(subcat_link):
                        url = urljoin(self.base_url, subcat_link)
                        db.prepdb.insert_one({'dist': self.name.split('_')[0],
                                              'link': url,
                                              'path': urlparse(url).path})
            first_count = 0
        else:
            with open(os.path.join('..', '..', '..',
                                   'dist', self.name.split('_')[0],
                                   'temp_cat_tree.pickle'), 'rb') as f:
                self.__class__.cat_tree = pickle.load(f)
        
        db.prepdb.update_one(
                {'dist': self.name.split('_')[0],
                 'current_count': {'$exists': 1}},
                {'$set': {'current_count': 0,
                          'total_count': db.prepdb.count_documents({}) - first_count}},
                upsert=True
            )
        
        self.update_prog()
        for start_link in db.prepdb.find({'dist': self.name.split('_')[0],
                                          'link': {'$exists': 1}}):
            yield scrapy.Request(url=start_link['link'], callback=self.drill_down)

    def drill_down(self, response):
        subcat_names = response.xpath(xp.DRILL_SUBCAT_NAMES).extract()
        subcat_links = response.xpath(xp.DRILL_SUBCAT_LINKS).extract()
        
        if subcat_names:
           for subcat_name, subcat_link in zip(subcat_names, subcat_links):
               if self.cat_required(subcat_link):
                   url = urljoin(self.base_url, subcat_link)
                   db.prepdb.insert_one({'dist': self.name.split('_')[0],
                                         'link': url,
                                         'path': urlparse(url).path})
                   db.prepdb.update_one({'dist': self.name.split('_')[0],
                                         'total_count': {'$exists': 1}},
                                        {'$inc': {'total_count': 1}})
                   
                   self.update_prog()
            
                   yield scrapy.Request(url=url, callback=self.drill_down)
        else:
           cat_name = replace_illchar(response.xpath(xp.BREAD_CRUMBS1).extract_first())
           subcat_name = replace_illchar(response.xpath(xp.BREAD_CRUMBS2).extract()[-1])
         
           self.__class__.cat_tree[cat_name].add(subcat_name)
           self.update_counts(cat_name,
                              replace_illchar(response.xpath(xp.PREP_COUNTS).extract_first(),
                                              to_type=int
                                      ),
                              subcat_name,
                              response.url)
    
    def closed(self, reason):
        print('\n')
        count, tot_count = self.update_prog(prog_bar=False)
        if count == tot_count:
            with open(os.path.join(self.base_path, 'part_tree_latest.py'), 'wt') as f:
                headers = ['import os', 'import sys',
                           'from collections import defaultdict',
                           'import mycat_tree as mt',
                           'cat_tree = defaultdict(dict)']
                for header in headers:
                    f.write(header+'\n')
                    
                for cat, subcats in self.__class__.cat_tree.items():
                    headers = ["myrootcat = ''\n", "mycat = ''\n",
                               "mysubcat = mt.mytree[myrootcat][mycat]\n\n",
                               "subcats = [\n"]
                    for header in headers:
                        f.write(header)
                    for subcat in subcats:
                        f.write(f"{' '*4}'{subcat}',\n")
                    f.write(']\n')
                    headers = [f"mysub_idx = [{' ,'*len(subcats)}]\n",
                               'for idx, subcat in zip(mysub_idx, subcats):\n']
                    for header in headers:
                        f.write(header)
                    f.write(f"{' '*4}cat_tree['{cat}'][subcat] = {{'myrootcat': myrootcat, 'mycat': mycat, 'mysubcat': mysubcat[idx]}}\n\n")
        else:
            with open(os.path.join('..', '..', '..', 'dist',
                                   self.__class__.name.split('_')[0],
                                   'temp_cat_tree.pickle'), 'wb') as f:
                pickle.dump(self.__class__.cat_tree, f)
            
    def update_counts(self, cat_name, part_count, subcat_name, url):
        ucat = f'{cat_name}__{subcat_name}'
        db.cursordb.update_one({'dist': self.name.split('_')[0], 'ucat': ucat},
                               {'$setOnInsert': {'dist': self.name.split('_')[0],
                                                 'ucat': ucat},
                                '$set': {'start_link': url,
                                         'current_link': url,
                                         'current_count': 0,
                                         'total_count': part_count, 
                                         'scan_complete': False}},
                               upsert=True)
        
        self.update_prog()
    
            
        
