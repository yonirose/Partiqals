# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 13:50:40 2017

@author: jrosenfe
"""
# Prep spider
INIT_SUBCAT_NAMES = '//a[contains(@href, "%s")]/text()'
INIT_SUBCAT_LINKS = '//a[contains(@href, "%s")]/@href'
DRILL_SUBCAT_NAMES = "//ul[@class='sub-cats']//a/descendant::text()"
DRILL_SUBCAT_LINKS = "//ul[@class='sub-cats']//a/@href"
BREAD_CRUMBS = '//a[contains(@id, "Breadcrumbs")]/text()'
PREP_COUNTS = "//span[@id='ctl00_ContentMain_lblProductCount']/text()"

# Main crawler

# Table headers
TABLE_LEN = '//td[contains(@class, "td-select")]'
HEAD_START_IDX = 12
HEAD_TITLE = '//tr[@class="SearchResultColumnHeading"]/th[%s]/text()'
MISC_DATA = '//*[@id="ctl00_ContentMain_SearchResultsGrid_grid"]/tr[%s]/td[%s]/text()'

# Part information
PDF_LINK = '//*[@id="ctl00_ContentMain_SearchResultsGrid_grid"]/tr[%s]/td[7]/a/@href'
DIST_LINK = '//*[@id="ctl00_ContentMain_SearchResultsGrid_grid"]/tr[%s]/td[3]/div/a/@href'
DIST_NUM = '//*[@id="ctl00_ContentMain_SearchResultsGrid_grid"]/tr[%s]/td[3]/div/a/text()'
PART_NUM = '//*[@id="ctl00_ContentMain_SearchResultsGrid_grid"]/tr[%s]/td[4]/div/a/text()'
MANUFAC = '//*[@id="ctl00_ContentMain_SearchResultsGrid_grid"]/tr[%s]/td[5]/a/text()'
DESCR = '//*[@id="ctl00_ContentMain_SearchResultsGrid_grid"]/tr[%s]/td[6]/text()'
UNIT_PRICE = '//*[@id="ctl00_ContentMain_SearchResultsGrid_grid"]/tr[%s]/td[9]//span/text()'
MIN_QUAN = '//*[@id="ctl00_ContentMain_SearchResultsGrid_grid"]/tr[%s]/td[10]//tr/td[2]/text()'
NEXT_PAGE = '//*[@id="ctl00_ContentMain_PagerTop_lnkNext"]/@href'

