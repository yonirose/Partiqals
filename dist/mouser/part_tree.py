from collections import defaultdict
import dist.mycat_tree as mt

cat_tree = defaultdict(dict)
myrootcat = 'Active devices'
mycat = 'Discrete'
mysubcat = mt.mytree[myrootcat][mycat]

subcats = [
    'PIN Diodes',
]
mysub_idx = [3]
for idx, subcat in zip(mysub_idx, subcats):
    cat_tree['Wireless and RF Semiconductors'][subcat] = {'myrootcat': myrootcat, 'mycat': mycat, 'mysubcat': mysubcat[idx]}

myrootcat = 'Active devices'
mycat = 'Discrete'
mysubcat = mt.mytree[myrootcat][mycat]

subcats = [
    'RF JFET Transistors',
    'RF MOSFET Transistors',
    'RF Bipolar Transistors',
]
mysub_idx = [22, 19, 14]
for idx, subcat in zip(mysub_idx, subcats):
    cat_tree['Transistors RF'][subcat] = {'myrootcat': myrootcat, 'mycat': mycat, 'mysubcat': mysubcat[idx]}

myrootcat = 'Active devices'
mycat = 'Radio Fequency (RF)'
mysubcat = mt.mytree[myrootcat][mycat]

subcats = [
    'RF Amplifier',
    'RF Front End',
    'Prescaler',
    'RF Detector',
    'Tuners',
    'RFID Transponders',
    'RF Wireless Misc',
    'RF Mixer',
    'Modulator - Demodulator',
    'RF System on a Chip - SoC',
    'RF Receiver',
    'RF Transmitter',
    'RF Transceiver',
    'Phase Detectors - Shifters',
    'Up-Down Converters',
    'RF Switch ICs',
    'Attenuators',
]
mysub_idx = [3, 10, 11, 6, 6, 29, 6, 12, 13, 31, 17, 22, 20, 32, 12, 19, 0]
for idx, subcat in zip(mysub_idx, subcats):
    cat_tree['Wireless and RF Integrated Circuits'][subcat] = {'myrootcat': myrootcat, 'mycat': mycat, 'mysubcat': mysubcat[idx]}

myrootcat = 'Integrated circuits (IC)'
mycat = 'Clock and time'
mysubcat = mt.mytree[myrootcat][mycat]

subcats = [
    'Phase Locked Loops - PLL',
]
mysub_idx = [2]
for idx, subcat in zip(mysub_idx, subcats):
    cat_tree['Wireless and RF Integrated Circuits'][subcat] = {'myrootcat': myrootcat, 'mycat': mycat, 'mysubcat': mysubcat[idx]}

myrootcat = 'Integrated circuits (IC)'
mycat = 'Embedded'
mysubcat = mt.mytree[myrootcat][mycat]

subcats = [
    'RF Microcontrollers - MCU'
]
mysub_idx = [5]
for idx, subcat in zip(mysub_idx, subcats):
    cat_tree['Wireless and RF Integrated Circuits'][subcat] = {'myrootcat': myrootcat, 'mycat': mycat, 'mysubcat': mysubcat[idx]}


