# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 12:41:37 2016

@author: jrosenfe
v8
"""
import os
import datetime
from random import shuffle
from urllib.parse import urljoin

import scrapy
#from scrapy.settings import Settings

from utils.misc import replace_illchar
from utils.progress import print_prog
from dist.mouser import xpath_select as xp
from dist.mouser import part_tree as pt
import analyzer.line_parser as lp
import analyzer.analyze_html as ah
from ..items import PartsItem
import db_setup as db
import config as cfg
from utils.error_logging import ErrorHandler
from utils.misc import get_ngrams


class MouserSpider(scrapy.Spider):
    name = 'mouser'
    custom_settings = {
        'LOG_FILE': os.path.join('..', '..', '..', 'logs',
                                 f'{name}_scrapy.log'),
        'DOWNLOADER_MIDDLEWARES': {
                'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
                'part_scrape.Middleware.ProxyMiddleware.middlewares_mouser.RandomProxy': 100,
                'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
                'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
                'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400
            }
    }
    open(os.path.join('..', '..', '..', 'logs','%s_scrapy.log' % name), 'w').close()
    base_url = 'https://www.mouser.com'    
    prog_count = 0
    total_count = 0
    # total_pages = 0
    page_count = 0
    batch_count = 0   
    
    def __init__(self):
        super().__init__()
        self.docs = ah.MongoDocCreator()
        self.text_to = lp.Parser()
        self.err_to = ErrorHandler()
  
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
        
        print_prog(self.name+' total progress', self.__class__.prog_count,
                   self.__class__.total_count, left_just=20, endwith='')
        print_prog(' '*5+'Progress',  self.__class__.batch_count, cfg.BATCH_SIZE,
                   left_just=5, bar_length=20, endwith='\r')
        start_links = shuffle(start_links)
        for start_link in start_links:
            yield scrapy.Request(start_link, headers=headers)

    def parse(self, response):
        if os.path.isdir('.stop_spider'):
            print(f'\nStop crawling spider {self.name}')
            raise scrapy.exceptions.CloseSpider('Stopped by user')
            
        bread_crumbs = response.xpath(xp.BREAD_CRUMBS).extract()
        cat, subcat = bread_crumbs[-2:]
        cat, subcat = replace_illchar(cat), replace_illchar(subcat)
        table_len = len(response.xpath(xp.TABLE_LEN))
        
        table_heads = {}
        idx = xp.HEAD_START_IDX
        while True:
            head = response.xpath(xp.HEAD_TITLE % idx).extract()
            if head:
                table_heads[idx] = head[0].strip()
                idx += 1
            else:
                break
        try:
            for idx in range(3, table_len+1):
                part = {
                        'part_num': replace_illchar(response.xpath(xp.PART_NUM % idx).extract_first().strip()),
                        'dist_num': response.xpath(xp.DIST_NUM % idx).extract_first().strip(),
                        'manufac': replace_illchar(response.xpath(xp.MANUFAC % idx).extract_first()),
                        'descr': response.xpath(xp.DESCR % idx).extract_first().strip(),
                        'unit_price': replace_illchar(response.xpath(xp.UNIT_PRICE % idx).extract_first().strip()),
                        'dist': self.name,
                        'dist_partlink': urljoin(self.base_url, response.xpath(xp.DIST_LINK % idx).extract_first()),
                        'pdf_link': response.xpath(xp.PDF_LINK % idx).extract_first(),
                        'min_quan': response.xpath(xp.MIN_QUAN % idx).extract_first().strip().replace(',', ''),
                        'date_scraped': datetime.datetime.utcnow()
                    }
                for title_idx, table_title in table_heads.items():
                    misc_data = response.xpath(xp.MISC_DATA % (idx, title_idx)).extract_first().strip()
                    if misc_data:
                        text = f'{table_title} {misc_data}'
                        docs = [list(self.docs.make_mongoelem(ext_elems_to_analyze=[text]))[0]]
                        
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
            
                if not part['pdf_link']:
                    part['pdf_link'] = ''
        
                part['partnum_manufac_ngram3'] = get_ngrams(part['part_num']) \
                                                 + get_ngrams(part['manufac'])
                
                part['root_cat'] = pt.cat_tree[cat][subcat]['myrootcat']
                part['cat'] = pt.cat_tree[cat][subcat]['mycat']
                part['subcat'] = pt.cat_tree[cat][subcat]['mysubcat']
                
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
                
                processed_pdf = db.distdb.find_one({'part_num': part['part_num'],
                                                    'manufac': part['manufac'],
                                                    'processed': {'$exists': True}})
                
                if part['pdf_link'] and (not processed_pdf
                                         or processed_pdf['processed'] == 'error'):
                    db.distdb.update_one({'part_num': part['part_num'],
                                          'manufac': part['manufac']},
                                         {'$set': {'processed': 'pending', 'page': 0}})
    
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
            next_page = response.xpath(xp.NEXT_PAGE).extract_first()
            dup_req = False
        except AttributeError:
            next_page = response.url
            self.logger.debug(f'---> Got invalid data from {response.url}, trying again with {next_page}')
            dup_req = True
                
        if next_page:
            next_page = urljoin(self.base_url, next_page)
            if dup_req: # Don't update count, only link
                db.cursordb.update_one({'ucat': cat+'__'+subcat, 'dist': self.name},
                                       {'$set': {'current_link': next_page}})
            else:
                db.cursordb.update_one({'ucat': cat+'__'+subcat, 'dist': self.name},
                                       {'$set': {'current_link': next_page},
                                        '$inc': {'current_count': table_len}})
                                             
            if self.batch_count < cfg.BATCH_SIZE:
                yield scrapy.Request(url=next_page, callback=self.parse,
                                     dont_filter=dup_req)
        else:
            start_link = db.cursordb.find_one(
                    {'ucat': cat+'__'+subcat,
                     'dist': self.name}
                )['start_link']
            db.cursordb.update_one({'ucat': cat+'__'+subcat, 'dist': self.name},
                                   {'$set': {'current_link': start_link,
                                             'scan_complete': True},
                                    '$inc': {'current_count': table_len}})
            
    def save_pdf(self, response):
        # Save PDF
        upart = f"{response.meta['item']['part_num']}__{response.meta['item']['manufac']}"
        db.pdfdb.put(response.body, filename=upart)
        self.logger.info('*** Saved PDF %s ***' % upart)


                
