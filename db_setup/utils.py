# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 09:15:39 2016

@author: jrosenfe
"""
from bson.objectid import ObjectId
from pymongo import IndexModel, ASCENDING

import db_setup as db

def reset_scrapy_counts(really=False):
    if really:
        for cat in db.cursordb.find():
            db.cursordb.update_one(
                    {'_id': ObjectId(cat['_id'])},
                    {'$set': {'current_count': 0,
                              'scan_complete': False,
                              'current_link': cat['start_link']}}
                )
    else:
        print('You really did not mean it, did you?')

def reset_pdf_stats(really=False, filt='all'):
    '''
    filt can take one of the following values:
    'all', 'inprogress', 'error', 'done'
    '''
    if really:
        if filt == 'all':
            db.distdb.update_many({},
                                  {'$set': {'processed': 'pending', 'page': 0}})
        else:
            db.distdb.update_many({'processed': filt},
                                  {'$set': {'processed': 'pending', 'page': 0}})
    else:
       print('You really did not mean it, did you?') 
        
def generate_indexes():
    partdb_indexes = [
            IndexModel([('from', ASCENDING),
                        ('to', ASCENDING), ('unit', ASCENDING)]),
            IndexModel([('word', ASCENDING)]),
            IndexModel([('dist_num', ASCENDING), ('col', ASCENDING)]),
            IndexModel([('part_num', ASCENDING), ('page_num', ASCENDING)])
        ]
    db.partdb.create_indexes(partdb_indexes)
    
    distdb_indexes = [
            IndexModel([('root_cat', ASCENDING), ('cat', ASCENDING),
                        ('subcat', ASCENDING)]),
            IndexModel([('partnum_manufac_ngram3', ASCENDING)]),
            IndexModel([('part_num', ASCENDING), ('manufac', ASCENDING)])
        ]
    db.distdb.create_indexes(distdb_indexes)
    
    manufacdb_indexes = [IndexModel([('manufac_ngram3', ASCENDING)])]
    db.manufacdb.create_indexes(manufacdb_indexes)
    
    invenb_indexes = [IndexModel([('ucat', ASCENDING), ('dist', ASCENDING)])]
    db.invendb.create_indexes(invenb_indexes)

