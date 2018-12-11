from collections import defaultdict
from .. import mycat_tree as mt

cat_tree = defaultdict(dict)

myrootcat = 'Interconnects'
mycat = 'Cables and wires'
mysubcat = mt.mytree[myrootcat][mycat]

subcats = ['Coaxial Cables (RF)',
           'Fiber Optic Cables',
           'Flat Flex Cables (FFC, FPC)',
           'Flat Ribbon Cables',
           'Modular - Flat Cable',
           'Multiple Conductor Cables',
           'Single Conductor Cables (Hook-Up Wire)',
           'Wire Wrap']
mysub_idx = [0, 1, 2, 3, 4, 5, 6, 7]
for idx, subcat in zip(mysub_idx, subcats):
    cat_tree['Cables Wires'][subcat] = {'myrootcat': myrootcat, 'mycat': mycat, 'mysubcat': mysubcat[idx]}

myrootcat = 'Passive devices'
mycat = 'Capacitors'
mysubcat = mt.mytree[myrootcat][mycat]

subcats = ['Accessories',
           'Aluminum - Polymer Capacitors',
           'Aluminum Capacitors',
           'Capacitor Networks Arrays',
           'Ceramic Capacitors',
           'Electric Double Layer Capacitors EDLC Supercapacitors',
           'Film Capacitors',
           'Mica and PTFE Capacitors',
           'Niobium Oxide Capacitors',
           'Silicon Capacitors',
           'Tantalum - Polymer Capacitors',
           'Tantalum Capacitors',
           'Thin Film Capacitors',
           'Trimmers Variable Capacitors',
           'Aluminum Electrolytic Capacitors']
mysub_idx = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
for idx, subcat in zip(mysub_idx, subcats):
    cat_tree['Capacitors'][subcat] = {'myrootcat': myrootcat, 'mycat': mycat, 'mysubcat': mysubcat[idx]}

myrootcat = 'Reliability'
mycat = 'Circuit protection'
mysubcat = mt.mytree[myrootcat][mycat]

subcats = ['Accessories',
           'Circuit Breakers',
           'Disconnect Switch Components',
           'Electrical Specialty Fuses',
           'Fuseholders',
           'Fuses',
           'Gas Discharge Tube Arresters (GDT)',
           'Ground Fault Circuit Interrupter (GFCI)',
           'Inrush Current Limiters (ICL)',
           'Lighting Protection',
           'PTC Resettable Fuses',
           'Surge Suppression ICs',
           'Thermal Cutoffs, Cutouts (TCO)',
           'TVS - Diodes',
           'TVS - Mixed Technology',
           'TVS - Thyristors',
           'TVS - Varistors, MOVs']
mysub_idx = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
for idx, subcat in zip(mysub_idx, subcats):
    cat_tree['Circuit Protection'][subcat] = {'myrootcat': myrootcat, 'mycat': mycat, 'mysubcat': mysubcat[idx]}

myrootcat = 'Passive devices'
mycat = 'Crystals, oscillators, and resonators'
mysubcat = mt.mytree[myrootcat][mycat]

subcats = ['Crystals',
           'Oscillators',
           'Pin Configurable-Selectable Oscillators',
           'Programmable Oscillators',
           'Resonators',
           'Sockets and Insulators',
           'Stand Alone Programmers',
           'VCOs (Voltage Controlled Oscillators)']
mysub_idx = [0, 1, 2, 3, 4, 5, 6, 7]
for idx, subcat in zip(mysub_idx, subcats):
    cat_tree['Crystals Oscillators Resonators'][subcat] = {'myrootcat': myrootcat, 'mycat': mycat, 'mysubcat': mysubcat[idx]}

myrootcat = 'Active devices'
mycat = 'Discrete'
mysubcat = mt.mytree[myrootcat][mycat]

subcats = ['Diodes - Bridge Rectifiers',
           'Diodes - Rectifiers - Arrays',
           'Diodes - Rectifiers - Single',
           'Diodes - RF',
           'Diodes - Variable Capacitance (Varicaps, Varactors)',
           'Diodes - Zener - Arrays',
           'Diodes - Zener - Single',
           'Power Driver Modules',
           'Thyristors - DIACs, SIDACs',
           'Thyristors - SCRs',
           'Thyristors - SCRs - Modules',
           'Thyristors - TRIACs',
           'Transistors - Bipolar (BJT) - Arrays',
           'Transistors - Bipolar (BJT) - Arrays, Pre-Biased',
           'Transistors - Bipolar (BJT) - RF',
           'Transistors - Bipolar (BJT) - Single',
           'Transistors - Bipolar (BJT) - Single, Pre-Biased',
           'Transistors - FETs, MOSFETs - Arrays',
           'Transistors - FETs, MOSFETs - RF',
           'Transistors - FETs, MOSFETs - Single',
           'Transistors - IGBTs - Arrays',
           'Transistors - IGBTs - Modules',
           'Transistors - IGBTs - Single',
           'Transistors - JFETs',
           'Transistors - Programmable Unijunction',
           'Transistors - Special Purpose']
mysub_idx = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
             18, 19, 20, 21, 22, 23, 24]
for idx, subcat in zip(mysub_idx, subcats):
    cat_tree['Discrete Semiconductor Products'][subcat] = {'myrootcat': myrootcat, 'mycat': mycat, 'mysubcat': mysubcat[idx]}
  
myrootcat = 'Thermals'
mycat = 'Thermal management'
mysubcat = mt.mytree[myrootcat][mycat]

subcats = ['AC Fans',
           'DC Fans',
           'Fans - Accessories',
           'Fans - Finger Guards, Filters and Sleeves',
           'Thermal - Accessories',
           'Thermal - Adhesives, Epoxies, Greases, Pastes',
           'Thermal - Heat Sinks',
           'Thermal - Liquid Cooling',
           'Thermal - Pads, Sheets',
           'Thermal - Thermoelectric, Peltier Assemblies',
           'Thermal - Thermoelectric, Peltier Modules']
mysub_idx = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
for idx, subcat in zip(mysub_idx, subcats):
    cat_tree['Fans Thermal Management'][subcat] = {'myrootcat': myrootcat, 'mycat': mycat, 'mysubcat': mysubcat[idx]}

myrootcat = 'Passive devices'
mycat = 'Filters'
mysubcat = mt.mytree[myrootcat][mycat]

subcats = ['Accessories',
           'Ceramic Filters',
           'Common Mode Chokes',
           'DSL Filters',
           'EMI-RFI Filters (LC, RC Networks)',
           'Feed Through Capacitors',
           'Ferrite Beads and Chips',
           'Ferrite Cores - Cables and Wiring',
           'Ferrite Disks and Plates',
           'Helical Filters',
           'Monolithic Crystals',
           'Power Line Filter Modules',
           'RF Filters',
           'SAW Filters']
mysub_idx = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
for idx, subcat in zip(mysub_idx, subcats):
    cat_tree['Filters'][subcat] = {'myrootcat': myrootcat, 'mycat': mycat, 'mysubcat': mysubcat[idx]}

myrootcat = 'Passive devices'
mycat = 'Inductors and coils'
mysubcat = mt.mytree[myrootcat][mycat]

subcats = ['Adjustable Inductors',
           'Arrays Signal Transformers',
           'Delay Lines',
           'Fixed Inductors',
           'Wireless Charging Coils']
mysub_idx = [0, 1, 2, 3, 4]
for idx, subcat in zip(mysub_idx, subcats):
    cat_tree['Inductors Coils Chokes'][subcat] = {'myrootcat': myrootcat, 'mycat': mycat, 'mysubcat': mysubcat[idx]}

# -----------------------------------------------------------------------------
myrootcat = 'Integrated circuits (IC)'
mycat = 'Audio IC'
mysubcat = mt.mytree[myrootcat][mycat]

subcats = ['Audio Special Purpose']
mysub_idx = [0]
for idx, subcat in zip(mysub_idx, subcats):
    cat_tree['Integrated Circuits (ICs)'][subcat] = {'myrootcat': myrootcat, 'mycat': mycat, 'mysubcat': mysubcat[idx]}

mycat = 'Clock and time'
mysubcat = mt.mytree[myrootcat][mycat]

subcats = ['Clock-Timing - Application Specific',
           'Clock-Timing - Clock Buffers, Drivers',
           'Clock-Timing - Clock Generators, PLLs, Frequency Synthesizers',
           'Clock-Timing - Delay Lines',
           'Clock-Timing - IC Batteries',
           'Clock-Timing - Programmable Timers and Oscillators',
           'Clock-Timing - Real Time Clocks']
mysub_idx = [0, 1, 2, 3, 4, 5, 6]
for idx, subcat in zip(mysub_idx, subcats):
    cat_tree['Integrated Circuits (ICs)'][subcat] = {'myrootcat': myrootcat, 'mycat': mycat, 'mysubcat': mysubcat[idx]}
    
mycat = 'Data acquisition'
mysubcat = mt.mytree[myrootcat][mycat]

subcats = ['Data Acquisition - ADCs-DACs - Special Purpose',
           'Data Acquisition - Analog Front End (AFE)',
           'Data Acquisition - Analog to Digital Converters (ADC)',
           'Data Acquisition - Digital Potentiometers',
           'Data Acquisition - Digital to Analog Converters (DAC)',
           'Data Acquisition - Touch Screen Controllers']
mysub_idx = [0, 1, 2, 3, 4, 5]
for idx, subcat in zip(mysub_idx, subcats):
    cat_tree['Integrated Circuits (ICs)'][subcat] = {'myrootcat': myrootcat, 'mycat': mycat, 'mysubcat': mysubcat[idx]}
    
mycat = 'Embedded'
mysubcat = mt.mytree[myrootcat][mycat]

subcats = ['Embedded - CPLDs (Complex Programmable Logic Devices)',
           'Embedded - DSP (Digital Signal Processors)',
           'Embedded - FPGAs (Field Programmable Gate Array)',
           'Embedded - FPGAs (Field Programmable Gate Array) with Microcontrollers',
           'Embedded - Microcontroller or Microprocessor Modules',
           'Embedded - Microcontrollers',
           'Embedded - Microcontrollers - Application Specific',
           'Embedded - Microprocessors',
           'Embedded - PLDs (Programmable Logic Device)',
           'Embedded - System On Chip (SoC)']
mysub_idx = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
for idx, subcat in zip(mysub_idx, subcats):
    cat_tree['Integrated Circuits (ICs)'][subcat] = {'myrootcat': myrootcat, 'mycat': mycat, 'mysubcat': mysubcat[idx]}

mycat = 'Signal interfaces'
mysubcat = mt.mytree[myrootcat][mycat]

subcats = ['Interface - Analog Switches - Special Purpose',
           'Interface - Analog Switches, Multiplexers, Demultiplexers',
           'Interface - CODECs',
           'Interface - Controllers',
           'Interface - Direct Digital Synthesis (DDS)',
           'Interface - Drivers, Receivers, Transceivers',
           'Interface - Encoders, Decoders, Converters',
           'Interface - Filters - Active',
           'Interface - I-O Expanders',
           'Interface - Modems - ICs and Modules',
           'Interface - Modules',
           'Interface - Sensor and Detector Interfaces',
           'Interface - Serializers, Deserializers',
           'Interface - Signal Buffers, Repeaters, Splitters',
           'Interface - Signal Terminators',
           'Interface - Specialized',
           'Interface - Telecom',
           'Interface - UARTs (Universal Asynchronous Receiver Transmitter)',
           'Interface - Voice Record and Playback']
mysub_idx = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
for idx, subcat in zip(mysub_idx, subcats):
    cat_tree['Integrated Circuits (ICs)'][subcat] = {'myrootcat': myrootcat, 'mycat': mycat, 'mysubcat': mysubcat[idx]}
    
mycat = 'Linear amplifiers'
mysubcat = mt.mytree[myrootcat][mycat]

subcats = ['Linear - Amplifiers - Audio',
           'Linear - Amplifiers - Instrumentation, OP Amps, Buffer Amps',
           'Linear - Amplifiers - Special Purpose',
           'Linear - Amplifiers - Video Amps and Modules',
           'Linear - Analog Multipliers, Dividers',
           'Linear - Comparators',
           'Linear - Video Processing']
mysub_idx = [0, 1, 2, 3, 4, 5, 6]
for idx, subcat in zip(mysub_idx, subcats):
    cat_tree['Integrated Circuits (ICs)'][subcat] = {'myrootcat': myrootcat, 'mycat': mycat, 'mysubcat': mysubcat[idx]}
    
mycat = 'Digital logic'
mysubcat = mt.mytree[myrootcat][mycat]

subcats = ['Logic - Buffers, Drivers, Receivers, Transceivers',
           'Logic - Comparators',
           'Logic - Counters, Dividers',
           'Logic - FIFOs Memory',
           'Logic - Flip Flops',
           'Logic - Gates and Inverters',
           'Logic - Gates and Inverters - Multi-Function, Configurable',
           'Logic - Latches',
           'Logic - Multivibrators',
           'Logic - Parity Generators and Checkers',
           'Logic - Shift Registers',
           'Logic - Signal Switches, Multiplexers, Decoders',
           'Logic - Specialty Logic',
           'Logic - Translators, Level Shifters',
           'Logic - Universal Bus Functions']
mysub_idx = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
for idx, subcat in zip(mysub_idx, subcats):
    cat_tree['Integrated Circuits (ICs)'][subcat] = {'myrootcat': myrootcat, 'mycat': mycat, 'mysubcat': mysubcat[idx]}
    
mycat = 'Memory devices'
mysubcat = mt.mytree[myrootcat][mycat]

subcats = ['Memory',
           'Memory - Batteries',
           'Memory - Configuration Proms for FPGAs',
           'Memory - Controllers']
mysub_idx = [0, 1, 2, 3]
for idx, subcat in zip(mysub_idx, subcats):
    cat_tree['Integrated Circuits (ICs)'][subcat] = {'myrootcat': myrootcat, 'mycat': mycat, 'mysubcat': mysubcat[idx]}
    
mycat = 'Power management ICs (PMIC)'
mysubcat = mt.mytree[myrootcat][mycat]

subcats = ['PMIC - AC DC Converters, Offline Switchers',
           'PMIC - Battery Chargers',
           'PMIC - Battery Management',
           'PMIC - Current Regulation-Management',
           'PMIC - Display Drivers',
           'PMIC - Energy Metering',
           'PMIC - Full, Half-Bridge Drivers',
           'PMIC - Gate Drivers',
           'PMIC - Hot Swap Controllers',
           'PMIC - Laser Drivers',
           'PMIC - LED Drivers',
           'PMIC - Lighting, Ballast Controllers',
           'PMIC - Motor Drivers, Controllers',
           'PMIC - OR Controllers, Ideal Diodes',
           'PMIC - PFC (Power Factor Correction)',
           'PMIC - Power Distribution Switches, Load Drivers',
           'PMIC - Power Management - Specialized',
           'PMIC - Power Over Ethernet (PoE) Controllers',
           'PMIC - Power Supply Controllers, Monitors',
           'PMIC - RMS to DC Converters',
           'PMIC - Supervisors',
           'PMIC - Thermal Management',
           'PMIC - V-F and F-V Converters',
           'PMIC - Voltage Reference',
           'PMIC - Voltage Regulators - DC DC Switching Controllers',
           'PMIC - Voltage Regulators - DC DC Switching Regulators',
           'PMIC - Voltage Regulators - Linear',
           'PMIC - Voltage Regulators - Linear + Switching',
           'PMIC - Voltage Regulators - Linear Regulator Controllers',
           'PMIC - Voltage Regulators - Special Purpose']
mysub_idx = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
             18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]
for idx, subcat in zip(mysub_idx, subcats):
    cat_tree['Integrated Circuits (ICs)'][subcat] = {'myrootcat': myrootcat, 'mycat': mycat, 'mysubcat': mysubcat[idx]}
    
mycat = 'Special purpose ICs'
mysubcat = mt.mytree[myrootcat][mycat]

subcats = ['Specialized ICs']
mysub_idx = [0]
for idx, subcat in zip(mysub_idx, subcats):
    cat_tree['Integrated Circuits (ICs)'][subcat] = {'myrootcat': myrootcat, 'mycat': mycat, 'mysubcat': mysubcat[idx]}    
# -----------------------------------------------------------------------------

myrootcat = 'Active devices'
mycat = 'Isolators'
mysubcat = mt.mytree[myrootcat][mycat]

subcats = ['Digital Isolators',
           'Isolators - Gate Drivers',
           'Optoisolators - Logic Output',
           'Optoisolators - Transistor, Photovoltaic Output',
           'Optoisolators - Triac, SCR Output',
           'Special Purpose']
mysub_idx = [0, 1, 2, 3, 4, 5]
for idx, subcat in zip(mysub_idx, subcats):
    cat_tree['Isolators'][subcat] = {'myrootcat': myrootcat, 'mycat': mycat, 'mysubcat': mysubcat[idx]}

myrootcat = 'Magnetics'
mycat = 'Transformer and inductor components'
mysubcat = mt.mytree[myrootcat][mycat]

subcats = ['Bobbins (Coil Formers), Mounts, Hardware',
           'Ferrite Cores',
           'Magnetic Wire']
mysub_idx = [0, 1, 2]
for idx, subcat in zip(mysub_idx, subcats):
    cat_tree['Magnetics - Transformer, Inductor Components'][subcat] = {'myrootcat': myrootcat, 'mycat': mycat, 'mysubcat': mysubcat[idx]}

myrootcat = 'Electromechanical'
mycat = 'Motors and drivers'
mysubcat = mt.mytree[myrootcat][mycat]

subcats = ['Accessories',
           'Motor Driver Boards, Modules',
           'Motors - AC DC',
           'Solenoids Actuators',
           'Stepper Motors']
mysub_idx = [0, 1, 2, 3, 4]
for idx, subcat in zip(mysub_idx, subcats):
    cat_tree['Motors Solenoids Driver Boards-Modules'][subcat] = {'myrootcat': myrootcat, 'mycat': mycat, 'mysubcat': mysubcat[idx]}

myrootcat = 'Passive devices'
mycat = 'Potentiometers and variable resistors'
mysubcat = mt.mytree[myrootcat][mycat]

subcats = ['Accessories',
           'Adjustable Power Resistor',
           'Joystick Potentiometers',
           'Rotary Potentiometers, Rheostats',
           'Scale Dials',
           'Slide Potentiometers',
           'Thumbwheel Potentiometers',
           'Trimmer Potentiometers',
           'Value Display Potentiometers']
mysub_idx = [0, 1, 2, 3, 4, 5, 6, 7, 8]
for idx, subcat in zip(mysub_idx, subcats):
    cat_tree['Potentiometers Variable Resistors'][subcat] = {'myrootcat': myrootcat, 'mycat': mycat, 'mysubcat': mysubcat[idx]}

myrootcat = 'Power supplies'
mycat = 'On-Board'
mysubcat = mt.mytree[myrootcat][mycat]

subcats = ['AC DC Converters',
           'Accessories',
           'DC DC Converters',
           'LED Drivers']
mysub_idx = [0, 1, 2, 3]
for idx, subcat in zip(mysub_idx, subcats):
    cat_tree['Power Supplies - Board Mount'][subcat] = {'myrootcat': myrootcat, 'mycat': mycat, 'mysubcat': mysubcat[idx]}

myrootcat = 'Power supplies'
mycat = 'Off-board'
mysubcat = mt.mytree[myrootcat][mycat]

subcats = ['AC AC Wall Adapters',
           'AC DC Configurable Power Supplies (Factory Assembled)',
           'AC DC Configurable Power Supply Chassis',
           'AC DC Configurable Power Supply Modules',
           'AC DC Converters',
           'AC DC Desktop, Wall Adapters',
           'Accessories',
           'DC DC Converters',
           'LED Drivers',
           'Power over Ethernet (PoE)']
mysub_idx = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
for idx, subcat in zip(mysub_idx, subcats):
    cat_tree['Power Supplies - External-Internal (Off-Board)'][subcat] = {'myrootcat': myrootcat, 'mycat': mycat, 'mysubcat': mysubcat[idx]}

myrootcat = 'Electromechanical'
mycat = 'Relays'
mysubcat = mt.mytree[myrootcat][mycat]

subcats = ['Accessories',
           'I-O Relay Module Racks',
           'I-O Relay Modules - Analog',
           'I-O Relay Modules - Input',
           'I-O Relay Modules - Output',
           'Power Relays, Over 2 Amps',
           'Relay Sockets',
           'Signal Relays, Up to 2 Amps',
           'Solid State Relays']
mysub_idx = [0, 1, 2, 3, 4, 5, 6, 7, 8]
for idx, subcat in zip(mysub_idx, subcats):
    cat_tree['Relays'][subcat] = {'myrootcat': myrootcat, 'mycat': mycat, 'mysubcat': mysubcat[idx]}

myrootcat = 'Passive devices'
mycat = 'Resistors'
mysubcat = mt.mytree[myrootcat][mycat]

subcats = ['Accessories',
           'Chassis Mount Resistors',
           'Chip Resistor - Surface Mount',
           'Precision Trimmed Resistors',
           'Resistor Networks Arrays',
           'Specialized Resistors',
           'Through Hole Resistors']
mysub_idx = [0, 1, 2, 3, 4, 5, 6]
for idx, subcat in zip(mysub_idx, subcats):
    cat_tree['Resistors'][subcat] = {'myrootcat': myrootcat, 'mycat': mycat, 'mysubcat': mysubcat[idx]}
    
myrootcat = 'Active devices'
mycat = 'Radio Fequency (RF)'
mysubcat = mt.mytree[myrootcat][mycat]

subcats = ['Attenuators',
           'Balun',
           'RF Accessories',
           'RF Amplifiers',
           'RF Antennas',
           'RF Demodulators',
           'RF Detectors',
           'RF Diplexers',
           'RF Directional Coupler',
           'RF Evaluation and Development Kits, Boards',
           'RF Front End (LNA + PA)',
           'RF Misc ICs and Modules',
           'RF Mixers',
           'RF Modulators',
           'RF Power Controller ICs',
           'RF Power Dividers-Splitters',
           'RF Receiver, Transmitter, and Transceiver Finished Units',
           'RF Receivers',
           'RF Shields',
           'RF Switches',
           'RF Transceiver ICs',
           'RF Transceiver Modules',
           'RF Transmitters',
           'RFI and EMI - Contacts, Fingerstock and Gaskets',
           'RFI and EMI - Shielding and Absorbing Materials',
           'RFID Accessories',
           'RFID Antennas',
           'RFID Evaluation and Development Kits, Boards',
           'RFID Reader Modules',
           'RFID Transponders, Tags',
           'RFID RF Access Monitoring ICs']
mysub_idx = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
             18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
for idx, subcat in zip(mysub_idx, subcats):
    cat_tree['RF-IF and RFID'][subcat] = {'myrootcat': myrootcat, 'mycat': mycat, 'mysubcat': mysubcat[idx]}

# -----------------------------------------------------------------------------
myrootcat = 'Sensors and transducers'
mycat = 'Specialized sensors'
mysubcat = mt.mytree[myrootcat][mycat]

subcats = ['Accessories',
           'Amplifiers',
           'Capacitive Touch Sensors, Proximity Sensor ICs',
           'Color Sensors',
           'Current Transducers',
           'Dust Sensors',
           'Encoders',
           'Flex Sensors',
           'Float Level Sensors',
           'Flow Sensors',
           'Force Sensors',
           'Gas Sensors',
           'Humidity Moisture Sensors',
           'Image Sensors Camera',
           'IrDA Transceiver Modules',
           'LVDT Transducers (Linear Variable Differential Transformer)',
           'Multifunction',
           'Pressure Sensors, Transducers',
           'Solar Cells',
           'Specialized Sensors',
           'Strain Gauges',
           'Ultrasonic Receivers, Transmitters']
mysub_idx = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
             18, 19, 20, 21]
for idx, subcat in zip(mysub_idx, subcats):
    cat_tree['Sensors Transducers'][subcat] = {'myrootcat': myrootcat, 'mycat': mycat, 'mysubcat': mysubcat[idx]}

mycat = 'Magnetic'
mysubcat = mt.mytree[myrootcat][mycat]

subcats = ['Magnetic Sensors - Compass, Magnetic Field (Modules)',
           'Magnetic Sensors - Linear, Compass (ICs)',
           'Magnetic Sensors - Position, Proximity, Speed (Modules)',
           'Magnetic Sensors - Switches (Solid State)',
           'Magnets - Multi Purpose',
           'Magnets - Sensor Matched']
mysub_idx = [0, 1, 2, 3, 4, 5]
for idx, subcat in zip(mysub_idx, subcats):
    cat_tree['Sensors Transducers'][subcat] = {'myrootcat': myrootcat, 'mycat': mycat, 'mysubcat': mysubcat[idx]}
    
mycat = 'Motion'
mysubcat = mt.mytree[myrootcat][mycat]

subcats = ['Motion Sensors - Accelerometers',
           'Motion Sensors - Gyroscopes',
           'Motion Sensors - IMUs (Inertial Measurement Units)',
           'Motion Sensors - Inclinometers',
           'Motion Sensors - Optical',
           'Motion Sensors - Tilt Switches',
           'Motion Sensors - Vibration']
mysub_idx = [0, 1, 2, 3, 4, 5, 6]
for idx, subcat in zip(mysub_idx, subcats):
    cat_tree['Sensors Transducers'][subcat] = {'myrootcat': myrootcat, 'mycat': mycat, 'mysubcat': mysubcat[idx]}
    
mycat = 'Optical'
mysubcat = mt.mytree[myrootcat][mycat]

subcats = ['Optical Sensors - Ambient Light, IR, UV Sensors',
           'Optical Sensors - Distance Measuring',
           'Optical Sensors - Mouse',
           'Optical Sensors - Photo Detectors - CdS Cells',
           'Optical Sensors - Photo Detectors - Logic Output',
           'Optical Sensors - Photo Detectors - Remote Receiver',
           'Optical Sensors - Photodiodes',
           'Optical Sensors - Photoelectric, Industrial',
           'Optical Sensors - Photointerrupters - Slot Type - Logic Output',
           'Optical Sensors - Photointerrupters - Slot Type - Transistor Output',
           'Optical Sensors - Phototransistors',
           'Optical Sensors - Reflective - Analog Output',
           'Optical Sensors - Reflective - Logic Output']
mysub_idx = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
for idx, subcat in zip(mysub_idx, subcats):
    cat_tree['Sensors Transducers'][subcat] = {'myrootcat': myrootcat, 'mycat': mycat, 'mysubcat': mysubcat[idx]}
    
mycat = 'Position and proximity'
mysubcat = mt.mytree[myrootcat][mycat]

subcats = ['Position Sensors - Angle, Linear Position Measuring',
           'Proximity Sensors',
           'Proximity-Occupancy Sensors - Finished Units']
mysub_idx = [0, 1, 2]
for idx, subcat in zip(mysub_idx, subcats):
    cat_tree['Sensors Transducers'][subcat] = {'myrootcat': myrootcat, 'mycat': mycat, 'mysubcat': mysubcat[idx]}
    
mycat = 'Sensor cables and interfaces'
mysubcat = mt.mytree[myrootcat][mycat]

subcats = ['Sensor Cable - Accessories',
           'Sensor Cable - Assemblies',
           'Sensor Interface - Junction Blocks']
mysub_idx = [0, 1, 2]
for idx, subcat in zip(mysub_idx, subcats):
    cat_tree['Sensors Transducers'][subcat] = {'myrootcat': myrootcat, 'mycat': mycat, 'mysubcat': mysubcat[idx]}
    
mycat = 'Temperature'
mysubcat = mt.mytree[myrootcat][mycat]

subcats = ['Temperature Sensors - Analog and Digital Output',
           'Temperature Sensors - NTC Thermistors',
           'Temperature Sensors - PTC Thermistors',
           'Temperature Sensors - RTD (Resistance Temperature Detector)',
           'Temperature Sensors - Thermocouple, Temperature Probes',
           'Temperature Sensors - Thermostats - Mechanical',
           'Temperature Sensors - Thermostats - Solid State']
mysub_idx = [0, 1, 2, 3, 4, 5, 6]
for idx, subcat in zip(mysub_idx, subcats):
    cat_tree['Sensors Transducers'][subcat] = {'myrootcat': myrootcat, 'mycat': mycat, 'mysubcat': mysubcat[idx]}
# -----------------------------------------------------------------------------

myrootcat = 'Magnetics'
mycat = 'Transformer and inductor components'
mysubcat = mt.mytree[myrootcat][mycat]

subcats = ['Accessories',
           'Audio Transformers',
           'Current Sense Transformers',
           'Isolated Non-Isolated Autotransformer - Step Up Step Down',
           'Power Transformers',
           'Pulse Transformers',
           'Specialty Transformers',
           'Switching Converter, SMPS Transformers']
mysub_idx = [3, 4, 5, 6, 7, 8, 9, 10]
for idx, subcat in zip(mysub_idx, subcats):
    cat_tree['Transformers'][subcat] = {'myrootcat': myrootcat, 'mycat': mycat, 'mysubcat': mysubcat[idx]}
    