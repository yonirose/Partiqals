# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 09:15:39 2016

@author: jrosenfe
"""

import re
from ngram import NGram

def replace_illchar(s, to_type=str):
    ill_chars = ['/', ',', '(', ')', ':', '&', '>', '<', '$']
    rep_chars = ['-', '', '', '', '-', 'and', '', '', '']
    for ill_char, rep_char in zip(ill_chars, rep_chars):
        s = s.replace(ill_char, rep_char)
    return to_type(s.strip())

def cmp_files(file1, file2, diffresults_file):
    with open(file1, 'r') as f1:
        with open(file2, 'r') as f2:
            diff_lines = list(set(f1) - set(f2))
    with open(diffresults_file, 'w') as f:
        for line in diff_lines:
            f.write(str(line))
            
def get_ngrams(term, n=3):
    term = re.sub(r'[-_.__/\\ ]', '', term.lower())
    return list(NGram(N=n)._split(term))
        
