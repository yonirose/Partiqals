# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 09:15:39 2016

@author: jrosenfe
"""
import os
import traceback
from functools import wraps
from datetime import datetime

import config as cfg

class ErrorHandler():
    def __init__(self, base_path=None, log_name='analyze_err.log', reset_log=False):
        if base_path is None:
            self.base_path = os.path.join('..', '..', '..', 'logs')
        else:
            self.base_path = base_path
            
        self.log_name = log_name
        if reset_log:
            open(self.path, 'w').close()
        self.last_mess = ''
      
    def register(self, message, mess_type, part_num):
        with open(os.path.join(self.base_path, self.log_name),
                  'a', encoding='utf-8') as f:
            time_sig = datetime.now().strftime('%m-%d-%Y %H:%M:%S')
            new_mess = '[%s] %s: %s' % (part_num, mess_type.upper(), message)
            # Suppress repeating errors
            if not new_mess == self.last_mess: 
                f.write('%s %s\n' % (time_sig, new_mess))
                tb = traceback.format_exc().split('\n')[-4:]
                tb = [_.strip() for _ in tb]
                tb = '\n'.join(tb)
                f.write('%s%s\n' % (tb, '-'*100))
                self.last_mess = new_mess
    
    def logger(self, term, mess_type, part_num):
        def decort(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    self.register('%s <%s>' % (term, e.args[0]), mess_type,
                                               part_num)
            return wrapper
        return decort
    
    def parse_errlog(self, base_path=None):
        if base_path is None:
            base_path = self.base_path
        found_err = False
        first_date = ''
        last_line = ''
        last_line_info = ''
                
        cat_errs = {}
        subcat_errs = {}
        
        for log_file in [f'{spider_name}_scrapy.log'
                         for spider_name in cfg.SPIDER_LIST]:
            log_name = log_file.split('.')[0]
            with open(os.path.join(base_path, log_name + '_L1.log'), 'at') as errf, \
                 open(os.path.join(base_path, log_file), 'r') as f:
                errf.write('~'*100)
                # Read first two lines of the entire log file
                for _ in range(2):
                    errf.write(f.readline())
                errf.write('-'*100+'\n')
                # Analyze rest of the lines
                for ix, line in enumerate(f):
                    # print(ix, end='\r')
                    # sys.stdout.flush()
                    if 'ERROR:' in line or found_err:
                        line_date = line.split(' ')[0]
                        if found_err:
                            if first_date == line_date:
                                found_err = False
                                errf.write('-'*100+'\n')
                                if last_line in cat_errs:
                                    cat_errs[last_line] += 1
                                    subcat_errs[last_line].append(last_line_info)
                                else:
                                    cat_errs[last_line] = 1
                                    subcat_errs[last_line] = [last_line_info]
                            else:
                                errf.write(line)
                                try:
                                    last_line = line[:line.rindex(": '")].strip()
                                    last_line_info = line[line.rindex(": '")+1:].strip()
                                except ValueError:
                                    last_line = line
                                    last_line_info = ''
                        else:
                            found_err = True
                            first_date = line_date
                            errf.write(line)
                
                # Save statistics
                with open(os.path.join(base_path, log_name + '_L3.log'), 'at') as fr, \
                     open(os.path.join(base_path, log_name + '_L2.log'), 'at') as f:
                    fr.write('~'*100)
                    f.write('~'*100)
                    for key, val in cat_errs.items():
                        f.write('%s --> %s\n' % (key.strip('\n'), val))
                        f.write('='*100+'\n')
                        fr.write('%s --> %s\n' % (key.strip('\n'), val))
                        fr.write('-'*len(key.strip('\n'))+'\n')
                        for more_info in list(set(subcat_errs[key])):
                            if more_info:
                                f.write(more_info+'\n')
                        f.write('\n')
            

if __name__ == '__main__':
    e = ErrorHandler()
    #e.register('Hello. This is info Ω ≤', 'info')



