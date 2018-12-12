import os
import sys
from collections import defaultdict
import mycat_tree as mt
cat_tree = defaultdict(dict)
myrootcat = ''
mycat = ''
mysubcat = mt.mytree[myrootcat][mycat]

subcats = [
    'Specialized Resistors',
    'Resistor Networks Arrays',
    'Chassis Mount Resistors',
    'Through Hole Resistors',
    'Accessories',
    'Chip Resistor - Surface Mount',
]
mysub_idx = [ , , , , , ,]
for idx, subcat in zip(mysub_idx, subcats):
    cat_tree['Resistors'][subcat] = {'myrootcat': myrootcat, 'mycat': mycat, 'mysubcat': mysubcat[idx]}

myrootcat = ''
mycat = ''
mysubcat = mt.mytree[myrootcat][mycat]

subcats = [
    'Accessories',
    'Thin Film Capacitors',
    'Capacitor Networks Arrays',
    'Niobium Oxide Capacitors',
    'Electric Double Layer Capacitors EDLC Supercapacitors',
    'Tantalum - Polymer Capacitors',
    'Ceramic Capacitors',
    'Trimmers Variable Capacitors',
    'Tantalum Capacitors',
    'Silicon Capacitors',
    'Film Capacitors',
    'Aluminum Electrolytic Capacitors',
    'Mica and PTFE Capacitors',
    'Aluminum - Polymer Capacitors',
]
mysub_idx = [ , , , , , , , , , , , , , ,]
for idx, subcat in zip(mysub_idx, subcats):
    cat_tree['Capacitors'][subcat] = {'myrootcat': myrootcat, 'mycat': mycat, 'mysubcat': mysubcat[idx]}

12/11/2018, 15:29:19

import os
import sys
from collections import defaultdict
import mycat_tree as mt
cat_tree = defaultdict(dict)
myrootcat = ''
mycat = ''
mysubcat = mt.mytree[myrootcat][mycat]

subcats = [
    'Chip Resistor - Surface Mount',
    'Resistor Networks Arrays',
    'Through Hole Resistors',
    'Chassis Mount Resistors',
    'Specialized Resistors',
    'Accessories',
]
mysub_idx = [ , , , , , ,]
for idx, subcat in zip(mysub_idx, subcats):
    cat_tree['Resistors'][subcat] = {'myrootcat': myrootcat, 'mycat': mycat, 'mysubcat': mysubcat[idx]}

myrootcat = ''
mycat = ''
mysubcat = mt.mytree[myrootcat][mycat]

subcats = [
    'Capacitor Networks Arrays',
    'Electric Double Layer Capacitors EDLC Supercapacitors',
    'Tantalum - Polymer Capacitors',
    'Niobium Oxide Capacitors',
    'Trimmers Variable Capacitors',
    'Tantalum Capacitors',
    'Mica and PTFE Capacitors',
    'Silicon Capacitors',
    'Aluminum - Polymer Capacitors',
    'Ceramic Capacitors',
    'Film Capacitors',
    'Thin Film Capacitors',
    'Aluminum Electrolytic Capacitors',
    'Accessories',
]
mysub_idx = [ , , , , , , , , , , , , , ,]
for idx, subcat in zip(mysub_idx, subcats):
    cat_tree['Capacitors'][subcat] = {'myrootcat': myrootcat, 'mycat': mycat, 'mysubcat': mysubcat[idx]}

