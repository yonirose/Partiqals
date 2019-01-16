# -*- coding: utf-8 -*-
"""
Created on Thu May 11 09:00:00 2017

@author: jrosenfe
"""
import sys
import os
import shutil
import time
from random import shuffle
from subprocess import Popen

from utils.error_logging import ErrorHandler
import config as cfg
from utils.progress import print_prog, scrapy_prog


class DispatcherHandler():
    def __init__(self):
        self.parser = ErrorHandler()
        
    def dispatch_loop(self):
        while True:
            if os.path.isdir('.stop_spider'):
                print('\nAll spiders stopped\n')
                break
            else:
                print('\n', time.strftime('%m/%d/%Y'), time.strftime('%H:%M:%S'),
                      ' Disk space [Gb]', end='')
                total, used, free = shutil.disk_usage('.')
                total = round(total/1024/1024/1024, 2)
                used = round(used/1024/1024/1024, 2)
                free = round(free/1024/1024/1024, 2)
                print_prog(' '*5 + 'used', used, total, left_just=5,
                           bar_length=20, endwith='')
                print_prog(' free', free, total, left_just=5, bar_length=20)
                print('\nSpider names: ')
                for spider_name in cfg.SPIDER_LIST:
                    print(f'{spider_name} ', end='')
                print('\n')
                shuffle(cfg.SPIDER_LIST)
                procs = [Popen(('scrapy crawl %s' % spider_to_run).split())
                         for spider_to_run in cfg.SPIDER_LIST]
                results = [proc.wait() for proc in procs]
                self.parse_logs()

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
            
    def parse_logs(self):
        self.parser.parse_errlog(os.path.join('..', '..', '..', 'logs'))
        
    def run_all(self):
        self.prep_spider()
        self.start_spider()
        
    def print_stats(self):
        scrapy_prog()

    def help(self):
        help_opts = [
                'Dispatches scrapy spiders and invoking misc. utils\n',
                '--start = Start dispatch process',
                '--stop = Stop dispatch process',
                '--prep = Prepare information for crawling',
                '--prep-start = Prepare and start a spider',
                '--parse-logs = Parse scrapy logs into three levels',
                '--stats = Print progress of all spiders',
                '--help = help menu'
            ]
        for opt in help_opts:
            print(opt)

    
if __name__ == '__main__':
    disp = DispatcherHandler()
    op = {'--start': disp.start_spider,
          '--stop': disp.stop_spider,
          '--prep': disp.prep_spider,
          '--prep-start': disp.run_all,
          '--parse-logs': disp.parse_logs,
          '--stats': disp.print_stats,
          '--help': disp.help}
    try:
        op[sys.argv[1]]()
    except (KeyError, IndexError):
        print('Incorrect command. Use --help to see the help menu.')
            
