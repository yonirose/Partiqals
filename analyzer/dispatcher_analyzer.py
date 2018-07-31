# -*- coding: utf-8 -*-
"""
Created on Thu May 11 09:00:00 2017

@author: jrosenfe
dispatcher_process_v5
"""
import sys
import os
import shutil
import time
from subprocess import Popen
from bson.objectid import ObjectId
import db_setup as db
import config as cfg

class DispatcherHandler():
    def __init__(self, num_proc=cfg.NUM_PROC):
        self.base_dir = os.path.join('.', 'pdf_extract')
        self.num_proc = num_proc
    
    def dispatch_proc(self):
        for _ in range(self.num_proc):
            Popen('python analyze_pdf.py'.split(' '))
            time.sleep(0.1)
                  
    def dispatch_loop(self):
        self.dispatch_proc()
        
        while True:
            if os.path.isdir(os.path.join(self.base_dir, 'stop')):
                print('\nStopping dispatch process...')
                break
            else:
                time.sleep(1)
    
if __name__ == '__main__':
    if len(sys.argv) == 1 or sys.argv[1] == '--help':
        print('Dispatches PDF files for processing\n')
        print('--start = Start dispatch process')
        print('--stop = Stop dispatch process')
        print('--stat = Status report')
        print('--help = help menu')
    elif sys.argv[1] == '--start':
        disp = DispatcherHandler(num_proc=cfg.NUM_PROC)
        open(os.path.join('..', 'logs', 'analyze_err.log'), 'w').close()
        folders = os.listdir(os.path.join('.', 'pdf_extract'))
        if len(folders) > 2:
            print('Deleting the following remaining folders:')
            for folder in folders:
                if '__' in folder:
                    print(folder)
                    shutil.rmtree(os.path.join('.', 'pdf_extract', folder),
                                               ignore_errors=True)
        os.rename(os.path.join('.', 'pdf_extract', 'stop'),
                  os.path.join('.', 'pdf_extract', 'start'))
        # Make all in progress PDFs as errored
        for err_pdf in db.metadb.find({'processed': 'inprogress'}):
            db.metadb.update_one({'_id': ObjectId(err_pdf['_id'])},
                                 {'$set': {'processed': 'error'}})
        print('\nDispatching process has started')
        disp.dispatch_loop() 
    elif sys.argv[1] == '--stop':
        try:
            os.rename(os.path.join('.', 'pdf_extract', 'start'),
                      os.path.join('.', 'pdf_extract', 'stop'))
        except FileNotFoundError:
            pass
    elif sys.argv[1] == '--stat':
        false_pdf = db.metadb.find({'processed': 'pending'})
        true_pdf = db.metadb.find({'processed': 'done'})
        prog_pdf = db.metadb.find({'processed': 'inprogress'})
        err_pdf = db.metadb.find({'processed': 'error'})
        print('Number of remaining PDF documents to analyze: %s'
              % false_pdf.count())
        print('Number of successfully processed PDF documents: %s'
              % true_pdf.count())
        print('Number of currently processed PDF documents: %s'
              % prog_pdf.count())
        print('Number of errored PDF documents: %s'
              % err_pdf.count())
        print('\nTotal PDF documents: %s' % (false_pdf.count()
                                             +true_pdf.count()
                                             +prog_pdf.count()
                                             +err_pdf.count()))
    else:
        print('Incorrect command. Use --help to see the help menu.')
    
    
    