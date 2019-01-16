# -*- coding: utf-8 -*-
"""
Created on Sun Dec 2 13:38:39 2018

@author: jrosenfe
"""
import os
import datetime
import time
import re
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

class AutoStorage:
    
    def __init__(self, storage_name):
        self.storage_name = storage_name
        super().__init__() # Calls ValidationTypes.__init__()
        
    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.storage_name] + (self.storage_name,)
        
    def __set__(self, instance, value):
        instance.__dict__[self.storage_name] = value
        

class DataValidation(AutoStorage):
    
    def __set__(self, instance, value):
        value = self.format_and_validate(value)
        super().__set__(instance, value)
        
    def format_and_validate(self, value):
        raise NotImplementedError


class ValidationTypes:
    
    def __init__(self):
        self.valid_funcs = {'empty_string': self.empty_string,
                            'not_int': self.not_int,
                            'not_float': self.not_float,
                            'not_str': self.not_str,
                            'http_inlink': self.http_inlink}
        
    def report_issue(self, problem):
        return (
                '~'*80
                + '\n'
                + time.strftime('%m/%d/%Y')
                + ' '
                + time.strftime('%H:%M:%S')
                + ' '
                + 'DIST: %s\n'
                + '%s\n'
                + 'PART NUM: %s, ISSUE: '
                + problem + '\n' 
            )
                
    def waiver(self, valid_type, data):
        waiver_cases = {'not_float': ['Digi-Reel']}
        for waiver_case in waiver_cases[valid_type]:
            if data == waiver_case:
                return True
        return False
        
    def empty_string(self, data_type, data):
        if data == '':
            return self.report_issue(f"{data_type} is empty string ''")
        return None
      
    def not_int(self, data_type, data):
        if not isinstance(data, int):
            return self.report_issue(f'{data_type} is not int but <{data}>')
        return None
            
    def not_float(self, data_type, data):
        if not isinstance(data, float) and not self.waiver('not_float', data):
            return self.report_issue(f'{data_type} is not float but <{data}>')
        return None
            
    def not_str(self, data_type, data):
        if not isinstance(data, str):
            return self.report_issue(f'{data_type} is not str but <{data}>')
        return None
            
    def http_inlink(self, data_type, data):
        if 'http' not in data and 'https' not in data:
            return self.report_issue(f"{data_type} has no 'http(s)' in <{data}>")
        return None


class PartNum(DataValidation, ValidationTypes):
    
    def __init__(self, storage_name, *valid_types):
        super().__init__(storage_name)
        self.valid_types = valid_types
          
    def format_and_validate(self, value):
        try:
            value = replace_illchar(value.strip())
        except Exception:
            value = 'N/A'
        
        for valid_type in self.valid_types:
            err_msg = self.valid_funcs[valid_type](self.storage_name, value)
            if err_msg is not None:
                return (value, err_msg)
        return (value, None)


class DistNum(DataValidation, ValidationTypes):
    
    def __init__(self, storage_name, *valid_types):
        super().__init__(storage_name)
        self.valid_types = valid_types

    def format_and_validate(self, value):
        try:
            value = value.strip()
        except Exception:
            value = 'See distributer'
        
        for valid_type in self.valid_types:
            err_msg = self.valid_funcs[valid_type](self.storage_name, value)
            if err_msg is not None:
                return (value, err_msg)
        return (value, None)

    
class Manufac(DataValidation, ValidationTypes):
    
    def __init__(self, storage_name, *valid_types):
        super().__init__(storage_name)
        self.valid_types = valid_types

    def format_and_validate(self, value):
        try:
            value = replace_illchar(value)
        except Exception:
            value = 'See distributer'
        
        for valid_type in self.valid_types:
            err_msg = self.valid_funcs[valid_type](self.storage_name, value)
            if err_msg is not None:
                return (value, err_msg)
        return (value, None)
    
    
class Descr(DataValidation, ValidationTypes):
    
    def __init__(self, storage_name, *valid_types):
        super().__init__(storage_name)
        self.valid_types = valid_types

    def format_and_validate(self, value):
        try:
            value = value.strip()
        except Exception:
            value = 'N/A'
        
        for valid_type in self.valid_types:
            err_msg = self.valid_funcs[valid_type](self.storage_name, value)
            if err_msg is not None:
                return (value, err_msg)
        return (value, None)
    
    
class UnitPrice(DataValidation, ValidationTypes):
    
    def __init__(self, storage_name, *valid_types):
        super().__init__(storage_name)
        self.valid_types = valid_types

    def format_and_validate(self, value):
        try:
            value = float(replace_illchar(value.strip()))
        except Exception:
            if self.waiver('not_float', value):
                pass
            else:
                value = 'See distributer'
        
        for valid_type in self.valid_types:
            err_msg = self.valid_funcs[valid_type](self.storage_name, value)
            if err_msg is not None:
                return (value, err_msg)
        return (value, None)
    
    
class DistPartLink(DataValidation, ValidationTypes):
    
    def __init__(self, storage_name, *valid_types):
        super().__init__(storage_name)
        self.valid_types = valid_types

    def format_and_validate(self, value):
        if not value:
            value = ''
        
        for valid_type in self.valid_types:
            err_msg = self.valid_funcs[valid_type](self.storage_name, value)
            if err_msg is not None:
                return (value, err_msg)
        return (value, None)
    
    
class PdfLink(DataValidation, ValidationTypes):
    
    def __init__(self, storage_name, *valid_types):
        super().__init__(storage_name)
        self.valid_types = valid_types

    def format_and_validate(self, value):
        if not value:
            value = ''
        
        for valid_type in self.valid_types:
            err_msg = self.valid_funcs[valid_type](self.storage_name, value)
            if err_msg is not None:
                return (value, err_msg)
        return (value, None)
    
    
class MinQuan(DataValidation, ValidationTypes):
    
    def __init__(self, storage_name, *valid_types):
        super().__init__(storage_name)
        self.valid_types = valid_types

    def format_and_validate(self, value):
        try:
            value = int(value.strip().replace(',', ''))
        except Exception:
            value = 'See distributer'
        
        for valid_type in self.valid_types:
            err_msg = self.valid_funcs[valid_type](self.storage_name, value)
            if err_msg is not None:
                return (value, err_msg)
        return (value, None)


class PrepBaseMixin:
    
    current_count = 0
    cat_tree = defaultdict(set)
    
    def __init__(self, xpath_select, init):
        super().__init__()
        self.xp = xpath_select
        self.init = init
    
    def bread_crumbs(self, response):
        raise NotImplementedError
    
    def clean_next_url(self, url):
        raise NotImplementedError
        
    def clean_pdf_url(self, url):
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
                        url = self.clean_next_url(urljoin(self.base_url, subcat_link))
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
                   url = self.clean_next_url(urljoin(self.base_url, subcat_link))
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
                   self.clean_next_url(response.url)
            )
    
    def closed(self, reason):
        print('\n')
        count, tot_count = self.update_prog(prog_bar=False)
        if count == tot_count:
            with open(os.path.join(self.base_path, 'part_tree_latest.py'), 'at') as f:
                headers = [f"# {time.strftime('%m/%d/%Y')}, {time.strftime('%H:%M:%S')}\n",
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


class DescrpWrap:
    ''' Descriptor definition '''
    part_num = PartNum('part_num', *['empty_string', 'not_str'])
    dist_num = DistNum('dist_num', *['empty_string', 'not_str'])
    manufac = Manufac('manufac', *['empty_string', 'not_str'])
    descr = Descr('descr', *['empty_string', 'not_str'])
    unit_price = UnitPrice('unit_price', *['not_float'])
    dist_partlink = DistPartLink('dist_partlink', *['empty_string'])
    pdf_link = PdfLink('pdf_link', *['empty_string', 'http_inlink'])
    min_quan = MinQuan('min_quan', *['not_int'])

class MainBaseMixin:
    
    prog_count = 0
    total_count = 0
    batch_count = 0
    
    ''' Descriptor definition '''
    part_num = PartNum('part_num', *['empty_string', 'not_str'])
    dist_num = DistNum('dist_num', *['empty_string', 'not_str'])
    manufac = Manufac('manufac', *['empty_string', 'not_str'])
    descr = Descr('descr', *['empty_string', 'not_str'])
    unit_price = UnitPrice('unit_price', *['not_float'])
    dist_partlink = DistPartLink('dist_partlink', *['empty_string'])
    pdf_link = PdfLink('pdf_link', *['empty_string', 'http_inlink'])
    min_quan = MinQuan('min_quan', *['not_int'])

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
        
    def clean_next_url(self, url):
        raise NotImplementedError
        
    def clean_pdf_url(self, url):
        raise NotImplementedError
        
    def process_misc_data(self, text, part_num, misc_data):
        raise NotImplementedError
        
    def check_current_url(self, url):
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
        print_prog(' '*5+'Progress', self.batch_count, cfg.BATCH_SIZE,
                   left_just=5, bar_length=20, endwith='\r')
        shuffle(start_links)
        for start_link in start_links:
            yield scrapy.Request(start_link, headers=headers)
    
    def update_db(self, part):
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

    def clean_part_data_and_store(self, part, cat, subcat):
        for _ in [('unit_price', float), ('min_quan', int)]:
            try:
                part[_[0]] = _[1](part[_[0]])
            except ValueError:
                if not part[_[0]] or re.match(r'[0-9]+', part[_[0]]) is not None:
                   part[_[0]] = 'See distributer'
                   
        part['pdf_link'] = self.clean_pdf_url(part['pdf_link'])
        part['partnum_manufac_ngram3'] = get_ngrams(part['part_num']) \
                                         + get_ngrams(part['manufac'])
        part['root_cat'] = self.pt.cat_tree[cat][subcat]['myrootcat']
        part['cat'] = self.pt.cat_tree[cat][subcat]['mycat']
        part['subcat'] = self.pt.cat_tree[cat][subcat]['mysubcat']
        self.update_db(part)
        
    def parse(self, response):
        descrp = DescrpWrap() # Per instance desriptors to avoid overwriting
        if os.path.isdir('.stop_spider') or self.batch_count > cfg.BATCH_SIZE*0.9:
            print(f'\nStop crawling spider {self.name}')
            raise scrapy.exceptions.CloseSpider('Stopped by user')
        
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
            cat, subcat = self.bread_crumbs(response)
            table_len = len(response.xpath(self.xp.TABLE_LEN))
            for idx in range(self.start_row_idx, table_len+1):
                self.part_num = response.xpath(self.xp.PART_NUM % idx).extract_first()
                self.dist_num = response.xpath(self.xp.DIST_NUM % idx).extract_first()
                self.manufac = response.xpath(self.xp.MANUFAC % idx).extract_first()
                self.descr = response.xpath(self.xp.DESCR % idx).extract_first()
                self.unit_price = response.xpath(self.xp.UNIT_PRICE % idx).extract_first()
                self.dist_partlink = response.xpath(self.xp.DIST_LINK % idx).extract_first()
                self.pdf_link = response.xpath(self.xp.PDF_LINK % idx).extract_first()
                self.min_quan = response.xpath(self.xp.MIN_QUAN % idx).extract_first()
                
                base_params = [self.part_num, self.dist_num, self.manufac,
                               self.descr, self.unit_price, self.dist_partlink,
                               self.pdf_link, self.min_quan]
                
                part = dict()
                for value, err_msg, storage_name in base_params:
                    if err_msg is not None:
                       with open(os.path.join('..', '..', '..', 'logs',
                                 'data_validation.log'), 'at') as dv_file:
                           try:
                               err_msg = err_msg % (self.name, response.url, base_params[0][0])
                               dv_file.write(err_msg)
                           except TypeError:
                               self.logger.info('~~> '+err_msg % (self.name, response.url, base_params[0][0]))
                               
                    part[storage_name] = value
                part = {**part, **{'dist': self.name,
                                   'date_scraped': datetime.datetime.utcnow()}}
                part['dist_partlink'] = urljoin(self.base_url,
                                                part['dist_partlink'])
                
                '''
                part = {
                        'part_num': self.part_num,
                        'dist_num': self.dist_num,
                        'manufac': self.manufac,
                        'descr': self.descr,
                        'unit_price': self.unit_price,
                        'dist': self.name,
                        'dist_partlink': self.dist_partlink,
                        'pdf_link': self.pdf_link,
                        'min_quan': self.min_quan,
                        'date_scraped': datetime.datetime.utcnow()
                    }
                '''
                
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
                
                self.clean_part_data_and_store(part, cat, subcat)
                
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
            
            modified_url = self.check_current_url(response.url)
            if modified_url:
                next_page = modified_url
                raise AttributeError
            else:
                next_page = response.xpath(self.xp.NEXT_PAGE).extract_first()
            if next_page:
                next_page = self.clean_next_url(urljoin(self.base_url, next_page))
                db.cursordb.update_one({'ucat': cat+'__'+subcat, 'dist': self.name},
                                       {'$set': {'current_link': next_page},
                                        '$inc': {'current_count': table_len}})
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
        except (AttributeError, ValueError):
            next_page = self.clean_next_url(urljoin(self.base_url, next_page))
            self.logger.debug(f'---> Got invalid data from {response.url}, trying again with {next_page}')
            db.cursordb.update_one({'ucat': cat+'__'+subcat, 'dist': self.name},
                                   {'$set': {'current_link': next_page}})
            yield scrapy.Request(url=next_page, callback=self.parse,
                                 dont_filter=True)
        
    def save_pdf(self, response):
        # Save PDF
        upart = f"{response.meta['item']['part_num']}__{response.meta['item']['manufac']}"
        db.pdfdb.put(response.body, filename=upart)
        self.logger.info('*** Saved PDF %s ***' % upart)