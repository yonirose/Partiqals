# -*- coding: utf-8 -*-
"""
Created on Sat Mar  3 16:46:42 2018

@author: jrosenfe
v2
"""

import re
from collections import namedtuple, abc

#from ngram import NGram

from utils.misc import get_ngrams

'''
if __name__ == '__main__':
    import symb_unit as symb
else:
'''
from analyzer import symb_unit as symb


class TokenHandler():
    def __init__(self):
        self.result = {'cond': [], 'param': [], 'unit': [], 'term': [],
                       'word': []}
    
    def change_token(self, token_type, token_value, token_loc=-1):
        Token = namedtuple('Token', ['type', 'value'])
        self.tokens[token_loc] = Token(token_type, token_value)
        self.tokens_sws[token_loc] = Token(token_type, token_value)
            
    def term(self, term):
        if term == 'at': # This is needed since RegEx cannot recognize it as COND
            self.change_token('COND', term)
            self.cond(term)
            return
        
        def phrase():
            if self.tokens[-2].type == 'COND':
                self.result['cond'][-1] += ' %s' % term
            else:
                self.result['term'].append(term.strip('.'))
            
        def num():
            try:
                self.result['term'].append(str(self.result['param'].pop()[0])+term)
            except IndexError:
                self.result['term'][-1] += term
        
        def cond():
            self.result['cond'][-1] += ' ' + term
        
        def term_range():
            self.result['term'][-1] = self.result['term'][-1].strip('-')
            self.result['term'].append(term)
        
        func = {'COND': cond, 'SWS': phrase, 'MWS': phrase, 'NUM': num,
                'UNIT': phrase, 'TERM': phrase, 'OPRND': phrase, 'RANGE': term_range}
        key = 'SWS' if self.tokens_sws[-2].type == 'SWS' else self.tokens[-2].type
        # key = self.tokens[-2].type
        if self.verbose:
            print('term key', key)
        func[key]()
        # To account for terms like 34ER-35KNL
        try:
            if self.result['term'][-2][-1] == '-':
                last_term = self.result['term'].pop()
                self.result['term'][-1] += last_term
        except IndexError:
            pass
    
    def cleanup_num(self, num):
        num = num.lstrip('0').replace(' ', '')
        if num:
            if num[0] == '.':
                num = '0' + num
        else:
            num = '0'
        return num
        
    def num(self, num):
        if num in symb.package_codes:
            self.change_token('TERM', num)
            self.term(num)
            return
        num = self.cleanup_num(num)
            
        def cond():
            self.result['cond'][-1] += ' ' + num
            self.change_token('COND', num) 
            
        def oprnd():
            if self.tokens[-3].type == 'NUM':
                temp_result = tuple()
                for param in self.result['param'][-1]:
                    temp_result += (eval(str(param)
                                        + self.tokens[-2].value
                                        + num), )
                self.result['param'][-1] = temp_result      
            elif self.tokens[-3].type == 'UNIT':
                raise KeyError # Forces to execute the code in the else block
            elif self.tokens[-3].type == 'TERM':
                single_num()
        
        def single_num():
            if self.tokens[-2].type == 'COND':
                cond()
            elif self.tokens[-2].type == 'RANGE':
                num_range()
            else:
                self.result['param'].append((eval(num),))
        
        def num_range():
            def num_key():
                self.result['param'][-1] = (self.result['param'][-1][0], eval(num))
                
            def unit():
                    self.result['param'][-1] = (self.result['param'][-1][0],
                                                eval(num),
                                                self.result['param'][-1][1])
                
            def term():
                self.result['term'][-1] += ('' if self.result['term'][-1][-1] == '-'
                                            else '-') + num
            
            def mws():
                pass
            
            def anything_else():
                self.result['term'][-1] += ' ' + self.tokens[-2].value + num
                self.change_token('TERM', num)
                
            
            func = {'NUM': num_key, 'UNIT': unit, 'TERM': term, 'MWS': unit}
            try:
                key = self.tokens[-3].type
                func[key]()
            except IndexError:
                anything_else()
            
        def number():
            if num[0] == '+' and self.tokens_sws[-2].type == 'NUM':
                self.result['param'][-1] = (eval(self.tokens_sws[-2].value
                                            + num),)
            
        func = {'COND': cond, 'OPRND': oprnd, 'UNIT': single_num,
                'SWS': single_num, 'MWS': single_num, 'RANGE': num_range,
                'NUM': number}
        key = 'SWS' if self.tokens_sws[-2].type == 'SWS' else self.tokens[-2].type
        if self.verbose:
            print('num key', key)
        try:
            func[key]()
        except KeyError:
            if self.result['param']: # To account for cases like m2 etc.
                self.result['param'][-1] = (
                        self.result['param'][-1][0],
                        self.result['param'][-1][1] + str(num)
                    )
        
    def unit(self, unit):
        unit = unit.strip()
        for _ in ['-', '.']:
            unit = unit.replace(_, '')
        
        def mws(prefix=''):
            self.result['unit'].append(prefix+unit)
        
        def num(prefix=''):
            # The equality to 4 is to account for situation like 1Ohm to 1MOhm
            if not len(self.result['param'][-1]) == 4:
                self.result['param'][-1] = self.result['param'][-1] + (prefix+unit,)
                
        def cond_num():
            self.result['cond'][-1] += ' ' + unit
            
        def perc_oprnd():
            try:
                if self.tokens[-4].type == 'NUM':
                    self.result['param'][-1] = (self.result['param'][-1][0],
                                                '%/' + unit)
                else:
                    raise IndexError
            except IndexError:
                self.result['unit'].append('%/' + unit)
        
        def range_term():
            self.result['term'][-1] += ' ' + unit
            self.change_token('TERM', unit)
            
        def num_oprnd():
            if self.tokens[-3].value == '1' and self.tokens[-4].type == 'MWS':
                self.result['param'].pop()
                mws('1/')
            elif self.tokens_sws[-4].type == 'SWS':
                self.result['param'].pop()
                num(prefix='1/')
            else:
                num(prefix='1/')
                    
        funcs = {'MWS': mws, 'MWS_NUM': num, 'RANGE_NUM': num, 'PM_NUM': num,
                 'NUM_NUM': num, 'UNIT_NUM': num, 'PERC_MWS': mws, 'MWS_TERM': mws,
                 'UNIT_MWS': mws, 'NUM_PERC': num, 'TERM_NUM': num, 'COND_TERM': mws,
                 'NUM_TERM': mws, 'COND_NUM': cond_num, 'TERM_MWS': mws,
                 'OPRND_NUM': num, 'PERC_OPRND': perc_oprnd, 'NUM_MWS': mws,
                 'NUM_UNIT': mws, 'TERM_UNIT': mws, 'UNIT_UNIT': mws,
                 'COND_PM': cond_num, 'RANGE_TERM': range_term,
                 'NUM_OPRND': num_oprnd, 'COND_COND': cond_num}
        try:
            key = self.tokens[-3].type + '_' + self.tokens[-2].type
        except IndexError:
            key = self.tokens[-2].type
        if self.verbose:
            print('unit key', key)
        funcs[key]()
    
    def range_boundr(self, r):
        r = r.strip()
        def num_range():
            self.result['param'][-1] = (self.result['param'][-1][0],)
            
        def term_range():
            self.result['term'][-1] += '-' # + str(next_num)
        
        def term_term():
            self.result['term'][-1] += r
            
        def cond_cond():
            self.change_token('COND', r)
            self.result['cond'][-1] += ' ' + r
            
        def unit_term():
            self.result['cond'][-1] += ' %s %s' % (self.result['term'].pop(), r)
            self.change_token('COND', r)
            
        funcs = {'NUM_RANGE': num_range, 'TERM_RANGE': term_term,
                 'MWS_TERM': term_term, 'TERM_TERM': term_term,
                 'COND_COND': cond_cond, 'UNIT_TERM': unit_term}
        try:
            key = self.tokens[-3].type + '_' + self.tokens[-2].type
        except IndexError:
            self.tokens.pop()
            return
            
        if self.verbose:
            print('range key', key)
        funcs[key]()
    
    def pm_mp(self, pm_symb):
        next_num = eval(self.cleanup_num(next(self.gen, None).value))
        
        def mws_pm():
            self.result['param'].append((-next_num, next_num))
        
        def num_pm():
            if self.tokens[-4].type == 'COND':
                self.result['cond'][-1] += ' %s %s' % (pm_symb, next_num)
            elif self.tokens[-4].type == 'PM':
                mws_pm()
            else:
                mdiff = self.result['param'][-1][0] - next_num
                pdiff = self.result['param'][-1][0] + next_num
                self.result['param'][-1] = (min(mdiff, pdiff), max(mdiff, pdiff))
               
        def unit_pm():
            if len(self.result['param'][-1]) > 2:
                mws_pm()
                return
            
            '''
            if len(self.results['param'][-1]) > 2 and \
                self.result['param'][-1][-1].isalpha(): 
            '''
            
            unit = self.result['param'][-1][1]
            
            num_pm()
            self.result['param'][-1] = (self.result['param'][-1][0],
                                        self.result['param'][-1][1],
                                        unit)
        
        def cond_pm():
            self.result['cond'][-1] += ' ' + pm_symb + str(next_num)
            self.tokens.pop()
        
        funcs = {'MWS_PM': mws_pm, 'NUM_PM': num_pm, 'UNIT_PM': unit_pm,
                 'COND_PM': cond_pm, 'TERM_PM': mws_pm}
        key = self.tokens[-3].type + '_' + self.tokens[-2].type
        if self.verbose:
            print('pm_mp key', key)
        funcs[key]()
        
    def perc(self, perc):
        def mws_pm_num():
           self.change_token('UNIT', perc)
           self.unit(perc)
        
        def num_num():
            self.result['param'] = (
                    self.result['param'][:-2]
                    + [(self.result['param'][-2][0]
                    + self.result['param'][-2][0]*self.result['param'][-1][0]/100,)]
                )

        def num_unit(): # Fix this method when \d-\d range will be working 
            if self.tokens[-2].value[0] == '+' or self.tokens[-2].value[0] == '-':        
                unit = self.result['param'][-2][1]
                num_num()
                self.result['param'][-1] = (self.result['param'][-1][0], unit)
            else:
                mws_pm_num()
    
        def num_pm():
            num = eval(self.tokens[-4].value)
            perc_num = eval(self.tokens[-2].value)
            self.result['param'][-1] = (num*(1 - perc_num/100),
                                        num*(1 + perc_num/100),)
            
        def unit_pm_num():
            if len(self.result['param'][-1]) == 2:
                self.result['param'][-1] = (self.result['param'][-1][0],
                                            self.result['param'][-1][1],
                                            perc)
                return
            
            unit = self.result['param'][-1][2]
            num = eval(self.tokens[-5].value)
            perc_num = eval(self.tokens[-2].value)
            self.result['param'][-1] = (num*(1 - perc_num/100),
                                        num*(1 + perc_num/100),
                                        unit)
            
        def cond_cond_cond():
            self.change_token('COND', perc)
            self.result['cond'][-1] += perc
        
        def perc_term_num():
            self.result['param'][-1] = (self.result['param'][-1][0], perc)
            
        funcs = {'MWS_NUM': mws_pm_num, 'NUM_MWS_NUM': mws_pm_num,
                 'UNIT_MWS_NUM': mws_pm_num, 'MWS_PM_NUM': mws_pm_num,
                 'MWS_NUM_NUM': num_num, 'NUM_NUM_NUM': num_num, 'NUM_NUM': num_num,
                 'NUM_UNIT_NUM': num_unit, 'NUM_PM_NUM': num_pm,
                 'UNIT_PM_NUM': unit_pm_num, 'NUM_OPRND_NUM': mws_pm_num,
                 'NUM_RANGE_NUM': mws_pm_num, 'COND_COND_COND': cond_cond_cond,
                 'TERM_PM_NUM': unit_pm_num, 'PERC_TERM_NUM': perc_term_num,
                 'PERC_MWS_NUM': perc_term_num}
        try:
            key = (self.tokens[-4].type + '_'
                   + self.tokens[-3].type + '_'
                   + self.tokens[-2].type)
        except IndexError:
            try:
                key = self.tokens[-3].type + '_' + self.tokens[-2].type
            except IndexError:
                key = self.tokens[-2].type
            
        if self.verbose:
            print('perc key', key)
        funcs[key]()

    def cond(self, cond):
        def term():
            # try:
            self.result['cond'].append(self.result['term'].pop()+ ' ' + cond)
            # except IndexError:
            #   print(self.text)
            #   assert False
        
        def at():
            def concat_cond(obj):
                unpack = {
                        1: lambda: str(obj[0]),
                        2: lambda: '%s %s' % (obj[0], obj[1]) \
                            if isinstance(obj[1], str) else '%s to %s' % (obj[0], obj[1]),
                        3: lambda: '%s to %s %s' % (obj[0], obj[1], obj[2]),
                        4: lambda: '%s %s to %s %s' % (obj[0], obj[2], obj[1], obj[3])
                    }
                return unpack[len(obj)]
                    
            if self.tokens[-2].type == 'UNIT':
                if self.tokens[-3].type == 'NUM':
                    # last_param = self.result['param'].pop()
                    self.result['cond'].append(concat_cond(self.result['param'].pop())()
                                               + ' '
                                               + cond
                                               + ' ')
                    '''
                    self.result['cond'].append(str(last_param[0])
                                               + str(last_param[1])
                                               + ' '
                                               + cond
                                               + ' ')
                    '''
                else:
                    self.result['cond'].append(self.result['unit'].pop()
                                               + ' '
                                               + cond
                                               + ' ')
            else:
                try:
                    self.result['cond'][-1] += ' ' + cond
                except IndexError: # Catches if self.result['cond'] is empty
                    if len(self.result['term']): 
                        self.result['cond'].append(self.result['term'].pop()
                                                   + ' '
                                                   + cond)
                    else:
                        self.result['cond'].append(cond)
        
        def range_boundr():
            self.tokens.pop()
            self.tokens_sws.pop()
        
        func = {'TERM': term, 'UNIT': at, 'MWS': at, 'NUM': at,
                'RANGE': range_boundr}
        key = self.tokens[-2].type
        if self.verbose:
            print('cond key', key)
        func[key]()
        
    def note(self, note):
        pass
                
        
class Parser(TokenHandler):
    def __init__(self, verbose=False):
        self.verbose = verbose
        super().__init__()
        base_unit = r'-?[\d[ ?fpnuµmkKMGT]?-?%s/?\.?(/.\d*)?'
        all_units = ''
        for units in symb.phy_units.values():
            for unit in units:
                all_units += (base_unit % unit + ' ' + '|'
                             + base_unit % unit.upper() + ' ' + '|'
                             + base_unit % unit.lower() + ' ' + '|')
                '''
                # To account for V / m units
                if '/' in unit:
                    slash_loc = unit.index('/')
                    all_units += base_unit % unit[0:slash_loc] + ' / ' \
                                 + unit[slash_loc+1:] + ' ' + '|'
                '''

        # The extra '|m )' is to account for mm and m
        all_units = r'(?P<UNIT>'+ all_units[:-1] + '|m )'
        
        '''
        all_units_up = r'(?P<UNIT_UP>'+ all_units_up[:-1] + '|m )'
        all_units_dn = r'(?P<UNIT_DN>'+ all_units_dn[:-1] + '|m )'
        '''
        
        token_def = [
                r'(?P<COND>[=<>@≤≥])',
                r'(?P<INF>[+-]?inf )',
                r'(?P<PERC>%)',
                r'(?P<RANGE>\s?to |\s?[-~] )', # Replace '\d-\d' to ' - '
                #r'(?P<RANGE>\S[-~]\S| to | [-~] )',
                r'(?P<MWS>\s{2,})',
                r'(?P<SWS>\s)',
                r'(?P<NUM>[+-]?\.?\d+\.?\d*(?:[Ee] ?\+?-? ?[0-9]+)?)',
                r'(?P<OPRND>[\*\/]+)',
                all_units,
                r'(?P<NOTE>[Nn]ote *\d+\.?\d{0,}'
                + r'|([Nn]ote *)?\[\d+\.{0,1}\d{0,}\]'
                + r'|([Nn]ote *)?\(\d+\.{0,1}\d{0,}\))',
                r'(?P<TERM>[0-9a-zA-Z\-\.][a-zA-Z\-\.][a-zA-Z0-9\-\.]*)',
                #r'(?P<TERM>\d{0,}\w{1,})',
                r'(?P<PM>±|∓|\+/-*|-/\+*)'
            ]
        
        self.master_pat = re.compile('|'.join(token_def))
        self.symb_pat = re.compile(r'[a-zA-Z/%°.\-\–]+|[\[\]()\^²³ꝏ˚º,]')
        
        self.custom_subs = [
                (re.compile(r'\(\d+(\.\d+)?\)'), ''),
                (re.compile(r'" L'), r'" Length'),
                (re.compile(r'" W'), r'" Width'),
                (re.compile(r' / '), r'/'),
                (re.compile(r'^A '), r''),                       # Remove A at the start of a sentence
                (re.compile(r'\. ?A'), r''),                     # Remove A after a period
                (re.compile(r'([\d ])(x|×)([\d ])'), r'\1*\3'),  # Convetr axb to a*b
                (re.compile(r'(\*10)([\–\-+]\d)'), r'e\2'),      # Convert a*10-b to ae-b
                (re.compile(r'([\d\w])(-|~|±|\+/-|-/\+)(\d)'), r'\1 \2 \3'), # Convert a-b to a - b
                (re.compile(r'(m|M)(eg|EG)(ohm|Ohm|OHM)'), 'MΩ'),
                (re.compile(r'( DC | dc | Dc )'), ' 0 '),
                (re.compile(r'([a-z] *)(- )(\d)'), r'\1-\3'),
                (re.compile(r'( {2,})(- )(\d)'), r'\1-\3'),
                (re.compile(r'(\+ )(\d)'), r'\2')
            ]
        
        self.token_func = {'TERM': self.term, 'NUM': self.num,
                           'UNIT': self.unit, 'UNIT_UP': self.unit, 'UNIT_DN': self.unit,
                           'RANGE': self.range_boundr,
                           'PM': self.pm_mp, 'PERC': self.perc,
                           'COND': self.cond, 'NOTE': self.note}
    
        self.new_units = {}
        for new_unit, old_units in symb.unit_replace.items():
            for old_unit in old_units:
                if old_unit[-1] == '!': # '!' at the end of an unit means not to have upper and lower a veriosn of it
                    self.new_units[old_unit[:-1]] = new_unit
                else:
                    self.new_units[old_unit] = new_unit
                    self.new_units[old_unit.lower()] = new_unit
                    self.new_units[old_unit.upper()] = new_unit
                
        self.tokens = []
        self.tokens_sws = []
    
    def preprocess(self, text):
        text = f'  {text}  '
        for pat, sub in self.custom_subs:
            text = re.sub(pat, sub, text)
        
        # Find and change units and symbols to a defined form
        for word in re.findall(self.symb_pat, text):
            for w in [word, word[1:]]: # Try to remove first letter since it might be a unit with a prefix like mWatt
                try:
                    w = w.strip()
                    text = text.replace(w, self.new_units[w])
                    break
                except KeyError:
                    pass
        
        if self.verbose:
            print('text=|%s|' % text)
        return text
    
    @property
    def conversion_ratio(self):
        occur_cnt = 0
        for item_type in ['cond', 'param', 'unit', 'term']:
            if isinstance(self.result[item_type], abc.Sequence):
                for instances in self.result[item_type]:
                    for instance in instances:
                        if str(instance) in self.text:
                            occur_cnt += 1
            elif str(self.result[item_type]) in self.text:
                occur_cnt += 1
        return occur_cnt/len(self.text.strip().split(' '))
                
    def postprocess(self):
        # Remove unit duplicates
        self.result['unit'] = list(set(self.result['unit']))
        
        # Remove term duplicates WITH order
        terms = []
        for term in self.result['term']:
            if term not in terms:
                terms.append(term)
        self.result['term'] = terms
        
    
        # Conversion sanity check. If less than 0.5 just keep the raw text
        if self.conversion_ratio < 0.5:
            self.reset_result()
            self.result['term'] = [self.raw_text]
    
        # Generate words
        for term in self.result['term']:
            if len(term) > 3:
                self.result['word'] += get_ngrams(term)
            else:
                self.result['word'].append(term)
            
    def generate_tokens(self, text):
        pat = self.master_pat
        Token = namedtuple('Token', ['type', 'value'])
        scanner = pat.scanner(text)
        for m in iter(scanner.match, None):
            if m.lastgroup == 'SWS':
               self.tokens_sws.append(Token(m.lastgroup, m.group()))
               continue
            else:
                self.tokens.append(Token(m.lastgroup, m.group()))
                self.tokens_sws.append(self.tokens[-1])
                yield self.tokens[-1]
    
    def parse(self, text):
        self.reset_result()
        self.raw_text = text
        self.text = self.preprocess(text)
        self.gen = self.generate_tokens(self.text)
        for tok in self.gen:
            if self.verbose:
                print(tok)
            try:
                self.token_func[tok.type](tok.value)
            except KeyError: # This catches also other func[key] that does not exist and do nothing
                pass
            except IndexError:
                self.reset_result()
                self.result['term'] = [self.raw_text]
            
        self.postprocess()
    
    def reset_result(self):
        self.result = {'cond': [], 'param': [], 'unit': [], 'term': [],
                       'word': []}
        self.tokens = []
        self.tokens_sws = []


if __name__ == '__main__':
    p = Parser() 
    p.parse(' while at the Hello fast-asleep.  1/5V 4*2+/-10mA from 45deg-F  Note (1)') # preprocees by adding two spaces at the beginning and end
    # p.parse('15KE6.8-45KNL series 45mA-150')
    print(p.result)

# ' 3-food12.K  ±12 12.3 - 14.0E+1 A +/- 12 ±50mV 43e-2 5mV to 45V '
