# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 15:42:15 2017

@author: jrosenfe
v2
"""

import os
import scrapy
# from scrapy.settings import Settings

import db_setup as db
import config as cfg
from utils.progress import print_prog

class PdfDatasheetAgent(scrapy.Spider):
    name = 'agent_spider'
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
                  
    pdf_cnt = 0
    pdf_totcnt = 0
    uparts = {}
            
    def start_requests(self):
        start_links = []
        parts = db.metadb.find({'processed': 'error'})
        PdfDatasheetAgent.pdf_totcnt = parts.count()
        print_prog('Agenting',  PdfDatasheetAgent.pdf_cnt,
                   PdfDatasheetAgent.pdf_totcnt,
                   left_just=5, bar_length=20, endwith='\r')
        for part in parts:
            start_links.append(cfg.PDF_AGENT_URL+part['upart'].split('__')[0])
            PdfDatasheetAgent.uparts[part['upart'].split('__')[0]] = part['upart']
        
        for start_link in start_links:
            yield self.make_requests_from_url(start_link)
        
    def parse(self, response):
        # href = response.xpath(cfg.AGENT_PDF_XPATH).extract_first()
        
        # Get the last element from the links array
        href = response.xpath(cfg.AGENT_PDF_XPATH).extract()[-1]
        if href:
            part_num = response.url.split('/')[-1]
            yield scrapy.Request(
                    url= 'https://www.datasheetpro.com'+href,
                    callback=self.save_pdf,
                    meta={'upart': PdfDatasheetAgent.uparts[part_num]}
                )

    def save_pdf(self, response):
        upart = response.meta['upart']
        # print(upart)
        if cfg.KEEP_GRIDFS_PDF:
            db.pdfdb.delete(db.pdfdb.find_one({'filename': upart})._id)
            db.pdfdb.put(response.body, filename=upart)
        db.distdb.update_one({'part_num': upart.split('__')[0],
                                'manufac': upart.split('__')[1]},
                                {'$set': {'pdf_link': response.url}})
        db.metadb.update_one({'upart': upart},
                               {'$set': {'processed': 'pending'}})
        PdfDatasheetAgent.pdf_cnt += 1
        print_prog('Agenting',  PdfDatasheetAgent.pdf_cnt,
                   PdfDatasheetAgent.pdf_totcnt,
                   left_just=5, bar_length=20, endwith='\r')
        
        
            
