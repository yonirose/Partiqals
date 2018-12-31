# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 11:32:15 2017

@author: jrosenfe
v6d
"""

import os
import re
from lxml import etree
from operator import itemgetter, attrgetter
from collections import namedtuple, defaultdict, deque, abc, UserList
# import itertools
# import copy
import cv2
import numpy as np
from shapely.ops import unary_union
from shapely.geometry import box, mapping

if __name__ == '__main__':
    import line_parser as lp
else:    
    from analyzer import line_parser as lp

import utils.error_logging as er
import config as cfg


class ElemList(UserList):
    def __init__(self, elem_type):
        super().__init__()
        self.Element = elem_type
    
    def __setitem__(self, indxs, val):
        try:
           if len(indxs) == 2:
               s = []
               for indx in indxs: 
                   if isinstance(indx, int):
                       s.append(slice(indx, indx+1, None))
                   elif isinstance(indx, slice):
                       s.append(indx)
                   else:
                       raise TypeError('Index is %s but must be int or slice' % type(indx))
               for y in range(s[0].start, s[0].stop, 1 if s[0].step == None else s[0].step):
                   for x in range(s[1].start, s[1].stop, 1 if s[1].step == None else s[1].step):
                       super().append(self.Element(y=y, x=x, val=val))
           else:
               raise IndexError('Expected two indexes but %s were given' % len(indxs))
        except TypeError: # Catches object of type 'int' has no len()
           super().__setitem__(indxs, val)
    
           
class HTMLTableProcessor():
    Element = namedtuple('Element', ['y', 'x', 'val'])
    
    def __init__(self, path, db_elems=None):
        self.elems = ElemList(self.Element)
        if db_elems is None:
            self.db_elems = []
        self.path = path
        self.term_loc = defaultdict(deque)
    
    def extract_html(self):
        def get_value_type(val):
            if val.isalpha():
                return 'a' # aplha
            elif val.isnumeric():
                return 'n' # numeric
            elif val.isalnum():
                return 'an' # alphanumeric
            else:
                return 'v' # A value that does not qualify as the three above
        
        try:
            with open('%s.html' % self.path, encoding='utf-8') as f:
                page = f.read()
        except UnicodeDecodeError:
            # Execptions will not be raised with latin-1 even with encoding errors
            with open(self.path+'.html', encoding='latin-1') as f:
                page = f.read()

        tree = etree.HTML(page)
        self.page_width = int(tree.xpath('//img')[0].attrib['width'])
        self.page_height = int(tree.xpath('//img')[0].attrib['height'])
        self.table_map = np.empty([self.page_height, self.page_width], dtype=str)
        divs = tree.xpath('//div')
        
        for div in divs:
            try:
                left = int(re.findall(r'left:(\d+)', div.attrib['style'])[0])
                top = int(re.findall(r'top:(\d+)', div.attrib['style'])[0])
                
                child_text = ''
                for child in div.iterchildren():
                    font_size = int(re.findall(r'font-size:(\d+)',
                                               child.attrib['style'])[0])
                    if font_size > cfg.MIN_FONT_SIZE and child.text:
                        child_text += child.text
                # top=y, left=x
                self.table_map[top:top+cfg.CHAR_HEIGHT_PIXEL,
                               left:left+len(child_text)*cfg.CHAR_LENGTH_PIXEL] = get_value_type(child_text)
                               
                xmid = int(left + len(child_text)*cfg.CHAR_LENGTH_PIXEL/2)
                #self.elems.append(self.Element(y=top, x=xmid, val=child_text))
                self.elems[top, xmid] = child_text
                self.term_loc[child_text].append(self.Element(y=top, x=left, val=child_text))
            except IndexError:
                pass
    
    def vertical_padding(self, elem):
        try:
            # Scan down
            del_y = cfg.SCAN_DOWN_DELTA
            while not any(self.table_map[elem.y+del_y,
                          elem.x:elem.x+cfg.MIN_HORIZ_LINE_LENGTH] == '_'):
                del_y += 1
            if del_y >= cfg.PADDING_DELTA:
                self.elems[elem.y+cfg.PADDING_DELTA:
                           elem.y+del_y-cfg.PADDING_DELTA:
                           cfg.PADDING_DELTA, elem.x] = elem.val
            # Scan up
            del_y = cfg.SCAN_UP_DELTA            
            while not any(self.table_map[elem.y-del_y,
                          elem.x:elem.x+cfg.MIN_HORIZ_LINE_LENGTH] == '_'):
                del_y += 1
            if del_y >= cfg.PADDING_DELTA:
                self.elems[elem.y-del_y:elem.y:cfg.PADDING_DELTA, elem.x] = elem.val
        except IndexError:
            pass
    
    def vertical_limit_lines(self, min_y1, min_x1, max_y1, max_x2):
        # Add lines to indicate left and right vertical table limits
        for x_leftright in [min_x1-1, max_x2+1]:
            self.table_map[min_y1:max_y1+1, x_leftright] = '||'
            self.elems[min_y1:max_y1+1:cfg.BOUND_Y_SPACING, x_leftright] = '||'

    def horiz_limit_lines(self, y_top, xmin, ymax, xmax):
        # Add additional horizontal lines to indicate seperation between tables
        for y_coord in [y_top, ymax+1]:
            self.table_map[y_coord, xmin:xmax] = '_'
            self.elems[y_coord, xmin:xmax+1:cfg.BOUND_X_SPACING] = '='
            # Try to fit line between the left table side to the edge of the page
            self.elems[y_coord, 0:xmin:cfg.BOUND_X_SPACING] = '='
            # Try to fit line between the right table side to the edge of the page
            self.elems[y_coord, xmax+1:self.page_width:cfg.BOUND_X_SPACING] = '='
                   
    def vertical_table_lines(self, min_y1, min_x1, max_y1, max_x2):         
        # Fill vertical lines inside the table if possible
        for x_coord in range(min_x1, max_x2, cfg.VERT_LINE_SPACING):
            if (self.table_map[min_y1:max_y1, x_coord] == 'v').all():
               self.table_map[min_y1:max_y1, x_coord] = '|'
               self.elems[min_y1, x_coord] = '|'
    
    def find_vertical_lines(self, horiz_lines):
        all_rects = []
        table_bounds = []
        xmin_shifted_horiz_lines = defaultdict(list)
        
        for xmin, lines in horiz_lines.items():
            ymin = min(lines, key=attrgetter('y')).y
            ymax = max(lines, key=attrgetter('y')).y
            xmax = max(lines, key=attrgetter('xmax')).xmax
            if not ymin == ymax: # Check that it is not a single line
                bins = [ymin-1]
                for y_coord in range(0, ymax-cfg.WHITE_SPACE_HEIGTH,
                                     cfg.WHITE_SPACE_HEIGTH):
                    if (self.table_map[y_coord:y_coord+cfg.WHITE_SPACE_HEIGTH,
                                       xmin:xmax] == '').all():
                        bins.append(y_coord)
                bins.append(ymax+1)
                bins = sorted(list(set(bins)))
                xmin_shifts = list(range(len(bins)))
                
                # np.digitize returns the indices of the bins to which each value
                # in input array belongs
                ylines = [line.y for line in lines]
                for ind, line in zip(np.digitize(ylines, bins), lines):
                    xmin_shifted_horiz_lines[xmin_shifts[ind-1]].append(line)
                    
        all_rects = []
        for lines in xmin_shifted_horiz_lines.values():
            xmin = min(lines, key=attrgetter('xmin')).xmin 
            ymin = min(lines, key=attrgetter('y')).y
            ymax = max(lines, key=attrgetter('y')).y
            xmax = max(lines, key=attrgetter('xmax')).xmax
            
            poly = box(xmin, ymin, xmax, ymax)
            if poly.is_valid:
                all_rects.append(poly)
        
        if all_rects:
            # Perform union operation on all the found rectangles grouped by xmin_shifted    
            table_union_info = mapping(unary_union(all_rects))
            if table_union_info['type'] == 'Polygon':
                coords = list(table_union_info['coordinates'])
            elif table_union_info['type'] == 'MultiPolygon':
                coords = [_[0] for _ in table_union_info['coordinates']]
            else:
                return
            ''' <--
            else:
                raise TypeError('%s type is not valid' % table_union_info['type'])
            '''
        else:
            return
        
        # After union is done find the bounding min and max of these shapes
        # This will bound the polygons as rectangles representing tables
        for coord in coords:
            xmin = int(min(coord, key=itemgetter(0))[0])
            ymin = int(min(coord, key=itemgetter(1))[1])
            xmax = int(max(coord, key=itemgetter(0))[0])
            ymax = int(max(coord, key=itemgetter(1))[1])
            self.vertical_limit_lines(ymin, xmin, ymax, xmax)
            table_bounds.append((ymin, xmin, ymax, xmax))
            
            # Fill vertical lines inside the table if possible and needed
            self.vertical_table_lines(ymin, xmin, ymax, xmax)
        
        # print(table_bounds)
        # find top seperator for cases where tables don't have top line
        def table_top_limits(ymax, xmin, xmax, y_coord=None, ymin=None):
            if not ymin == None:
                y_coord = ymin
            elif y_coord == None:
                raise ValueError('y_coord and ymin cannot be both None')
            
            # Mark top and bottom of table
            self.table_map[y_coord, xmin:xmax] = '_'
            self.table_map[ymax, xmin:xmax] = '_'
            # Check to left and right of table if possible to mark as well
            for y in [y_coord, ymax]:
                for xstart, xend in [(0, xmin-1),
                                     (xmax+1, self.page_width)]:
                    if (self.table_map[y, xstart:xend] == '').all():
                        self.table_map[y, xstart:xend] = '_'
                self.elems[y, xmin:xmax+1:cfg.BOUND_X_SPACING] = '='
                
        for ymin, xmin, ymax, xmax in table_bounds:
            if (self.table_map[ymin:ymin+cfg.TOP_TABLE_ROW, xmin:xmax] == 'a').any():
                table_top_limits(ymin=ymin, ymax=ymax, xmin=xmin, xmax=xmax)
                # print('Top line exists')
                '''
                self.table_map[ymin, xmin:xmax] = '_'
                self.table_map[ymax, xmin:xmax] = '_'
                '''
            else: # Table does not have top line and need to be found
                for y_coord in range(ymin-1, 0, -cfg.WHITE_SPACE_HEIGTH):
                    if (self.table_map[y_coord-cfg.WHITE_SPACE_HEIGTH:y_coord,
                                       xmin:xmax] == '').all():
                        table_top_limits(y_coord=y_coord, ymax=ymax,
                                         xmin=xmin, xmax=xmax)
                        '''
                        # Mark top and bottom table
                        self.table_map[y_coord, xmin:xmax] = '_'
                        self.table_map[ymax, xmin:xmax] = '_'
                        # Check to left and right of table if possible to mark as well
                        for y in [y_coord, ymax]:
                            for xstart, xend in [(0, xmin-1),
                                                 (xmax+1, self.page_width)]:
                                if (self.table_map[y, xstart:xend] == '').all():
                                    self.table_map[y, xstart:xend] = '_'
                            self.elems[y, xmin:xmax+1:cfg.BOUND_X_SPACING] = '='
                        '''
                        break
        
    def extractdata_tablegrid(self):
        img = cv2.imread(self.path+'.png')
        img_width = img.shape[1]
        img_height = img.shape[0]
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edge = cv2.Canny(gray, cfg.CANNY_TH1, cfg.CANNY_TH2,
                         apertureSize = cfg.APERTURE_SIZE)

        lines = cv2.HoughLinesP(edge, rho = 1, theta = 1*np.pi/180,
                                threshold = 5, minLineLength = 5,
                                maxLineGap = 5)
        
        horiz_lines = defaultdict(list)
        num_vert_lines = 0
        TableLine = namedtuple('TableLine', ['xmin', 'y', 'xmax'])
        try:
            for _ in range(lines.shape[0]):
                x1 = int(lines[_][0][0]*(self.page_width/img_width))
                x1 = int(np.floor(x1/10)*10) # Bring x2 to the nearest tenth
                y1 = int(lines[_][0][1]*(self.page_height/img_height))
                x2 = int(lines[_][0][2]*(self.page_width/img_width))
                x2 = int(np.floor(x2/10)*10) # Bring x2 to the nearest tenth
                y2 = int(lines[_][0][3]*(self.page_height/img_height))
                
                if abs(y1 - y2) <= cfg.HORIZ_LINE_SLOPE: 
                    self.table_map[y1, min(x1, x2):max(x1, x2)] = '_'
                    self.elems[y1, x1] = '_'
                    # self.elems.append(self.Element(y=y1, x=x1, val='_'))
                    if abs(x1-x2) > cfg.MIN_HORIZ_LINE_LENGTH:
                        horiz_lines[min(x1, x2)].append(
                                TableLine(xmin=min(x1, x2), y=y1, xmax=max(x1, x2))
                            )
                elif abs(x1 - x2) <= cfg.VERT_LINE_SLOPE and \
                    abs(y1 - y2) > cfg.MIN_VERT_LINE_LENGTH:
                        self.table_map[min(y1, y2):max(y1, y2), x1] = '|'
                        self.elems[y1, x1] = '|'
                        # self.elems.append(self.Element(y=y1, x=x1, val='|'))
                        num_vert_lines += 1
        # Catch and pass when 'lines' is a 'NoneType' when no lines are found in the page
        except AttributeError:
            pass
        
        # Apply the vertical line algorithm only when not many vertical lines were found
        #if num_vert_lines <= cfg.MIN_NUM_VERT_LINES: <--------
        if horiz_lines:
            self.find_vertical_lines(horiz_lines) 
                
        # Pad horizontal elements
        # iterv_elems = copy.deepcopy(self.elems)
        # for elem in copy.deepcopy(self.elems):
        for elem in self.elems.copy():
            if elem.val == '_':
                continue
            elif (not elem.val == '|'
                 and not elem.val == '||'
                 and not elem.val == '='):
                    self.vertical_padding(elem)     
                
                
class PageAnalyzer(HTMLTableProcessor):
    def __init__(self, path, part_num):
        if path is not None:
            super().__init__(path)
            self.extract_html()
            self.extractdata_tablegrid()
        self.part_num = part_num
        # <==
        self.collect_terms = {'word': [], 'param': [], 'unit': [], 'cond': [],
                              'term': []}
        
    def cleanup_collection(self, direct):
        if any(self.collect_terms.values()):
            for data_type in ['word', 'param', 'unit', 'cond']:
                self.collect_terms[data_type] = list(set(self.collect_terms[data_type]))
            
            # Romve duplicate terms in 'term' WITH order
            _terms = []
            for _term in self.collect_terms['term']:
                if _term not in _terms:
                    if not  _term[-1] == '-':
                        _terms.append(_term)
            self.collect_terms['term'] = _terms
            
    
            # Check if the line was parsed as a single line and therefore is considered just as a condition
            # This is done to capture situation of a SINGLE line like this: gate voltage vgs=10 V
            ''' NOT SURE IF NEEDED ANYMORE SINCE IT IS TAKEN CARE IN LINE_PARSE
            if self.collect_terms['cond'] and self.collect_terms['param'] and \
                self.collect_terms['unit'] and not self.collect_terms['term']:
                    split_terms = self.collect_terms['cond'][0].split()
                    # Check if there is realy a term before the condition
                    if len(split_terms) > 1 and not split_terms[1] == '=':
                        self.collect_terms['term'] = [split_terms[0]]
                        self.collect_terms['word'] = self.collect_terms['term']
                        self.collect_terms['cond'][0] = ' '.join(self.collect_terms['cond'][0].split()[1:])
            '''
            
            # Sort multiple terms based on their original location
            # First, sort by y. Second, trim y values to nearest tenth.
            # For example, 122 and 118.3 will turn to be 120 using round(x, -1)
            # Thrid, sort by x
            terms_tosort = []
            for term in self.collect_terms['term']:
                try:
                    first_term = self.term_loc[term].popleft()
                    # This is needed to ensure items for both horizontal and vertical scans
                    self.term_loc[term].append(first_term)
                    terms_tosort.append(
                            # self.Element(round(first_term.y, -1),
                            self.Element(first_term.y,
                                         first_term.x,
                                         term)
                                )
                except IndexError: # Catches when self.term_loc does not have term item or empty
                    pass
            
            if terms_tosort:
                terms_tosort = sorted(terms_tosort, key=attrgetter('y', 'x'))
                self.collect_terms['term'] = [term.val for term in terms_tosort]
                '''
                self.collect_terms['word'] = list(
                        {split_trm.lower() 
                            for term in self.collect_terms['term']
                                for split_trm in term.split()}
                    )
                '''
            self.db_elems.append({**self.collect_terms, **{'direct': direct}})
            self.collect_terms = {'word': [], 'param': [], 'unit': [],
                                  'cond': [], 'term': []}
            return self.db_elems[-1] # Return the last added db_elems
        else:
            return None
                                    
    def collect_insidetable(self, term):
        self.text_to.reset_result()
        # Explicit decoration
        self.err_to.logger(term, 'info', self.part_num)(self.text_to.parse)(term)
       
        for data_type in ['cond', 'word', 'param', 'unit', 'term']:
            self.collect_terms[data_type] += self.text_to.result[data_type]
            if '' in self.collect_terms[data_type]:
                self.collect_terms[data_type].remove('')
        
        # Add sub-terms to self.term_loc to account for modified terms after processing
        for subterm in self.text_to.result['term']:
            if subterm is not term:
                self.term_loc[subterm] = self.term_loc[term]
        
    def scan_tablegrids(self, groups, sep, direct):
        for group in groups:
            if group.val == sep:
                yield self.cleanup_collection(direct)
            elif (not group.val == '|'
                 and not group.val == '||'
                 and not group.val == '_'
                 and not group.val == '='):
                    self.collect_insidetable(group.val) 
        # This yield is here since when there are no horizotnal lines the for loop
        # never reaches the yield resulting in infinite loop. Also, using return
        # will result in StopIteration exception resulting in infinit loop
        yield self.cleanup_collection(direct)
        
    def group_elems(self, direct):
        sep = {'v': ('x', 'y', '|', '='), 'h': ('y', 'x', '_', '||')}
        
        top_idx = 0
        iter_elems = sorted(self.elems, key=attrgetter(sep[direct][0]))
        for bot_idx, elem in enumerate(iter_elems):
            if not elem.val == sep[direct][2]:
                continue
            else:
                yield from self.scan_tablegrids(
                        sorted(iter_elems[top_idx:bot_idx+1],
                               key=attrgetter(sep[direct][1])),
                        sep=sep[direct][3],
                        direct=direct
                    )
                top_idx = bot_idx + 1
                

class MongoElem(PageAnalyzer):
    def __init__(self, path, part_num):
        super().__init__(path, part_num)
    
    def ext_elems(self, ext_elems_to_analyze):
        for elem in ext_elems_to_analyze:
            self.text_to.reset_result()
            self.text_to.parse(elem)
            yield self.text_to.result
        
    def unit_conv(self, unit, from_range, to_range):
        unit_scale = {'f': 1e-15, 'p': 1e-12, 'n': 1e-9, 'u': 1e-6,
                      'm': 1e-3, 'k': 1e3, 'M': 1e6, 'G': 1e9, 'T': 1e12}
        special_units = {'mils': (0.0000254, 'm', 'u'), '"': (0.0254, 'm', ''),
                         'ft': (0.3048, 'm', ''), 'ft2': (0.3048**2, 'm2', ''),
                         'ft3': (0.3048**3, 'm3', ''), 'cm': (0.01, 'm', ''),
                         'cm2': (0.01**2, 'm2', ''), 'cm3': (0.01**3, 'm3', ''),
                         'min': (60, 's', ''), 'hr': (3600, 's', ''),
                         'T': (1, 'T', ''), 'm': (1, 'm', ''), 'm2': (1, 'm2', ''),
                         'm3': (1, 'm3', ''), 'lb': (453.592, 'g', '')}
        try:
            # Special cases
            umult, _unit, _unit_scale = special_units[unit]
        except KeyError:
            try:
                if len(unit) > 2 and unit[:3] == 'ppm':
                    umult = 1
                    _unit = unit
                    _unit_scale = ''
                else:
                    umult = unit_scale[unit[0]]
                    _unit = unit[1:]
                    _unit_scale = unit[0]
                    if unit[-1] in ['2', '3']:
                        umult = umult**int(unit[-1])
                        _unit_scale = _unit_scale+unit[-1]
            except (KeyError, IndexError): # Accounts for no prefix cases
                if '°F' in unit:
                    from_range = (from_range - 32)*0.5556
                    to_range = (to_range - 32)*0.5556
                    _unit = unit.replace('°F', '°C')
                elif '°K' in unit:
                    from_range = from_range - 273.15
                    to_range = to_range - 273.15
                    _unit = unit.replace('°K', '°C')
                else:
                    _unit = unit if unit else ''
                umult = 1
                _unit_scale = ''
        return _unit, _unit_scale, from_range*umult, to_range*umult
    
    def get_mongoelem(self, db_elem, param, unit, from_range, to_range):
        _unit, _unit_scale, from_range, to_range = self.unit_conv(unit, from_range, to_range)
        
        # Combine the original elem with the new keys/values
        return {
                **db_elem, **{'param': param['param'] if param else [from_range, to_range],
                'unit': _unit, 'from': from_range, 'to': to_range,
                'unit_scale': _unit_scale, 'orig_unit': unit}
            }


class MongoDocCreator(MongoElem):
    def __init__(self, path=None, part_num=None, perc=cfg.SINGLE_PARAM_RANGE):
                 #ext_elems_to_analyze=None):
        self.perc = perc # Determines the range from to parameters for a single param
        if path is not None:
            super().__init__(path, part_num)
            self.gens = [self.group_elems(direct='h'), self.group_elems(direct='v')]

        self.text_to = lp.Parser()
        self.err_to = er.ErrorHandler()
                
    def make_mongo_doc(self, db_elem):
        sparams_nounit = [] # sparams = single param
        sparams_unit = []
        rparams_nounit = [] # rparams = range param
        rparams_unit = []
        sorter = {
                (1, float): lambda _: sparams_nounit.append({'param': _[0]}),
                (1, int): lambda _: sparams_nounit.append({'param': _[0]}),
                (2, str): lambda _: sparams_unit.append({'param': _[0],
                                                         'unit': _[1]}),
                (2, float): lambda _: rparams_nounit.append({'from': _[0],
                                                           'to': _[1]}),
                (2, int): lambda _: rparams_nounit.append({'from': _[0],
                                                           'to': _[1]}),
                (3, int): lambda _: rparams_nounit.append({'from': min(_),
                                                           'to': max(_)}),
                (3, float): lambda _: rparams_nounit.append({'from': min(_),
                                                             'to': max(_)}),    
                (3, str): lambda _: rparams_unit.append({'from': _[0],
                                                         'to': _[1],
                                                         'unit': _[2]}),
                (4, str): lambda _: rparams_unit.append({'from': min(_[0:3]),
                                                         'to': max(_[0:3]),
                                                         'unit': _[3]})
            }
        
        def from_to(param): # To account for negative numbers
            return (min(param*(1-self.perc/100), param*(1+self.perc/100)),
                    max(param*(1-self.perc/100), param*(1+self.perc/100)))
        
        def sort_params():
            for param in db_elem['param']:
                if len(param) == 4 and isinstance(param[2], str) \
                    and isinstance(param[3], str): # This means it is a range with different unit scale
                        conv_result = []
                        for idx1, idx2 in [(2, 0), (3, 1)]:
                            conv_result.append(self.unit_conv(
                                    unit=param[idx1],
                                    from_range=param[idx2],
                                    to_range=param[idx2]
                                ))
                        param = (conv_result[0][-1], conv_result[1][-1],
                                 conv_result[1][0])
                sorter[len(param), type(param[-1])](param)
        
        def make_doc():
            '''
            The alogrithm to sort out different type of numbers and combinations works like this:
            The algorithm is applied per line. First, number (param) elements are divided into
            four groups: single parameter with and without units attached and range 
            parameters with and without units attached. After that, each group is analyzed.
            The single parameter with unit range will be +/-perc with the attached unit.
            If there are also single parameters without attached units all the found units
            will be attached (one by one) to each single parameters without a unit.
            If only single parameters without a unit exists then min() and max() is
            applied and all units found are attached. The range parameters with and
            without units are handled normally.
            '''
            sort_params()
            # Go over the four groups and return mongo-ready dict for insertion
            if sparams_unit and sparams_nounit:
                sp_mixed_params = {'param': []}
                sp_mixed_units = []
                for _ in sparams_unit:
                    sp_mixed_params['param'].append(_['param'])
                    sp_mixed_units.append(_['unit'])
                for _ in sparams_nounit:
                    sp_mixed_params['param'].append(_['param'])
                for unit in sp_mixed_units:
                    yield self.get_mongoelem(db_elem,
                            sp_mixed_params,
                            unit,
                            min(sp_mixed_params['param']),
                            max(sp_mixed_params['param'])
                        )
            else:        
                for sparam_unit in sparams_unit:
                    f, t = from_to(sparam_unit['param'])
                    yield self.get_mongoelem(db_elem, sparam_unit,
                                        sparam_unit['unit'],
                                        f, t)
                if sparams_nounit:
                    sp_nounit = {}
                    sp_nounit['param'] = [v for d in sparams_nounit
                                            for v in d.values()]
                    if len(sp_nounit['param']) > 1:
                        from_range = min(sp_nounit['param'])
                        to_range = max(sp_nounit['param'])
                    else:
                        # Convert from list of one number to just a number
                        sp_nounit['param'] = sp_nounit['param'][0] 
                        from_range, to_range = from_to(sp_nounit['param'])
                    if db_elem['unit']:
                        for unit in db_elem['unit']:
                            yield self.get_mongoelem(
                                db_elem, sp_nounit, unit, from_range,
                                to_range
                            )
                    else:
                        yield self.get_mongoelem(
                                db_elem, sp_nounit, '', from_range,
                                to_range
                            )
                
            for rparam_unit in rparams_unit:
                yield self.get_mongoelem(db_elem, '',
                                         rparam_unit['unit'],
                                         rparam_unit['from'],
                                         rparam_unit['to'])
            for rparam_nounit in rparams_nounit:
                if db_elem['unit']:
                    for unit in db_elem['unit']:
                        yield self.get_mongoelem(db_elem, '', unit,
                                                 rparam_nounit['from'],
                                                 rparam_nounit['to'])
                else:
                    yield self.get_mongoelem(db_elem, '', '',
                                             rparam_nounit['from'],
                                             rparam_nounit['to'])
        return make_doc()
        
    def make_mongoelem(self, ext_elems_to_analyze=None):
        if ext_elems_to_analyze is not None:
            if isinstance(ext_elems_to_analyze, abc.MutableSequence):
                self.gens = [self.ext_elems(ext_elems_to_analyze)]
            else:
                self.gens = [self.ext_elems([ext_elems_to_analyze])]
            
        for gen in self.gens:
            while True:
                try:
                    db_elem = next(gen)
                except StopIteration:
                    break
                if db_elem:
                    if db_elem['param']:
                        yield from self.make_mongo_doc(db_elem)
                    else:
                        db_elem['unit'] = ''
                        yield db_elem
                              
if __name__ == '__main__':
    
    # ana = MongoDocCreator(path='..\..\..\Ceramic Resonators.html\page1')
    # ana = MongoDocCreator(path=r'..\..\..\1.5KE200A.html\page2')
    # ana = MongoDocCreator('..\..\..\VRF2933p2.html\page1')
    # ana.extract_html('datasheet.html\page1.html')
    # ana.extract_tablegrid('datasheet.html\page1.png')
    # ana.extract_html('1.5KE200A.html\page3.html')
    # ana.extract_tablegrid('1.5KE200A.html\page3.png')
    # ana.extract_html('ASFL1.html\page1.html')
    # ana.extract_tablegrid('ASFL1.html\page1.png')
    # ana.extract_html('Taiyo_Yuden-FI212L062002-T.html\page4.html')
    # ana.extractdata_tablegrid('Taiyo_Yuden-FI212L062002-T.html\page4.png')
    
    # ana =  MongoDocCreator('..\..\PDF_db\FDC6305N.html\page2')
    ana = MongoDocCreator(os.path.join('pdf_extract', 'RMCF1210ZT0R00__Stackpole_Electronics_Inc',
                                       'RMC.html', 'page1'))

    # ana =  MongoDocCreator('..\..\..\SMP1340-079LF.html\page2')
    
    # ana =  MongoDocCreator(r'..\..\..\NPCCM0530M_M1040MLP.html\page1')
    
    # ana =  MongoDocCreator(r'..\..\..\test_horiz_grid_type15.html\page1')
    # ana =  MongoDocCreator(r'..\..\..\Taiyo_Yuden-FI212L062002-T.html\page4')
    
    # ana =  MongoDocCreator(r'..\..\..\PYu-RC_Group_51_RoHS_L_8.html\page1')
    
    # ana.extract_html('RF power transistor the LdmoST plastic family.html\page1.html')
    # ana.extractdata_tablegrid('RF power transistor the LdmoST plastic family.html\page1.png')   
    # ana.extract_html('MRF1513NT1.html\page1.html')
    # ana.extractdata_tablegrid('MRF1513NT1.html\page1.png')    
    # ana.extract_html('ARF460A_B(G)_E.html\page1.html')
    # ana.extractdata_tablegrid('ARF460A_B(G)_E.html\page1.png')
    # ana.extract_html('2SK3557-D.html\page1.html')
    # ana.extractdata_tablegrid('2SK3557-D.html\page1.png')
    # ana.extract_html('MRFE6VP6300HR3.html\page1.html')
    # ana.extractdata_tablegrid('MRFE6VP6300HR3.html\page1.png') 
    # ana.extract_html('UWT1C100MCL1GB_page1.html\page1.html')
    # ana.extractdata_tablegrid('UWT1C100MCL1GB_page1.html\page1.png')
    # ana.extract_html('cghv14250.html\page1.html')
    # ana.extractdata_tablegrid('cghv14250.html\page1.png')
    
    #ana.extract_html('BLL8H1214L.html\page1.html')
    #ana.extractdata_tablegrid('BLL8H1214L.html\page1.png')
    
    
    a = ana.make_mongoelem()
    a=list(a)
    
