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
#from utils.proxies import get_proxies
from utils.progress import print_prog


class DispatcherHandler():
    def __init__(self):
        pass
        
    def dispatch_loop(self):
        while True:
            if os.path.isdir('.stop_spider'):
                print('\nStopping crawling spider...')
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

                procs = [Popen(('scrapy crawl %s' % spider_to_run).split())
                         for spider_to_run in cfg.SPIDER_LIST]
                results = [proc.wait() for proc in procs]

    def start_spider(self):
        os.rename(os.path.join('.', '.stop_spider'),
                  os.path.join('.', '.start_spider'))
        self.dispatch_loop()

    def stop_spider(self):
        os.rename(os.path.join('.', '.start_spider'),
                  os.path.join('.', '.stop_spider'))

    def prep_spider(self):
        for spider_to_prep in cfg.SPIDER_LIST:
            result = Popen(('scrapy crawl %s_prep' % spider_to_prep).split())
            result.wait()

    def run_all(self):
        self.prep_spider()
        self.start_spider()

    def help(self):
        print('Dispatches scrapy spiders\n')
        print('--start = Start dispatch process')
        print('--stop = Stop dispatch process')
        print('--prep = Prepare information for crawling'),
        print('--prep-start = Prepare and start a spider')
        print('--help = help menu')

    
if __name__ == '__main__':
    disp = DispatcherHandler()
    op = {'--start': disp.start_spider,
          '--stop': disp.stop_spider,
          '--prep': disp.prep_spider,
          '--prep-start': disp.run_all,
          '--help': disp.help}
    try:
        op[sys.argv[1]]()
    except (KeyError, IndexError):
        print('Incorrect command. Use --help to see the help menu.')
            
