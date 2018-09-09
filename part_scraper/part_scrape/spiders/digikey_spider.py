# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 12:41:37 2016

@author: jrosenfe
v8
"""
import os
import datetime

import scrapy
#from scrapy.settings import Settings

from utils.misc import replace_illchar
from utils.progress import print_prog
from dist.digikey import xpath_select as xp
from dist.digikey import part_tree as pt
import analyzer.line_parser as lp
import analyzer.analyze_html as ah
from ..items import partsItem
import db_setup as db
import config as cfg
from utils.error_logging import ErrorHandler
from utils.misc import get_ngrams 


class DigikeySpider(scrapy.Spider):
    name = 'digikey' # cfg.SPIDER_LIST[0]
    custom_settings = {
        'LOG_FILE': os.path.join('..', '..', '..', 'logs',
                                 '%s_scrapy.log' % name)
    }
    open(os.path.join('..', '..', '..', 'logs','%s_scrapy.log' % name), 'w').close()
    
    '''
    my_settings = Settings()
    my_settings.set(
            name='LOG_FILE',
            value=os.path.join('..', '..', '..', 'logs', 'scrapy_%s.log' % name),
            priority='cmdline'
        )
    '''              
    prog_count = 0
    total_count = 0
    # total_pages = 0
    page_count = 0
    batch_count = 0
       
    
    def __init__(self):
        super().__init__()
        # scrapy.Spider.__init__(self)
        # base_path = os.path.join('..', '..', '..')
        # Start a new Scrapy log file
        # open(os.path.join(base_path, 'logs', 'scrapy_log.log'), 'w').close()
        
        self.docs = ah.MongoDocCreator()
        self.text_to = lp.Parser()
        self.err_to = ErrorHandler()

      
    def start_requests(self):
        start_links = []
        headers= {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                                 AppleWebKit/537.36 (KHTML, like Gecko) \
                                 Chrome/66.0.3359.139 Safari/537.36'}
        
        for cat in db.cursordb.find({'dist': DigikeySpider.name}):
            if not cat['scan_complete']:
                start_links.append(cat['current_link'])
                DigikeySpider.total_count += cat['total_count']
                DigikeySpider.prog_count += cat['current_count']
        
        # self.perc_total = int(self.scan_perc*(DigikeySpider.total_count - DigikeySpider.prog_count))
        print_prog(self.name+' Total progress', DigikeySpider.prog_count,
                   DigikeySpider.total_count, left_just=20, endwith='')
        print_prog(' '*5+'Progress',  DigikeySpider.batch_count, cfg.BATCH_SIZE,
                   left_just=5, bar_length=20, endwith='\r')
        for start_link in start_links:
            yield scrapy.Request(start_link, headers=headers)

    def parse(self, response):
        cat = replace_illchar(response.xpath(xp.CAT).extract_first().strip())
        subcat = response.xpath(xp.SUBCAT).extract_first()
        subcat = replace_illchar(subcat[subcat.rindex(';')+1:subcat.rindex('<')].strip())
        table_len = len(response.xpath(xp.TABLE_LEN))
        
        table_heads = {}
        idx = xp.HEAD_START_IDX
        while True:
            head = response.xpath(xp.HEAD_TITLE % idx).extract()
            if head:
                table_heads[idx] = head[0]
                idx += 1
            else:
                break
            
        for idx in range(1, table_len+1):
            part = {
                    'part_num': replace_illchar(response.xpath(xp.PART_NUM % idx).extract_first().strip()),
                    'dist_num': response.xpath(xp.DIST_NUM % idx).extract_first().strip(),
                    'manufac': replace_illchar(response.xpath(xp.MANUFAC % idx).extract_first()),
                    'descr': response.xpath(xp.DESCR % idx).extract_first().strip(),
                    'unit_price': response.xpath(xp.UNIT_PRICE % idx).extract_first().strip().replace(',', ''),
                    'dist': self.name,
                    'dist_partlink': 'http://www.digikey.com' + response.xpath(xp.DIST_LINK % idx).extract_first(),
                    'pdf_link': response.xpath(xp.PDF_LINK % idx).extract_first(),
                    'min_quan': response.xpath(xp.MIN_QUAN % idx).extract_first().strip().replace(',', ''),
                    'date_scraped': datetime.datetime.utcnow()
                }
            for title_idx, table_title in table_heads.items():
                misc_data = response.xpath(xp.MISC_DATA % (idx, title_idx)).extract_first().strip()
                if misc_data:
                    text = '%s %s' % (table_title, misc_data)
                    # Special case for Digikey package dimensions
                    if 'Size' in text and 'Dimension' in text and 'L' in text and 'W' in text:
                        self.text_to.reset_result()
                        # Explicit decoration
                        self.err_to.logger(text, 'info', part['part_num'])(self.text_to.parse)(text)
                        
                        text = [
                                'Size Dimension Length %s%s' % (
                                    self.text_to.result['param'][2][0],
                                    self.text_to.result['param'][2][1]
                                ),
                                'Size Dimension Width %s%s' % (
                                    self.text_to.result['param'][3][0],
                                    self.text_to.result['param'][3][1]
                                )
                            ]
                        docs = list(self.docs.make_mongoelem(ext_elems_to_analyze=text))
                    else:
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
            try:
                if part['unit_price'][0] == '$':
                    part['unit_price'] = float(part['unit_price'][1:])
                else:
                    part['unit_price'] = float(part['unit_price'])
            except IndexError:
                part['unit_price'] = 'See distributer'
            except ValueError:
                pass
            if part['pdf_link']:
                if part['pdf_link'][0:7] == '//media':
                    part['pdf_link'] = 'http:' + part['pdf_link']
            else:
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
                    {'manufac_ngram3': part['manufac']},
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
                    item = partsItem()
                    item['part_num'] = part['part_num']
                    item['manufac'] = part['manufac']
                    yield scrapy.Request(url=part['pdf_link'],
                                         callback=self.save_pdf,
                                         meta={'item': item})
                else:
                    self.logger.info('### Saved PDF link %s__%s ###' % (
                            part['part_num'], part['manufac']
                        ))
                   
            DigikeySpider.prog_count += 1
            DigikeySpider.batch_count += 1
        
        print_prog(self.name+' total progress', DigikeySpider.prog_count,
                   DigikeySpider.total_count, left_just=20, endwith='')
        print_prog(' '*5+'Progress', DigikeySpider.batch_count, cfg.BATCH_SIZE,
                   left_just=5, bar_length=20, endwith='\r')
        next_page = response.xpath(xp.NEXT_PAGE).extract_first()
        
        if next_page:
            next_page = 'https://www.digikey.com' + next_page
            
            db.cursordb.update_one({'ucat': cat+'__'+subcat,
                                      'dist':DigikeySpider.name},
                                     {'$set': {'current_link': next_page},
                                      '$inc': {'current_count': table_len}})
            if DigikeySpider.batch_count < cfg.BATCH_SIZE:
                yield scrapy.Request(url=next_page, callback=self.parse)
        else:
            start_link = db.cursordb.find_one(
                    {'ucat': cat+'__'+subcat,
                     'dist': DigikeySpider.name}
                )['start_link']
            db.cursordb.update_one({'ucat': cat+'__'+subcat,
                                      'dist':DigikeySpider.name},
                                     {'$set': {'current_link': start_link,
                                               'scan_complete': True},
                                      '$inc': {'current_count': table_len}})
            
    def save_pdf(self, response):
        # Save PDF
        db.pdfdb.put(response.body, filename=upart)
        self.logger.info('*** Saved PDF %s ***' % upart)


                
