# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 14:10:46 2017

@author: jrosenfe
v4
"""
from math import pi
from itertools import cycle

from bokeh.io import output_file, show
from bokeh.plotting import figure, reset_output
from bokeh.layouts import gridplot
from bokeh.models import HoverTool, ColumnDataSource, OpenURL, TapTool, NumeralTickFormatter
# from bokeh.models.widgets import DataTable, TableColumn
from bokeh.palettes import Category20, Pastel1
from bkcharts import Donut
import pandas as pd

import query_v4 as query
import db_conn


class PlotHandler(db_conn.MongoDb):
    def __init__(self, qry):
        output_file('Partipedia_plot.html')
        self.q = query.QueryHandler(qry)
        self.clr_circle = cycle(Category20[20])
        self.clr_map = dict()
        self.all_plots = []
        self.all_dists = []
        self.param_unit_partnums = []
        self.all_partnums = []
        self.all_parts = []
        self.labels = [
                'vfrom', 'vto', 'hval',
                'hunit', 'unit', 'part_num', 'term',
                'cond', 'manufac', 'nunit_price',
                'dist', 'dist_num', 'hunit_price',
                'dist_partlink', 'descr'
            ]
        
    def create_config(self, parts):
        self.dist = parts.process_parts()
        # This will include parts from common prop finding process
        # self.all_parts.append(parts.all_parts_found) 
        self.dist.find_dist()
        
        dist_clrcircle = cycle(Pastel1[9])
        dist_clrmap = {}
        # self.dist.distnames_found.append('Mouser')
        for dist, clr in zip(self.dist.distnames_found, dist_clrcircle):
            dist_clrmap[dist] = clr

        for part_num, clr in zip(parts.partnum_found, self.clr_circle):
            if part_num not in self.clr_map:
                self.clr_map[part_num] = clr
        '''
        self.dist.dist_found=self.dist.dist_found.append(pd.DataFrame({
                                'descr': 'RF FET N CH 500V 10A PSH PUL PR',
                                'dist': 'Mouser', 'dist_partlink': '',
                                'manufac': 'Microsemi Corporation',
                                'nunit_price': 200, 'part_num': 'ARF476FL',
                                'pdf_link': [''], 'unit_price': 200}))
        '''
        try:
            parts_dists = pd.merge(parts.parts_found,
                                   self.dist.dist_found_min_unit_price,
                                   how='inner')
            # self.all_dists.append(dist.dist_found)
            '''
            columns = [TableColumn(field="unit_price", title="Unit price"),
                       TableColumn(field="part_num", title="MPN")]
            data_table = DataTable(source=self.source, columns=columns, width=400, height=280)
            '''
            self.df = parts_dists[self.labels].copy(deep=True)
            self.df['clr'] = self.df['part_num'].apply(lambda _: self.clr_map[_])
            self.df['dist_clr'] = self.df['dist'].apply(lambda _: dist_clrmap[_])
            
            c = ConfigPlots(source=ColumnDataSource(data=self.df))
            
            # It is important to invoke the c methods in this order
            self.all_plots.append([c.range_range(parts),
                                   c.range_partnum(parts),
                                   c.price_partnum(self.dist),
                                   c.inven_donut()])
        # Catching and passing parts that don't have params and units
        # Or terms that could not be found
        except (KeyError, ValueError):
            pass
            
    def create_plots(self):
        for parts in self.q.run_query():
            self.create_config(parts)
            self.all_dists.append(self.dist.dist_found)   
        self.param_unit_partnums = parts.param_unit_partnums
        # This include found parts that don't have units and params
        self.all_partnums = parts.all_partnums
        
    def commonprop_plots(self, matches_toplot):
        for term, comm_parts in matches_toplot.items():
            parts = query.Parts(parts_found=comm_parts, user_term=term)
            self.create_config(parts)


class HoverHandler():
    def __init__(self, plot_type):
        self.plot_type = plot_type
    
    @property    
    def make_hover_tool(self):
        if self.plot_type == 'range_range':
            return self.range_range_hover()
        elif self.plot_type == 'range_partnum':
            return self.range_partnum_hover()
        elif self.plot_type == 'price_partnum':
            return self.price_partnum_hover()
    
    def range_range_hover(self):
        return HoverTool(
                tooltips=[
                    ('Parameter', '@term'),
                    ('Condition', '@cond'),
                    ('Value', '%s %s' %
                    ('@hval', '@hunit')),
                    ('Part', '@part_num'),
                    ('Manufacturer', '@manufac'),
                    ('Description', '@descr')
                ]
            )
            
    def range_partnum_hover(self):
        return HoverTool(
                tooltips=[
                    ('Parameter', '@term'),
                    ('Condition', '@cond'),
                    ('Value', '%s %s' % ('@hval', '@hunit')),
                    ('Part', '@part_num'),
                    ('Manufacturer', '@manufac'),
                    ('Description', '@descr')
                ]
            )

    def price_partnum_hover(self):
        return HoverTool(
                tooltips=[
                    ('Distributer', '@dist'),
                    ('SKU', '@dist_num'),
                    ('Unit price', '@hunit_price')
                ]
            )

                
class ConfigPlots(db_conn.MongoDb):
    def __init__(self, source=None):
        self.source = source

    def config_figure(
            self, title=None, x_range=None, y_range=None, plot_width=None,
            plot_height=None, hover=[], plot_tools=[
                    'pan', 'wheel_zoom', 'box_zoom',
                    'box_select', 'lasso_select', 'reset', 'save'
                ],
            min_borderleft = 100,
            xaxis_label=None, yaxis_label=None, xaxis_fonttype='normal',
            yaxis_fonttype='normal', xaxis_orient=0
        ):
        if plot_width or plot_height:
            if plot_width and plot_height:
                plot_config = dict(plot_width = plot_width,
                                   plot_height = plot_height)
            elif plot_width and not plot_height:
                plot_config = dict(plot_width = plot_width)
            else:
                plot_config = dict(plot_height = plot_height)
            plt = figure(title=title, y_range=y_range, x_range=x_range,
                         **plot_config, tools=hover+plot_tools)
        else:
            plt = figure(title=title, y_range=y_range, x_range=x_range,
                         tools=plot_tools+hover)
        plt.min_border_left = min_borderleft
        plt.xaxis.axis_label = xaxis_label
        plt.yaxis.axis_label = yaxis_label
        plt.xaxis.axis_label_text_font_style = xaxis_fonttype
        plt.yaxis.axis_label_text_font_style = yaxis_fonttype
        plt.xaxis.major_label_orientation = xaxis_orient

        return plt
    
    def range_range(self, parts):
        hover = HoverHandler('range_range')
        
        p = self.config_figure(
                title=parts.user_term.title(), plot_height=400,
                hover=[hover.make_hover_tool],
                xaxis_label='Lower Limit [%s]' % parts.unit,
                yaxis_label='Upper Limit [%s]' % parts.unit
            )
        self.y_range_range_range = p.y_range # To enable plot linking
        p.circle(
                'vfrom', 'vto',
                size=((10+parts.num_partsfound)/parts.num_partsfound)*10,
                fill_color='clr', line_color='clr', fill_alpha=0.5,
                hover_fill_color='white', hover_line_color='clr',
                source=self.source
            )       
        return p
    
    def range_partnum(self, parts):
        hover = HoverHandler('range_partnum')
        '''
        y_range=[
            parts.min_from-abs(parts.min_from)*0.5,
                parts.max_to*1.1
        ]
        '''
        
        p = self.config_figure(
                plot_height=400, 
                hover=[hover.make_hover_tool],
                x_range=list(parts.parts_found['part_num'].unique()),
                y_range=self.y_range_range_range, # To enable plot linking
                yaxis_label='Magnitude [%s]' % parts.unit,
                xaxis_orient=pi/4
            )
        
        self.x_range_range_partnum = p.x_range
        p.segment(
                'part_num', 'vfrom', 'part_num', 'vto', line_width=3,
                 line_color='clr', source=self.source
            )
        p.circle(
                'part_num', 'vfrom', size=10, fill_color='clr',
                line_color='clr', line_width=3, hover_fill_color='white',
                hover_line_color='clr', fill_alpha=1, source=self.source
            )
        p.circle(
                'part_num', 'vto', size=10, fill_color='clr',
                line_color='clr', line_width=3, hover_fill_color='white',
                hover_line_color='clr', fill_alpha=1, source=self.source
            )
        return p
    
    def price_partnum(self, dist):
        hover = HoverHandler('price_partnum')
        # formatters={'unit_price' : 'printf'})
        
        '''
        y_range = [
            -50, dist.dist_found['nunit_price'].max()*1.07
                if dist.dist_found['nunit_price'].max() > 1
                    or dist.dist_found['nunit_price'].max() < -1 else 0.5
        ]
        '''
        p = self.config_figure(
                plot_height=400, hover=[hover.make_hover_tool],
                x_range=self.x_range_range_partnum,
                yaxis_label='Unit ptice',
                xaxis_orient=pi/4
            )
        
        p.add_tools(TapTool())
        url = '@dist_partlink'
        taptool = p.select(type=TapTool)
        taptool.callback = OpenURL(url=url)
        p.yaxis[0].formatter = NumeralTickFormatter(format='$0.00')
        
        p.segment(
                'part_num', 0, 'part_num', 'nunit_price', line_width=3,
                line_color='clr', source=self.source
            )

        p.circle(
                'part_num', 'nunit_price', size=10, fill_color='dist_clr',
                line_color='dist_clr', line_width=3, hover_fill_color="white",
                hover_line_color='dist_clr', fill_alpha=1,
                muted_color='dist_clr', muted_alpha=0.2, legend='dist',
                source=self.source
            )
        p.legend.location = "top_left"
        p.legend.click_policy = "mute"
        return p
    
    def inven_donut(self, h=600, w=600):
        inven_df = pd.DataFrame(list(self.invendb.find()))
        d = Donut(
                data=inven_df, label=['cat', 'subcat'], values='total',
                text_font_size='8pt', hover_text='total', height=h, width=w,
                palette=Category20[20]
            )
        # output_file("donut.html", title="donut.py example")
        # show(d)
        return d
           
if __name__ == '__main__':
    db = db_conn.MongoDb()
    db.setup_db()
    
    # plots = PlotHandler(qry='drain source voltage and current drain and ce3512k2')
    plots = PlotHandler(qry='maximum voltage')
    # plots = PlotHandler(qry='drain source voltage + ce3512k2')
    plots.create_plots()
    
    show(gridplot(plots.all_plots, toolbar_location='above',
         toolbar_options=dict(logo=None)))
    # reset_output()
    '''
    common = query.FindCommonProp(partnum_found=plots.param_unit_partnums)
    common.findcommon_properties()
    plots.commonprop_plots(matches_toplot=common.all_matches)
    
    show(gridplot(plots.all_plots, toolbar_location='above',
        toolbar_options=dict(logo=None))
    )
    '''
    inven_plot = ConfigPlots()
    inven_plot.inven_donut()
    reset_output()
    