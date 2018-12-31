# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 12:41:37 2016

@author: jrosenfe
v2
"""

import os

import scrapy

from . base_spiders import PrepBaseMixin
from dist.digikey import xpath_select as xp
from dist.digikey import init_pages as init
from utils.misc import replace_illchar


class DigikeyCount(PrepBaseMixin, scrapy.Spider):
    name = "digikey_prepnew"
    custom_settings = {
        'LOG_FILE': os.path.join('..', '..', '..', 'logs',
                                 f'{name}_scrapy.log'),
        'DOWNLOADER_MIDDLEWARES': {
                'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
                'part_scrape.Middleware.ProxyMiddleware.middlewares_prep.RandomProxy': 100,
                'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
                'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
                'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400
            }
    } 
    open(os.path.join('..', '..', '..', 'logs', f'{name}_scrapy.log'),
                      'w').close()
    
    base_path = os.path.join('..', '..', '..', 'dist', name.split('_')[0])
    base_url = init.start_url[0]
    start_urls = init.start_url
    print('Initializing...', end='\r')
    
    def __init__(self):
        super().__init__(xpath_select=xp, init=init)
        
    def bread_crumbs(self, response):
        cat = response.xpath(xp.BREAD_CRUMBS1).extract_first()
        subcat = response.xpath(xp.BREAD_CRUMBS2).extract()[-1].strip('> ')
        return replace_illchar(cat), replace_illchar(subcat)
    
    def clean_pdf_url(self, url):
        if url:
            if url[0:7] == '//media':
                url = f'https:{url}'
        else:
            url = ''
        return url
