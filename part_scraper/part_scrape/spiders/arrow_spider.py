# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 12:41:37 2016

@author: jrosenfe
v8
"""
import os
from urllib.parse import urlparse

import scrapy
#from scrapy.settings import Settings

import analyzer.line_parser as lp
import analyzer.analyze_html as ah

from utils.error_logging import ErrorHandler


class ArrowSpider(scrapy.Spider):
    name = 'arrow'
    goto_link = 'https://www.mouser.com/Semiconductors/Wireless-RF-Semiconductors/Wireless-RF-Integrated-Circuits/RFID-Transponders/_/N-az8ic/?No=225'
    custom_settings = {
        'LOG_FILE': os.path.join('..', '..', '..', 'logs',
                                 '%s_scrapy.log' % name)
    }
    open(os.path.join('..', '..', '..', 'logs','%s_scrapy.log' % name), 'w').close()
    
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
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                                  AppleWebKit/537.36 (KHTML, like Gecko) \
                                  chrome/66.0.3359.139 Safari/537.36'}
        for start_link in [self.goto_link]:
            yield scrapy.Request(start_link, headers=headers)

    def parse(self, response):
        print('\n%s' % response.status)
        if response.status == 200:
            dist = urlparse(response.url)
            fname = f"{dist.netloc.split('.')[1]}_{''.join(dist.path[1:].split('/'))}.html"
            print(fname)
            with open(fname, 'wt', encoding='utf-8') as f:
                f.write(response.text)
        else:
            print(f'Response status {response.status}')

   
