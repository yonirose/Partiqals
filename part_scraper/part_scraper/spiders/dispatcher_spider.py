# -*- coding: utf-8 -*-
"""
Created on Thu May 11 09:00:00 2017

@author: jrosenfe
"""
import sys
import os
import shutil
import time
from subprocess import Popen

sys.path.append(r'..\..\..')
import config as cfg
from utils.proxies import get_proxies
from utils.progress import print_prog

class DispatcherHandler():
    def __init__(self):
        pass
        
    def dispatch_loop(self):
        while True:
            if os.path.isdir('stop_spider'):
                print('\nStopping spider crawling...')
                break
            else:
                print('\n', time.strftime('%m/%d/%Y'), time.strftime('%H:%M:%S'),
                      ' Disk space ', end='')
                total, used, free = shutil.disk_usage('.')
                total = int(total/1024/1024/1024)
                used = int(used/1024/1024/1024)
                free = int(free/1024/1024/1024)
                print_prog(' '*5 + 'used', used, total, left_just=5,
                           bar_length=20, endwith='')
                print_prog(' free', free, total, left_just=5, bar_length=20)
                print('Getting fresh proxies...')
                #get_proxies()
                result = Popen(('scrapy crawl %s' % cfg.SPIDER_LIST[0]).split(' '))
                result.wait()
    
if __name__ == '__main__':
    if len(sys.argv) == 1 or sys.argv[1] == '--help':
        print('Dispatches scrapy spiders\n')
        print('--start = Start dispatch process')
        print('--stop = Stop dispatch process')
        print('--help = help menu')
    elif sys.argv[1] == '--start':
        disp = DispatcherHandler()
        #folders = os.listdir(os.path.join('..', '..', 'scraped_pdfs'))
        os.rename(os.path.join('.', 'stop_spider'),
                  os.path.join('.', 'start_spider'))
        disp.dispatch_loop() 
    elif sys.argv[1] == '--stop':
        os.rename(os.path.join('.', 'start_spider'),
                  os.path.join('.', 'stop_spider'))
    else:
        print('Incorrect command. Use --help to see the help menu.')
    
    
    