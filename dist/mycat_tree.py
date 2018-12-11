# -*- coding: utf-8 -*-
"""
Created on Tue May 16 12:53:06 2017

@author: jrosenfe
"""

mytree = {'Interconnects': {'Cables and wires': ['Coaxial', #0
                                                 'Fiber optic', #1
                                                 'Flex', #2
                                                 'Ribbon', #3
                                                 'Modular', #4
                                                 'Multi-conductor', #5
                                                 'Singal conductor', #6
                                                 'Wire wrap']}, #7
          'Passive devices': {'Capacitors': ['Mounting', #0
                                             'Aluminum Polymer', #1
                                             'Aluminum', #2
                                             'Arrays', #3
                                             'Ceramic', #4
                                             'Supercapacitors and EDLC', #5
                                             'Film', #6
                                             'Mica and PTFE', #7
                                             'Niobium oxide', #8
                                             'Silicon', #9
                                             'Tantalum polymer', #10
                                             'Tantalum', #11
                                             'Thin film', #12
                                             'Variables and trimmers', #13
                                             'Aluminum electrolytic'], #14
                              'Crystals, oscillators, and resonators': ['Crystals', #0
                                                                        'Oscillators', #1
                                                                        'Configurable oscillators', #2
                                                                        'Programmble oscillators', #3
                                                                        'Resonators', #4
                                                                        'Oscillator sockets', #5
                                                                        'Oscillator programmers', #6
                                                                        'Voltage controlled oscillators (VCO)'], #7                        
                              'Filters': ['Mounting', #0
                                          'Ceramic', #1
                                          'Common mode chokes', #2
                                          'DSL', #3
                                          'EMI/RFI', #4
                                          'Feedthrough capacitors', #5
                                          'Ferrite beads', #6
                                          'Ferrite cores and wiring', #7
                                          'Ferrite disks', #8
                                          'Hellical', #9
                                          'Monolithic crystals', #10
                                          'Power line modules', #11
                                          'RF', #12
                                          'SAW'], #13
                              'Inductors and coils': ['Configurable', #0
                                                      'Arrays and signal transformers', #1
                                                      'Delay lines', #2
                                                      'Inductors', #3
                                                      'Wireless charging coils'], #4
                              'Potentiometers and variable resistors': ['Mounting', #0
                                                                        'Adjustable Power Resistor', #1
                                                                        'Joystick Potentiometers', #2
                                                                        'Rotary Potentiometers and rheostats', #3
                                                                        'Scale dials', #4
                                                                        'Slide potentiometers', #5
                                                                        'Thumbwheel potentiometers', #6
                                                                        'Trimmer potentiometers', #7
                                                                        'Potentiometers with display'], #8
                              'Resistors': ['Mounting', #0
                                            'Chassis mount resistors', #1
                                            'Surface mount chip resistors', #2
                                            'Precision trimmed resistors', #3
                                            'Resistor arrays', #4
                                            'Specialized resistors', #5
                                            'Through hole resistors']}, #6  
          'Reliability': {'Circuit protection': ['Mounting', #0
                                                 'Brakers', #1
                                                 'Disconnect switches', #2
                                                 'Electrical fuses', #3
                                                 'Fuse holders', #4
                                                 'Fuses', #5
                                                 'Gas discharge tubes (GDT)', #6
                                                 'Ground fault circuit (GFC)', #7
                                                 'Inrush current limiters (ICL)', #8
                                                 'Lighting protection', #9
                                                 'Resettable fuses', #10
                                                 'Surge suppression', #11
                                                 'Thermal cutoffs (TCO)', #12
                                                 'TVS diodes', #13
                                                 'TV', #14
                                                 'Thyristors TVS', #15
                                                 'Varistors and MOVs TVS']}, #16
          'Active devices': {'Discrete': ['Bridge rectifiers', #0
                                          'Array rectifiers', #1
                                          'Rectifiers', #2
                                          'RF diodes', #3
                                          'Vericaps and varactors', #4
                                          'Zener diode arrays', #5
                                          'Zener diodes', #6
                                          'Power drivers', #7
                                          'DIAC and SIDAC thyristors', #8
                                          'SCR thyristors', #9
                                          'SCR thyristors modules', #10
                                          'TRIAC thyristors', #11
                                          'Bipolar arrays', #12
                                          'Pre-biased bipolar arrays', #13
                                          'RF bipolar transistors', #14
                                          'Bipolar transistors', #15
                                          'Pre-biased bipolars', #16
                                          'MOSFET arrays', #17
                                          'RF MOSFETs', #18
                                          'MOSFETs', #19
                                          'IGBTs modules', #20
                                          'IGBTs', #21
                                          'JFETs', #22
                                          'Programmable unijunction', #23
                                          'Special purpose transistors'], #24
                             'Isolators': ['Digital Isolators', #0
                                           'Gate drivers', #1
                                           'Logic output for optoisolators', #2
                                           'Transistors and photovoltaic output for optoisolators', #3
                                           'Triac and SCR output for optoisolators', #4
                                           'Special purpose'], #5
                             'Radio Fequency (RF)': ['Attenuators', #0
                                                     'Baluns', #1
                                                     'Accessories', #2
                                                     'Amplifiers', #3
                                                     'Antennas', #4
                                                     'Demodulators', #5
                                                     'Detectors', #6
                                                     'Diplexers', #7
                                                     'Directional couplers', #8
                                                     'Evaluation and development kits', #9
                                                     'Front end LNAs and PAs', #10
                                                     'Misc. ICs and modules', #11
                                                     'Mixers', #12
                                                     'Modulators', #13
                                                     'Power controllers', #14
                                                     'Power dividers and splitters', #15
                                                     'Receiver, transmitter, and transceiver units', #16
                                                     'Receivers', #17
                                                     'Shields', #18
                                                     'Switches', #19
                                                     'Transceivers', #20
                                                     'Transceiver modules', #21
                                                     'Transmitters', #22
                                                     'RFI/EMI contacts, fingerstock, and gaskets', #23
                                                     'RFI/EMI shielding and absorbing materials', #24
                                                     'RFID accessories', #25
                                                     'RFID antennas', #26
                                                     'RFID evaluation and development kits', #27
                                                     'RFID reader modules', #28
                                                     'RFID tags and transponders', #29
                                                     'RFID/RF access and monitoring', #30
                                                     'RF detectors', #31
                                                     'Phase detectors']}, #32
          'Thermals': {'Thermal management': ['AC fans', #0
                                              'DC fans', #1
                                              'Fan accessories', #2
                                              'Filters, sleeves and guards', #3
                                              'Thermal accessories', #4
                                              'Thermal pastes', #5
                                              'Heat sinks', #6
                                              'Liquid cooling', #7
                                              'Sheets and pads', #8
                                              'Thermoelectric Peltier assemblies', #9
                                              'Thermoelectric Peltier modules']}, #10
          'Integrated circuits (IC)': {'Audio IC': ['Special purpose'], #0
                                       'Clock and time': ['Application specific', #0
                                                          'Buffers and drivers', #1
                                                          'Generators, PLLs, and synthesizers', #2
                                                          'Delay lines', #3
                                                          'IC batteries', #4
                                                          'Programmable timers and oscillators', #5
                                                          'Real time clocks'], #6
                                       'Data acquisition': ['Special purpose ADCs and DACs', #0
                                                            'Analog fron end (AFE)', #1
                                                            'Analog to digital converters (ADC)', #2
                                                            'Digital potentiometers', #3
                                                            'Digital to analog converters (DAC)', #4
                                                            'Touch screen controllers'], #5
                                       'Embedded': ['Complex programmable logic devices (CPLD)', #0
                                                    'Digital signal processors (DSP)', #1
                                                    'FPGAs', #2
                                                    'Microcontroller FPGAs', #3
                                                    'Microcontroller and microprocessor modules', #4
                                                    'Microcontrollers', #5
                                                    'Application specific microcontrollers', #6
                                                    'Microprocessors', #7
                                                    'Programmable logic devices (PLD)', #8
                                                    'System on chip (SoC)'], #9 
                                       'Signal interfaces': ['Special purpose analog switches', #0
                                                             'Analog switches, multiplexers, and demultiplexers', #1
                                                             'CODECs', #2
                                                             'Contorllers', #3
                                                             'Direct digital synthesis (DDS)', #4
                                                             'Drivers, receivers, and transceivers', #5
                                                             'Encoders, decoders, and converters', #6
                                                             'Active filters', #7
                                                             'I/O expenders', #8
                                                             'Modems', #9
                                                             'Interface modules', #10
                                                             'Sensors and detectors', #11
                                                             'Serializers and deserializers (SERDES)', #12
                                                             'Buffers, repeaters, and splitters', #13
                                                             'Signal termination', #14
                                                             'Specialized interfaces', #15
                                                             'Telecom', #16
                                                             'Universal asynchronous receiver transmitter (UART)', #17
                                                             'Voice recording and playback'], #18
                                       'Linear amplifiers': ['Audio amplifiers', #0
                                                             'Instrumentation amplifiers, Op-Amps, and buffers', #1
                                                             'Special purpose amplifiers', #2
                                                             'Video amplifiers and modules', #3
                                                             'Analog multipliers and dividers', #4
                                                             'Comparators', #5
                                                             'Video processing'], #6
                                       'Digital logic': ['Buffers, drivers, receivers, and transceivers', #0
                                                         'Comparators', #1
                                                         'Counters and dividers', #2
                                                         'FIFO memory', #3
                                                         'Flip flops', #4
                                                         'Gates and inverters', #5
                                                         'Configurable gates and inverters', #6
                                                         'Latches', #7
                                                         'Multivibrators', #8
                                                         'Parity generators and checkers', #9
                                                         'Shift registers', #10
                                                         'Switches, multiplexers, and decoders', #11
                                                         'Specialized logic circuits', #12
                                                         'Translators and level shifters', #13
                                                         'Universal bus functions'], #14
                                       'Memory devices': ['Memory', #0
                                                          'Batteries', #1
                                                          'Configurable PROMs for FPGAs', #2
                                                          'Controllers'], #3
                                       'Power management ICs (PMIC)': ['Offline and AC-DC converters', #0
                                                                       'Battery chargers', #1
                                                                       'Battery management', #2
                                                                       'Current regulation', #3
                                                                       'Display drivers', #4
                                                                       'Energy monitoring', #5
                                                                       'Full and half bridge drivers', #6
                                                                       'Gate drivers', #7
                                                                       'Hot swap controllers', #8
                                                                       'Laser drivers', #9
                                                                       'LED drivers', #10
                                                                       'Lighting and ballast controllers', #11
                                                                       'Contorllers, multiplexers, and ideal diodes', #12
                                                                       'Power factor correction (PFC)', #13
                                                                       'Power distribution switches and load drivers', #14
                                                                       'Specialized power management', #15
                                                                       'Power over Ethernet (PoE) contorllers', #16
                                                                       'Power supply controllers and monitors', #17
                                                                       'RMS to DC converters', #18
                                                                       'Supervisors', #19
                                                                       'Thermal management', #20
                                                                       'V/F and F/V converters', #21
                                                                       'Voltage references', #22
                                                                       'DC-DC switching controllers', #23
                                                                       'DC-DC switching regulators', #24
                                                                       'Linear regulators', #25
                                                                       'Linear and switching regulators', #26
                                                                       'Linear regulator controllers', #27
                                                                       'Special purpose regulators'], #28
                                       'Special purpose ICs': ['Specialized ICs']}, #0
          'Magnetics': {'Transformer and inductor components': ['Coil formers (Bobbins) and mounting', #0
                                                                'Ferrite cores', #1
                                                                'Magnetic wires', #2
                                                                'Accessories', #3
                                                                'Audio', #4
                                                                'Current Sense', #5
                                                                'Step up and down isolated and non-isolated', #6
                                                                'Power transformers', #7
                                                                'Pulse transformers', #8
                                                                'Special purpose transformers', #9
                                                                'Transformers for switching converters']}, #10                           
          'Electromechanical': {'Motors and drivers': ['Accessories', #0
                                                       'Driver boards and modules', #1
                                                       'AC and DC motors', #2
                                                       'Actuators and solenoids', #3
                                                       'Step motors'], #4
                                'Relays': ['Mounting', #0
                                           'I/O relay module racks', #1
                                           'Ananlog I/O relay modules', #2
                                           'Input I/O relay modules', #3
                                           'Output I/O relay modules', #4
                                           'Power relays', #5
                                           'Relay sockets', #6
                                           'Signal relays', #7
                                           'Solid state']}, #8
          'Power supplies': {'On-Board': ['AC-DC converters', #0
                                          'Accessories', #1
                                          'DC-DC converters', #2
                                          'LED drivers'], #3
                             'Off-board': ['AC-AC wall adapters', #0
                                           'AC-DC configurable power supplies', #1
                                           'AC-DC configurable power supply chassis', #2
                                           'AC-DC configurable power supply modules', #3
                                           'AC-DC converters', #4
                                           'AC-DC desktop and wall adapters', #5
                                           'Accessories', #6
                                           'DC-DC converters', #7
                                           'LED drivers', #8
                                           'Power over Ethernet (PoE)']}, #9
          'Sensors and transducers': {'Specialized sensors': ['Accessories', #0
                                                              'Amplifiers', #1
                                                              'Capacitive touch and proximity', #2
                                                              'Color sensors', #3
                                                              'Current transducers', #4
                                                              'Dust sensors', #5
                                                              'Encoders', #6
                                                              'Flex', #7
                                                              'Float and level', #8
                                                              'Flow', #9
                                                              'Force', #10
                                                              'Gas', #11
                                                              'Humidity and moisture', #12
                                                              'Image sensors', #13
                                                              'IrDA transceiver modules', #14
                                                              'Linear variable differential transformer (LVDT) transducers', #15
                                                              'Multifunction', #16
                                                              'Pressure sensors and transducers', #17
                                                              'Solar cells', #18
                                                              'Misc. sensors', #19
                                                              'Strain gauges', #20
                                                              'Ultrasonic receivers and transmitters'], #21
                                      'Magnetic': ['Magnetic field modules and compass', #0
                                                   'Linear and compass ICs', #1
                                                   'Position, proximity, and speed modules', #2
                                                   'Solid state switches', #3
                                                   'Multi purpose magnets', #4
                                                   'Magnetic actuators'], #5
                                      'Motion': ['Accelerometers', #0
                                                 'Gyroscopes', #1
                                                 'Inertial measurement Units (IMU)', #2
                                                 'Inclinometers', #3
                                                 'Optical', #4
                                                 'Tilt switches', #5
                                                 'Vibration'], #6
                                      'Optical': ['Ambient light, IR, and UV', #0
                                                  'Distance Measuring', #1
                                                  'Mouse', #2
                                                  'CdS cells photo detectors', #3
                                                  'Digital output photo detectors', #4
                                                  'Remote receiver photo detectors', #5
                                                  'Photodiodes', #6
                                                  'Industrial photoelectric', #7
                                                  'Digital output photointerrupters', #8
                                                  'Transistor output photointerrupters', #9
                                                  'Phototransistors', #10
                                                  'Analog output and reflective', #11
                                                  'Digital output and reflective'], #12
                                      'Position and proximity': ['Angle and linear position measuring', #0
                                                                 'Proximity', #1
                                                                 'Proximity occupancy modules'], #2
                                      'Sensor cables and interfaces': ['Mounting', #0
                                                                       'Assemblies', #1
                                                                       'Junction blocks'], #2
                                      'Temperature': ['Analog and digital output', #0
                                                      'NTC thermistors', #1
                                                      'PTC thermistors', #2
                                                      'Resistance Temperature Detector (RTD)', #3
                                                      'Thermocouples and temperature detectors', #4
                                                      'Mechanical thermostats', #5
                                                      'Solid state thermostats']} #6
                                                      }



 
  
     
