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
from utils.misc import replace_illchar


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
        
    def bread_crumbs(self, response):
        cat = response.xpath(xp.BREAD_CRUMBS1).extract_first()
        subcat = response.xpath(xp.BREAD_CRUMBS2).extract()[-1].strip('> ')
        return replace_illchar(cat), replace_illchar(subcat)
    
    def clean_pdf_link(self, pdf_link):
        if pdf_link:
            if pdf_link[0:7] == '//media':
                pdf_link = f'https:{pdf_link}'
        else:
            pdf_link = ''
        return pdf_link
    
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
            docs = list(self.docs.make_mongoelem(ext_elems_to_analyze=text))
        else:
            docs = [list(self.docs.make_mongoelem(ext_elems_to_analyze=[text]))[0]]
        return docs

      
    