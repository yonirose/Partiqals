# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 12:41:37 2016

@author: jrosenfe
v2
"""

import os

import scrapy

from . base_spiders import PrepBaseMixin
from dist.mouser import xpath_select as xp
from dist.mouser import init_pages as init
from utils.misc import replace_illchar


class MouserCount(PrepBaseMixin, scrapy.Spider):
    name = "mouser_prep"
    custom_settings = {
        'LOG_FILE': os.path.join('..', '..', '..', 'logs',
                                 f'{name}_scrapy.log'),
        'DOWNLOADER_MIDDLEWARES': {
                'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
                'part_scrape.Middleware.ProxyMiddleware.middlewares_prep_mouser.RandomProxy': 100,
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
        bread_crumbs = response.xpath(xp.BREAD_CRUMBS).extract()
        cat_name, subcat_name = bread_crumbs[-2:]
        return replace_illchar(cat_name), replace_illchar(subcat_name)
