import os
import sys
from collections import defaultdict
import mycat_tree as mt
cat_tree = defaultdict(dict)
myrootcat = ''
mycat = ''
mysubcat = mt.mytree[myrootcat][mycat]

subcats = [
    'PIN Diodes',
]
mysub_idx = [ ,]
for idx, subcat in zip(mysub_idx, subcats):
    cat_tree['Wireless and RF Semiconductors'][subcat] = {'myrootcat': myrootcat, 'mycat': mycat, 'mysubcat': mysubcat[idx]}

myrootcat = ''
mycat = ''
mysubcat = mt.mytree[myrootcat][mycat]

subcats = [
    'Prescaler',
    'Tuners',
    'RF Wireless Misc',
    'RF Transmitter',
    'RF Amplifier',
    'RF System on a Chip - SoC',
    'RF Receiver',
    'Up-Down Converters',
    'Phase Detectors - Shifters',
    'RF Mixer',
    'RF Front End',
    'RF Detector',
    'RFID Transponders',
    'Attenuators',
    'Modulator - Demodulator',
    'RF Microcontrollers - MCU',
    'RF Switch ICs',
    'Phase Locked Loops - PLL',
    'RF Transceiver',
]
mysub_idx = [ , , , , , , , , , , , , , , , , , , ,]
for idx, subcat in zip(mysub_idx, subcats):
    cat_tree['Wireless and RF Integrated Circuits'][subcat] = {'myrootcat': myrootcat, 'mycat': mycat, 'mysubcat': mysubcat[idx]}

myrootcat = ''
mycat = ''
mysubcat = mt.mytree[myrootcat][mycat]

subcats = [
    'RF Bipolar Transistors',
    'RF JFET Transistors',
    'RF MOSFET Transistors',
]
mysub_idx = [ , , ,]
for idx, subcat in zip(mysub_idx, subcats):
    cat_tree['Transistors RF'][subcat] = {'myrootcat': myrootcat, 'mycat': mycat, 'mysubcat': mysubcat[idx]}

