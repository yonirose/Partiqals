# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 16:19:13 2017

@author: jrosenfe
v4
"""

from numpy import inf
import pandas as pd
from textblob import TextBlob

from analyzer import analyze_html as ah
from analyzer import line_parser as lp
import db_setup as db
import config as cfg
from utils.misc import get_ngrams


class QueryHandler():
    def __init__(self, qs):
        for _ in ['greater than', 'larger than', 'more than', 'not less than',
                  'not smaller than', '>', '>=']:
            qs = qs.replace(_, 'inf - ')
        for _ in ['less than', 'smaller than', 'not greater than',
                  'not larger than', 'not more than', '<', '<=']:
            qs = qs.replace(_, '-inf - ')
        self.qs = qs.replace(' and ', ' + ')
        
    def run_query(self):
       for q in [_.strip() for _ in self.qs.split('+')]:
           yield QueryFinder(q).simple_query()


class QueryFinder():
    def __init__(self, q):
        self.q = q
        
    def simple_query(self):
        p = lp.Parser()
        p.parse(self.q)
        query = ah.MongoDocCreator(ext_elems_to_analyze=[p.result])
        elem = list(query.make_mongoelem())[0] # There should be only one element in this list. See analyze_html.py
        print('elem: ', elem)
        
        blobs = []
        for trm in elem['term']:
            blob_tags = TextBlob(trm).tags
            blobs += [blob[0].lower() for blob in blob_tags if blob[1] == 'JJ' or
                      blob[1] == 'NNP' or blob[1] == 'NN' or blob[1] == 'VBG' or
                      blob[1] == 'RB' or blob[1] == 'NNS' or blob[1] == 'VBD' or
                      blob[1] == 'VBN']
        
        try: # Try if 'from' and 'to' fields exist. In other words if there are numbers in the query
            if type(elem['param']) == list or not elem['param']:
               elem_from = elem['from']
               elem_to = elem['to']
            else:
               elem_from = elem_to = (elem['from'] + elem['to'])/2
            if elem_to == inf:
                query_dict = {'word': {'$all': blobs},
                              'to': {'$gte': elem_from},
                              'unit': elem['unit']}
            elif elem_from == -inf:
                query_dict = {'word': {'$all': blobs},
                              'from': {'$lte': elem_to},
                              'unit': elem['unit']}
            else:
                query_dict = {'word': {'$all': blobs},
                              'from': {'$lte': elem_from},
                              'to': {'$gte': elem_to},
                              'unit': elem['unit']}
        except KeyError:
            query_dict = {'word': {'$all': blobs}}
        print('qd: %s\n' % query_dict)
        
        parts_found = db.partdb.find(query_dict, {'_id': False,
                                                    'word': False,
                                                    # 'term': False,
                                                    # 'cond': False,
                                                    # 'param': False,
                                                    # 'manufac': False
                                                    })
        return Parts(parts_found=parts_found, 
                     user_term=elem['term'][0],
                     q=self.q)


class Parts():
    # This include found parts that don't have units and params
    all_partnums = []
    # Only parts that have params and units
    param_unit_partnums = []
    
    def __init__(self, parts_found, user_term='', q=''):
        self.raw_parts_found = list(parts_found)
        self.parts_found = []
        self.user_term = user_term
        self.partnum_found = []
        self.num_partsfound = []
        self.q = q
        self.unit = ''

    def process_parts(self):        
        if self.raw_parts_found:
            try:
                self.raw_parts_found = pd.DataFrame(self.raw_parts_found)
                
                self.parts_found = self.raw_parts_found.drop(
                        self.raw_parts_found[
                                self.raw_parts_found['param'] == False
                            ].index
                    )
                self.parts_found = self.raw_parts_found.drop(
                        self.raw_parts_found[
                                self.raw_parts_found['unit'] == ''
                            ].index
                    )
                self.parts_found = self.parts_found.sort_values(by='part_num')
               
                self.parts_found.drop_duplicates(
                        subset=['part_num', 'manufac', 'from',
                                'to', 'unit', 'unit_scale'],
                        inplace=True
                    )
                
                # v is for value to be plotted
                self.parts_found['vfrom'] = self.parts_found[
                        ['param', 'from','to']].apply(
                                lambda _: _['from']
                                if type(_['param'])==list else (_['from']+_['to'])/2,
                                axis=1
                            )
                
                self.parts_found['vto'] = self.parts_found[
                        ['param', 'from', 'to']].apply(lambda _: _['to']
                        if type(_['param'])==list else (_['from']+_['to'])/2,
                        axis=1)
                
                # h is for hover tooltip when plotted
                self.parts_found['hval'] = \
                        self.parts_found['param'].apply(
                            lambda _: str(min(_))+' to '+str(max(_))
                            if isinstance(_, list) else str(_)
                        )

                self.parts_found['hunit'] = self.parts_found[
                        ['unit', 'unit_scale']].apply(
                                lambda _: _['unit_scale']+_['unit'],
                                axis=1
                            )
               
                units = [_ for _ in set(self.parts_found['unit']) if _]
                if units:
                    self.unit = units[0]
                for unit in units[1:]:
                   if unit:
                       self.unit = self.unit + ', ' + unit
                
                self.min_from = self.parts_found['vfrom'].min()
                self.max_from = self.parts_found['vfrom'].max()
                self.min_to = self.parts_found['vto'].min()
                self.max_to = self.parts_found['vto'].max()
            
                '''
                scale_tocode = {'T': 4, 'G': 3, 'M': 2, 'k': 1, '': 0, 'm': -1,
                                'u': -2, 'n': -3, 'p': -4}
                code_toscale = {4: (1e12, 'T'), 3: (1e9, 'G'), 2: (1e6, 'M'),
                                1: (1e3, 'k') , 0: (1, ''), -1: (1e-3, 'm'),
                                -2: (1e-6, 'u'), -3: (1e-9, 'n'),
                                -4: (1e-12, 'p')}
                if len(self.unit) > 1:
                    self.unit = ', '.join(self.unit)
                else:
                    self.unit = list(self.unit)[0]
                    
                    scale_units = set(self.parts_found['unit_scale'])
                    scale_acc = 0
                    for scale_unit in scale_units:
                        scale_acc += scale_tocode[scale_unit]
                    scale_acc = round(scale_acc/len(scale_units))
                    self.unit = code_toscale[scale_acc][1]+self.unit
                    scale = code_toscale[scale_acc][0]
                    self.parts_found['vfrom'] = self.parts_found['vfrom'].apply(lambda _: _/scale)
                    self.parts_found['vto'] = self.parts_found['vto'].apply(lambda _: _/scale)
                '''
            except KeyError:
                pass # Catching and passing key errors on parts that don't have param or unit
            self.partnum_found = list(
                        self.raw_parts_found['part_num'].drop_duplicates()
                    )
            self.num_partsfound = len(self.partnum_found)
            Parts.param_unit_partnums = list(
                    set(Parts.param_unit_partnums)
                    | set(self.partnum_found)
                )
            Parts.all_partnums = list(
                    set(Parts.all_partnums)
                    | set(self.raw_parts_found['part_num'])
                )

        return Distr(self.partnum_found, self.q)


class Distr():
    def __init__(self, partnum_found, q=''):
        self.partnum_found = partnum_found
        self.q = q
        self.dist_found = []
        self.dist_found_min_unit_price = []
        self.distnames_found = []
                      
    def find_dist(self):
        self.dist_found.append(pd.DataFrame(
                list(self.distdb.find(
                    {'part_num':
                    {'$in': self.partnum_found}},
                    {'_id': False,
                     'partnum_ngram3': False}
                ))
            ))
                    
        # Try to find ngram3 of the query to account for possible part numbers        
        for q_token in self.q.split(' '):
            q_ngram3 = get_ngrams(self, q_token)
            self.dist_found.append(pd.DataFrame(
                    list(self.distdb.find({'partnum_ngram3': {'$all': q_ngram3}},
                    {'_id': False, 'partnum_ngram3': False}))
                    )
                )
        
        try:
            self.dist_found = pd.concat(self.dist_found) # self.dist_found becomes DataFrame
            self.dist_found.drop_duplicates(inplace=True)
        
        # if len(self.dist_found.index):
            self.dist_found['nunit_price'] = self.dist_found['unit_price'].apply(
                    lambda _: _ if isinstance(_, float) else 0
                )
            # The following two lines sort by 'part_num' and 'unit_price' so the
            # drop_duplicates() method will keep only the minimum 'unit_price' entry
            # This is for hovering plot to show only minimum entry
            self.dist_found = self.dist_found.sort_values(
                    by=['part_num', 'unit_price']
                )
            self.dist_found_min_unit_price = self.dist_found.drop_duplicates(
                    subset='part_num').copy(deep=True)
            self.dist_found_min_unit_price['hunit_price'] = \
                    self.dist_found_min_unit_price['unit_price'].apply(
                        lambda _: '$%.2f' % _ if isinstance(_, float) else _    
                    )
            self.distnames_found = list(self.dist_found['dist'].drop_duplicates())
        except ValueError: # Catching and passing when self.dist_found has an empty DataFrame
            pass
            
            
class FindCommonProp():
    def __init__(self, partnum_found):
        self.partnum_found = partnum_found
        self.all_matches = dict()
    
    def similarity_score(self, term1, term2):
            term1 = set(term1)
            term2 = set(term2)
            term_inters = term1 & term2
            return (len(term_inters)/len(term1))*(len(term_inters)/len(term2))
            
    def findcommon_properties(self):
        if self.partnum_found:
            commonprop_parts = list(
                    self.partdb.find({'part_num':
                    {'$in': self.partnum_found},
                    # 'manufac': part_found[1],
                    # 'param': {'$ne': ''},
                    'unit': {'$ne': ''},
                    # 'term': {'$ne': []},
                    'from': {'$exists': True},
                    'to': {'$exists': True}},
                    {'_id': False}).limit(400)
                )
            self.part_properties = pd.DataFrame(commonprop_parts)
            
            # Find all params of the parts previously found by simple_query()
            self.part_properties['match'] = True 
            self.all_matched = []
            for idx1, part_num1, words1, unit1, match1 in zip(
                    self.part_properties.index,
                    self.part_properties['part_num'],
                    self.part_properties['word'],
                    self.part_properties['unit'],
                    self.part_properties['match']
                ):
                prop_matches = []
                for idx2, part_num2, words2, unit2, match2 in zip(
                            self.part_properties.index,
                            self.part_properties['part_num'],
                            self.part_properties['word'],
                            self.part_properties['unit'],
                            self.part_properties['match']
                        ):
                    if all([
                            unit1 == unit2, part_num1 != part_num2, match1,
                            match2, self.similarity_score(words1, words2) >= cfg.SIMILAR_SCORE
                        ]):
                        self.part_properties.set_value(idx2, 'match', False)
                        prop_matches.append(self.part_properties.loc[idx2].to_dict())
                    '''    
                    if unit1 == unit2 and part_num1 != part_num2 and match1 and \
                        match2 and self.similarity_score(words1, words2) >= 0.4:
                            self.part_properties.set_value(idx2, 'match', False)
                            prop_matches.append(
                                self.part_properties.loc[idx2].to_dict()
                            )
                    '''
                if prop_matches:
                    self.part_properties.set_value(idx1, 'match', False)
                    prop_matches.append(self.part_properties.loc[idx1].to_dict())
                    
                    # Find representative term for parts with common properties
                    max_len = 0
                    for part in prop_matches:
                        for term in part['term']:
                            if len(term) > max_len:
                                max_len = len(term)
                                repr_term = term
                    self.all_matches[repr_term] = prop_matches

    
if __name__ == '__main__':
    # query = QueryFinder('Gate voltage 1v to 2.5 V leakge current >5A ABA-340F-R31-DC')
    # query = QueryFinder('rated voltage 6V.DC and impedance ratio 3 and case size 7mm')
    # query = QueryFinder('ripple current > 65 mA')
    # query = QueryFinder('drain source voltage > 20 V and junction temperature > 120 C and drain current >1.5A ')
    # query = QueryFinder('AFT05MS004NT1')
    # query = QueryFinder('drain source voltage', conn)
    
    # conn = MongoDb()
    # parts = QueryFinder('drain source voltage', conn).simple_query()
    # dist = parts.process_parts()
    # dist.find_dist()
    # parts.findcommon_properties(parts.partnum_found)
    
    # setup_db is a classmethod to enable inheritance among classes
    # of db_conn.MongoDb

    all_dist = []
    all_parts = []
    # query = QueryHandler('drain source voltage and current drain BLP8G10S-27')
    query = QueryHandler('maximum voltage')
    # parts = [_ for _ in query.run_query()]
    
    for parts in query.run_query():
        all_parts.append(parts)
        all_dist.append(parts.process_parts())
        # all_dist.append(dist.find_dist())
    
   
    

    
    