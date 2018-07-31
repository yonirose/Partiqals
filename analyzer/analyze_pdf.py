# -*- coding: utf-8 -*-
"""
Created on Thu May 11 09:00:00 2017

@author: jrosenfe
"""

import os
import shutil

import time
from subprocess import Popen

import lxml.etree
import requests

import analyze_html as ah
import symb_unit as symu
from utils.query import FindCommonProp
import db_setup as db
from utils.error_logging import ErrorHandler
from utils.progress import analyze_pdf_prog
from utils.misc import get_ngrams
import config as cfg

#import analyzer.line_parser as lp
#import analyzer.analyze_html as ah

class DataValidation():
    def __init__(self, elem):
        self.elem = elem
    '''
    def unit_comp(self):
       for phi_cat, terms in symu.unit_term.items():
           if set(self.elem['word']) & set(terms):
              if self.elem['unit'] not in symu.phy_units[phi_cat]:
                  return False
       return True
    '''
    
    def unit_comp(self):
       for phi_cat, terms in symu.unit_term.items():
           if set(self.elem['word']) & set(terms):
              if self.elem['unit'] in symu.phy_units[phi_cat]:
                  return True
       return False
   
    def similar_notexists(self):
        for all_elem in self.allpages_mongoelem:
            if FindCommonProp.similarity_score(self,
               self.elem['word'], all_elem['word']) >= cfg.ELEM_SIMILAR_SCORE and \
               self.curr_page_num != all_elem['page_num']:
                    return False
        return True
        
    def nounit_param_word(self):
        return (
                not self.elem['unit']
                and self.param_word()
            )
    
    def param_word(self):
        return (
                self.elem['param']
                and cfg.MIN_NUM_WORDS <= len(self.elem['word']) <= cfg.MAX_NUM_WORDS
            )
        
    def unit_param_word(self, curr_page_num, allpages_mongoelem):
        self.curr_page_num = curr_page_num
        self.allpages_mongoelem = allpages_mongoelem
        return (
                self.elem['unit']
                and self.param_word()
                and self.similar_notexists()
                and self.unit_comp()
            )
        
    def noparam_word(self):
        return not self.elem['param'] and self.elem['word']
        
    def no_fig(self):
        words = ' '.join(self.elem['word'])
        if 'noise' in words:
            return True
        elif 'figure' in words or 'fig' in words or 'fig.' in words:
            return False
        return True
    
    def alphaword_param(self):
        if self.elem['param']:
            for word in self.elem['word']:
                if not word.replace('-', '').isalpha():
                    return False
        return True
    '''
    def word_length(self):
        result = False
        for word in self.elem['word']:
            result = result or len(word) >= 3
            if result:
                return result
        return result
    '''    
    def unit_param(self):
        if self.elem['unit'] and not self.elem['param']:
            return False
        else:
            return True


class Analyzer():
    def __init__(self, upart, max_pdfpages=cfg.MAX_PDF_PAGES):
        self.max_pdfpages = max_pdfpages
        self.upart = upart
        self._upart = upart.replace(' ', '_') # To avoid space in file names
        self.base_dir = os.path.join('.', 'pdf_extract')
        self.pdf_dir = os.path.join(self.base_dir, self._upart,
                                    self.upart.split('__')[0]+'.pdf')
        self.html_dir = os.path.join(self.base_dir, self._upart,
                                     self.upart.split('__')[0]+'.html')
        self.err_to = ErrorHandler()
        
    def create_db(self, page_num):
        analyze_pdf_prog()
        success = False
        try:
            os.mkdir(os.path.join(self.base_dir, self._upart))
            if cfg.KEEP_GRIDFS_PDF:
                pdf_out = db.pdfdb.find_one({'filename': self.upart})
                pdf_data = pdf_out.read()
            else:
                response = requests.get(
                        db.distdb.find_one(
                                {'part_num': self.upart.split('__')[0],
                                 'manufac': self.upart.split('__')[1]},
                                {'pdf_link': True}
                            )['pdf_link']
                    )
                if response.status_code == 200:
                    pdf_data = response.content
                else:
                    raise FileNotFoundError('Page returned %d' % response.status_code)
            with open(self.pdf_dir, 'wb') as fpdf:
                fpdf.write(pdf_data)
                
            allpages_mongoelem = []
            # page_num = 1
            # page_num = self.metadb.find_one({'upart': self.upart})['page'] + 1
            page_num += 1
            
            cmdline = '%s -f %d -l %d -q %s %s' % (
                     os.path.join(self.base_dir, 'pdftohtml.exe'), 
                     page_num, page_num + self.max_pdfpages - 1,
                     self.pdf_dir, self.html_dir
                )
            #print(cmdline)
            
            result = Popen(cmdline)
            result.wait()
            
        except FileNotFoundError:
            db.metadb.update_one({'upart': self.upart},
                                   {'$set': {'processed': 'error'}})
        try:   
            while True:
                pdf = ah.MongoDocCreator(
                        path=os.path.join(self.html_dir, 'page%s' % page_num),
                        part_num=self.upart
                    )
                for elem in pdf.make_mongoelem():
                    if elem:
                        dv = DataValidation(elem)
                        if (
                            # dv.word_length()
                            dv.no_fig()
                            and dv.alphaword_param()
                            and dv.unit_param()
                        ):
                            if (
                                dv.noparam_word()
                                or dv.nounit_param_word()
                                or dv.unit_param_word(page_num, allpages_mongoelem)
                            ):
                                elem = {
                                    **{'part_num': self.upart.split('__')[0],
                                       'manufac': self.upart.split('__')[1],
                                       'page_num': page_num}, **elem
                                }
                                elem['word'] += get_ngrams(elem['part_num']) \
                                                + get_ngrams(elem['manufac'])
                                allpages_mongoelem.append(elem)
                page_num += 1
        except (FileNotFoundError, lxml.etree.XMLSyntaxError):
            if allpages_mongoelem:
                db.partdb.insert_many(allpages_mongoelem)
            if page_num == 1:
                db.metadb.update_one({'upart': self.upart},
                                       {'$set': {'processed': 'error', 'page': 0}})
                # Popen('scrapy runspider --logfile=agent_log.log agent_spider.py'.split())
            else:
                db.metadb.update_one({'upart': self.upart},
                                       {'$set': {'processed': 'done'},
                                        '$inc': {'page': page_num}})
                success = True
                
        # Checking if need to delete PDF datasheets to save space
        if cfg.KEEP_GRIDFS_PDF and not cfg.KEEP_PDF_IN_DB:
            db.pdfdb.delete(pdf_out._id)
        
        shutil.rmtree(os.path.join(self.base_dir, self._upart),
                      ignore_errors=True)
        
        return success


class Dispatcher():
    def __init__(self):
        self.inprogress = {}
    
    def check_inprogress(self, stale_time=180):
        now = time.time()
        for upart, progress_start in self.inprogress.copy().items():
            if now - progress_start > stale_time:
                db.metadb.update_one(
                            {'upart': upart},
                            {'$set': {'processed': 'error'}}
                        )
                del self.inprogress[upart]
                
    def dispatch_loop(self):
        while True:
            need_to_process = db.metadb.find_one_and_update(
                        {'processed': 'pending'},
                        {'$set': {'processed': 'inprogress'}}
                    )
            if isinstance(need_to_process, dict):
                part = Analyzer(need_to_process['upart'])
                self.inprogress[part.upart] = time.time()
                if part.err_to.logger('', 'info', part.upart)(part.create_db)(need_to_process['page']):
                    del self.inprogress[part.upart]
            else:
                time.sleep(0.1)
            
            self.check_inprogress()
            if os.path.isdir(os.path.join('.', 'pdf_extract', 'stop')):
                break
            
if __name__ == '__main__':
    disp = Dispatcher()
    disp.dispatch_loop()

   