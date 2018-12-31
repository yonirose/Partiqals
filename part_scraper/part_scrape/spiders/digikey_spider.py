# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 12:41:37 2016

@author: jrosenfe
v8
"""
import os
import scrapy

from . base_spiders import MainBaseMixin
from dist.digikey import xpath_select as xp
from dist.digikey import part_tree as pt
from . digikey_prep_spider_new import DigikeyCount 


class DigikeySpider(MainBaseMixin, scrapy.Spider):
    
    name = 'digikey'
    custom_settings = {
        'LOG_FILE': os.path.join('..', '..', '..', 'logs',
                                 '%s_scrapy.log' % name),
        'DOWNLOADER_MIDDLEWARES': {
                'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
                'part_scrape.Middleware.ProxyMiddleware.middlewares.RandomProxy': 100,
                'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
                'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
                'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400
            }
    }
    open(os.path.join('..', '..', '..', 'logs','%s_scrapy.log' % name), 'w').close()
    base_url = 'https://www.digikey.com'
       
    def __init__(self):
        super().__init__(start_row_idx=1, xpath_select=xp, part_tree=pt)
    
    #These methods must be defined
    def bread_crumbs(self, response):
        return DigikeyCount.bread_crumbs(self, response)
    
    def clean_pdf_url(self, url):
        return DigikeyCount.clean_pdf_link(self, url)
    
    def clean_next_url(self, url):
        return url
    
    def process_misc_data(self, text, part_num, misc_data):
        # Special case for package dimensions
        if all([token in text for token in ['Size', 'Dimension',
                                            'L', 'W']]):
            #self.text_to.reset_result()
            # Explicit decoration
            self.err_to.logger(text, 'info', part_num)(self.text_to.parse)(text)
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
        #    docs = list(self.docs.make_mongoelem(ext_elems_to_analyze=text))
        #else:
        #    docs = [list(self.docs.make_mongoelem(ext_elems_to_analyze=[text]))[0]]
        return self.docs.make_mongoelem(ext_elems_to_analyze=text) # This is a generator
    
    def check_current_url(self, url):
        return self.clean_next_url(url)

      
    