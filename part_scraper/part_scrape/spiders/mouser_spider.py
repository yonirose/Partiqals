# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 12:41:37 2016

@author: jrosenfe
v8
"""
import os
import scrapy

from . base_spiders import MainBaseMixin
from dist.mouser import xpath_select as xp
from dist.mouser import part_tree as pt
from . mouser_prep_spider import MouserCount


class MouserSpider(MainBaseMixin, scrapy.Spider):
    
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
    
    def __init__(self):
        super().__init__(start_row_idx=3, xpath_select=xp, part_tree=pt)
    
    # Overriden methods
    def bread_crumbs(self, response):
        return MouserCount.bread_crumbs(self, response)
    
    def clean_pdf_url(self, url):
        return MouserCount.clean_pdf_url(self, url)
    
    def clean_next_url(self, url):
        return self.clean_pdf_url(url)
    
    def clean_link(self, link):
        return MouserCount.clean_link(self, link)
    
    def process_misc_data(self, text, part_num, misc_data):
        return self.docs.make_mongoelem(ext_elems_to_analyze=text) # Returns a generator

    def check_current_url(self, url):
        return self.clean_next_url(url)