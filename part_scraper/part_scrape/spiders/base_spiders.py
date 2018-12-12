# -*- coding: utf-8 -*-
"""
Created on Sun Dec 2 13:38:39 2018

@author: jrosenfe
"""
import os
import datetime
import time
from collections import defaultdict
from random import shuffle
from urllib.parse import urljoin, urlparse
import pickle

import scrapy
from ..items import PartsItem

from utils.misc import replace_illchar
from utils.progress import print_prog
import analyzer.line_parser as lp
import analyzer.analyze_html as ah
from utils.misc import get_ngrams
import db_setup as db
import config as cfg
from utils.error_logging import ErrorHandler


class PrepBaseMixin:
    
    current_count = 0
    cat_tree = defaultdict(set)
    
    def __init__(self, xpath_select, init):
        super().__init__()
        self.xp = xpath_select
        self.init = init
    
    def bread_crumbs(self, response):
        raise NotImplementedError
    
    def cat_required(self, link):
        for ignore_cat in self.init.ignore_cats:
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
            for cat in self.init.cats:
                subcat_names = response.xpath(self.xp.INIT_SUBCAT_NAMES % f'/{cat}').extract()
                subcat_links = response.xpath(self.xp.INIT_SUBCAT_LINKS % f'/{cat}').extract()
                
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
        subcat_names = response.xpath(self.xp.DRILL_SUBCAT_NAMES).extract()
        subcat_links = response.xpath(self.xp.DRILL_SUBCAT_LINKS).extract()
        
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
           cat_name, subcat_name = self.bread_crumbs(response)
           self.__class__.cat_tree[cat_name].add(subcat_name)
           self.update_counts(
                   cat_name,
                   replace_illchar(
                           response.xpath(self.xp.PREP_COUNTS).extract_first(),
                           to_type=int),
                   subcat_name,
                   response.url
            )
    
    def closed(self, reason):
        print('\n')
        count, tot_count = self.update_prog(prog_bar=False)
        if count == tot_count:
            with open(os.path.join(self.base_path, 'part_tree_latest.py'), 'at') as f:
                headers = [f"{time.strftime('%m/%d/%Y')}, {time.strftime('%H:%M:%S')}\n",
                           'import os', 'import sys',
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
            db.prepdb.drop()      
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


class MainBaseMixin:
    
    prog_count = 0
    total_count = 0
    batch_count = 0  
    
    def __init__(self, start_row_idx, xpath_select, part_tree):
        super().__init__()
        self.xp = xpath_select
        self.pt = part_tree
        self.start_row_idx = start_row_idx
        
        self.docs = ah.MongoDocCreator()
        self.text_to = lp.Parser()
        self.err_to = ErrorHandler()
  
    def bread_crumbs(self, response):
        raise NotImplementedError
        
    def clean_pdf_link(self, pdf_link):
        raise NotImplementedError
        
    def process_misc_data(self, text, part_num, misc_data):
        raise NotImplementedError
        
    def start_requests(self):
        start_links = []
        headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                                 AppleWebKit/537.36 (KHTML, like Gecko) \
                                 Chrome/66.0.3359.139 Safari/537.36'}
        
        for cat in db.cursordb.find({'dist': self.name}):
            if not cat['scan_complete']:
                start_links.append(cat['current_link'])
                self.__class__.total_count += cat['total_count']
                self.__class__.prog_count += cat['current_count']
        if self.total_count == 0:
            print('Run prep-spider to obtain initial data')
            os.rename(os.path.join('.', '.start_spider'),
                      os.path.join('.', '.stop_spider'))
            raise scrapy.exceptions.CloseSpider('No initial data')
        
        print_prog(self.name+' total progress', self.__class__.prog_count,
                   self.__class__.total_count, left_just=20, endwith='')
        print_prog(' '*5+'Progress', self.__class__.batch_count, cfg.BATCH_SIZE,
                   left_just=5, bar_length=20, endwith='\r')
        shuffle(start_links)
        for start_link in start_links:
            yield scrapy.Request(start_link, headers=headers)

    def parse(self, response):
        if os.path.isdir('.stop_spider'):
            print(f'\nStop crawling spider {self.name}')
            raise scrapy.exceptions.CloseSpider('Stopped by user')
        
        cat, subcat = self.bread_crumbs(response)
        
        table_len = len(response.xpath(self.xp.TABLE_LEN))
        
        table_heads = {}
        idx = self.xp.HEAD_START_IDX
        while True:
            head = response.xpath(self.xp.HEAD_TITLE % idx).extract()
            if head:
                table_heads[idx] = head[0].strip()
                idx += 1
            else:
                break
        try:
            for idx in range(self.start_row_idx, table_len+1):
                part = {
                        'part_num': replace_illchar(response.xpath(self.xp.PART_NUM % idx).extract_first().strip()),
                        'dist_num': response.xpath(self.xp.DIST_NUM % idx).extract_first().strip(),
                        'manufac': replace_illchar(response.xpath(self.xp.MANUFAC % idx).extract_first()),
                        'descr': response.xpath(self.xp.DESCR % idx).extract_first().strip(),
                        'unit_price': replace_illchar(response.xpath(self.xp.UNIT_PRICE % idx).extract_first().strip()),
                        'dist': self.name,
                        'dist_partlink': urljoin(self.base_url, response.xpath(self.xp.DIST_LINK % idx).extract_first()),
                        'pdf_link': response.xpath(self.xp.PDF_LINK % idx).extract_first(),
                        'min_quan': response.xpath(self.xp.MIN_QUAN % idx).extract_first().strip().replace(',', ''),
                        'date_scraped': datetime.datetime.utcnow()
                    }
                for title_idx, table_title in table_heads.items():
                    misc_data = response.xpath(self.xp.MISC_DATA % (idx, title_idx)).extract_first().strip()
                    if misc_data:
                        docs = self.process_misc_data(f'{table_title} {misc_data}',
                                                      part['part_num'],
                                                      misc_data)
                        
                        for sub_idx, doc in enumerate(docs):
                            col = '%s.%s' % (title_idx, sub_idx)
                            doc = {**doc, **{'direct': 'v', 'manufac': part['manufac'],
                                             'page_num': 0, 'part_num': part['part_num'],
                                             'dist_num': part['dist_num'], 'col': col,
                                             }}
                            doc['word'] += get_ngrams(doc['part_num']) \
                                           + get_ngrams(doc['manufac'])
                            db.partdb.update_one({'dist_num': part['dist_num'],
                                                  'col': col},
                                                  {'$setOnInsert': doc}, upsert=True)
            
                for _ in [('unit_price', float), ('min_quan', int)]:
                    try:
                        part[_[0]] = _[1](part[_[0]])
                    except ValueError:
                        if not part[_[0]]:
                           part[_[0]] = 'See distributer'
                
                part['pdf_link'] = self.clean_pdf_link(part['pdf_link'])
                
                part['partnum_manufac_ngram3'] = get_ngrams(part['part_num']) \
                                                 + get_ngrams(part['manufac'])
                
                part['root_cat'] = self.pt.cat_tree[cat][subcat]['myrootcat']
                part['cat'] = self.pt.cat_tree[cat][subcat]['mycat']
                part['subcat'] = self.pt.cat_tree[cat][subcat]['mysubcat']
                
                db.invendb.update_one(
                        {'root_cat': part['root_cat'],
                         'cat': part['cat'],
                         'subcat': part['subcat']},
                        {'$inc': {'total': 1}},
                        upsert=True
                    )
            
                always_update = {'unit_price': part['unit_price'],
                                 'min_quan': part['min_quan'],
                                 'date_scraped': part['date_scraped'],
                                 'pdf_link': part['pdf_link'],
                                 'dist_partlink': part['dist_partlink']}
                db.distdb.update_one(
                        {'part_num': part['part_num'],
                         'manufac': part['manufac']},
                        {'$setOnInsert': {k: v for k, v in part.items()
                                               if k not in always_update.keys()},
                         '$set': always_update},
                         upsert=True
                    )
            
                db.manufacdb.update_one(
                        {'manufac': part['manufac']},
                        {'$setOnInsert': {'manufac': part['manufac'],
                                          'manufac_ngram3': get_ngrams(
                                                            part['manufac'])}},
                         upsert=True
                    )
                
                processed_pdf = db.metadb.find_one({'part_num': part['part_num'],
                                                    'manufac': part['manufac']})
                if part['pdf_link'] and (not processed_pdf
                                         or processed_pdf['processed'] == 'error'):
                    db.metadb.update_one({'part_num': part['part_num'],
                                          'manufac': part['manufac']},
                                         {'$set': {'processed': 'pending', 'page': 0,
                                                  'pdf_link': part['pdf_link']}},
                                         upsert=True)
    
                    if cfg.KEEP_GRIDFS_PDF:
                        item = PartsItem()
                        item['part_num'] = part['part_num']
                        item['manufac'] = part['manufac']
                        yield scrapy.Request(url=part['pdf_link'],
                                             callback=self.save_pdf,
                                             meta={'item': item})
                    else:
                        self.logger.info('### Saved PDF link %s__%s ###' % (
                                part['part_num'], part['manufac']
                            ))
                   
                self.__class__.prog_count += 1
                self.__class__.batch_count += 1
                print_prog(self.name+' total progress', self.prog_count,
                           self.total_count, left_just=20, endwith='')
                print_prog(' '*5+'Progress', self.batch_count, cfg.BATCH_SIZE,
                           left_just=5, bar_length=20, endwith='\r')
                
            next_page = response.xpath(self.xp.NEXT_PAGE).extract_first()
            if next_page:
                next_page = urljoin(self.base_url, next_page)
                db.cursordb.update_one({'ucat': cat+'__'+subcat, 'dist': self.name},
                                       {'$set': {'current_link': next_page},
                                        '$inc': {'current_count': table_len}})
                if self.batch_count < cfg.BATCH_SIZE:
                    yield scrapy.Request(url=next_page, callback=self.parse)
            else:
                start_link = db.cursordb.find_one(
                        {'ucat': cat+'__'+subcat,
                         'dist': self.name}
                    )['start_link']
                db.cursordb.update_one({'ucat': cat+'__'+subcat, 'dist': self.name},
                                       {'$set': {'current_link': start_link,
                                                 'scan_complete': True},
                                        '$inc': {'current_count': table_len}})
        except AttributeError:
            next_page = response.url
            self.logger.debug(f'---> Got invalid data from {response.url}, trying again with {next_page}')
            next_page = urljoin(self.base_url, next_page)
            db.cursordb.update_one({'ucat': cat+'__'+subcat, 'dist': self.name},
                                   {'$set': {'current_link': next_page}})
            if self.batch_count < cfg.BATCH_SIZE:
                yield scrapy.Request(url=next_page, callback=self.parse,
                                     dont_filter=True)
        
    def save_pdf(self, response):
        # Save PDF
        upart = f"{response.meta['item']['part_num']}__{response.meta['item']['manufac']}"
        db.pdfdb.put(response.body, filename=upart)
        self.logger.info('*** Saved PDF %s ***' % upart)