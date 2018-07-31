import os
import sys
sys.path.append(os.path.join('..', '..', '..', '..'))
from collections import defaultdict
import mycat_tree as mt
class PartTree():
    cat_tree = defaultdict(dict)
    myrootcat = ''
    mycat = ''
    mysubcat = mt.mytree[myrootcat][mycat]

    subcats = [               'Accessories',
               'Chassis Mount Resistors',
               'Chip Resistor - Surface Mount',
               'Precision Trimmed Resistors',
               'Resistor Networks, Arrays',
               'Specialized Resistors',
               'Through Hole Resistors',
]
    mysub_idx = [ , , , , , ,]
    for idx, subcat in zip(mysub_idx, subcats):
        cat_tree['Resistors'][subcat] = {'myrootcat': myrootcat,                         'mycat': mycat, 'mysubcat': mysubcat[idx]}

