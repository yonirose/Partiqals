# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 09:15:39 2016

@author: jrosenfe
"""
                             
import time
from operator import itemgetter
import db_setup as db

def print_prog(name, cnt, tot, bar_length=40, char_comp='#', char_incomp='_',
               left_just=50, time_sig=False, endwith='\n'):
    def prog_bar(perc, bar_length, char_comp, char_incomp):
        comp = int(round(perc*bar_length))
        incomp = bar_length-comp
        return '|'+char_comp*comp+char_incomp*incomp+'|'
    print('%s: %s %s %.2f%%' % (name.ljust(left_just),
        (str(cnt)+'/'+str(tot)).ljust(15),
        prog_bar(cnt/tot, bar_length, char_comp, char_incomp).ljust(5),
                 cnt/tot*100), end=endwith)
    if time_sig:
        print(time.strftime('%m/%d/%Y'), time.strftime('%H:%M:%S'))

def scrapy_prog():
    grand_totals = list(db.cursordb.aggregate(
            [{'$group': {'_id': '', 'current_count': {'$sum': '$current_count'},
                         'total_count': {'$sum': '$total_count'}}}]
        ))[0]
    print_prog('Total progress', grand_totals['current_count'],
                grand_totals['total_count'], time_sig=True)
    
    dist_totals = list(db.cursordb.aggregate(
            [{'$group': {'_id': '$dist',
                         'current_count': {'$sum': '$current_count'},
                         'total_count': {'$sum': '$total_count'}}}]
        ))
    for dist_total in dist_totals:
        print('\n')
        print_prog(dist_total['_id'].upper(), dist_total['current_count'],
                   dist_total['total_count'])
    
        all_cats = list(db.cursordb.find())
        all_cats = sorted(all_cats, key=itemgetter('dist', 'ucat'))
        for cats in all_cats:
            print_prog('%s > %s' % (cats['ucat'].split('__')[0],
                                    cats['ucat'].split('__')[1]),
                        cats['current_count'], cats['total_count'],
                )

def analyze_pdf_prog():
    remain_pdf = db.metadb.find({'processed': 'pending'}).count()
    proc_pdf = db.metadb.find({'processed': 'done'}).count()
    inprog_pdf = db.metadb.find({'processed': 'inprogress'}).count()
    err_pdf = db.metadb.find({'processed': 'error'}).count()
    tot_pdf = remain_pdf + proc_pdf + inprog_pdf + err_pdf
    
    try:
        print_prog('Processed', proc_pdf, tot_pdf, bar_length=10, left_just=5, endwith='')
        print_prog(' > Pending', remain_pdf, tot_pdf, bar_length=10, left_just=5, endwith='')
        # print_prog(' > In progress', inprog_pdf, tot_pdf, bar_length=1, left_just=5, endwith='')
        print_prog(' > Error', err_pdf, tot_pdf, bar_length=10, left_just=5, endwith='\r')
    except ZeroDivisionError:
        print('Zero PDFs in the database')