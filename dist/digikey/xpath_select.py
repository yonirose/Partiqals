# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 13:50:40 2017

@author: jrosenfe
"""
# Prep spider
INIT_SUBCAT_NAMES = '//a[contains(@href, "%s")]/text()'
INIT_SUBCAT_LINKS = '//a[contains(@href, "%s")]/@href'
DRILL_SUBCAT_NAMES = '//li/a[contains(@href, "products")]/text()'
DRILL_SUBCAT_LINKS = '//li/a[contains(@href, "products")]/@href'
BREAD_CRUMBS1 = '//*[@id="content"]/h1/a[2]/text()'
BREAD_CRUMBS2 = '//div/h1[contains(@class, "breadcrumbs")]/text()'
PREP_COUNTS = "//span[@id='matching-records-count']/text()"

# Main crawler
# Part catagories and sub-catagories
CAT = '//*[@id="content"]/h1/a[2]/text()'
SUBCAT = '//div/h1[contains(@class, "breadcrumbs")]'

# Table headers
TABLE_LEN = '//tr/td[contains(@class, "tr-compareParts")]'
HEAD_START_IDX = 14
HEAD_TITLE = '//*[@id="tblhead"]/tr[1]/th[%s]/text()'
MISC_DATA = '//*[@id="lnkPart"]/tr[%s]/td[%s]/text()'

# Part information
PDF_LINK = '//*[@id="lnkPart"]/tr[%s]/td[2]/a/@href'
DIST_LINK = '//*[@id="lnkPart"]/tr[%s]/td[4]/a/@href'
DIST_NUM = '//*[@id="lnkPart"]/tr[%s]/td[4]/a/text()'
PART_NUM = '//*[@id="lnkPart"]/tr[%s]/td[5]/a/span/text()'
MANUFAC = '//*[@id="lnkPart"]/tr[%s]/td[6]/span/a/span/text()'
DESCR = '//*[@id="lnkPart"]/tr[%s]/td[7]/text()'
UNIT_PRICE = '//*[@id="lnkPart"]/tr[%s]/td[9]/text()'
MIN_QUAN = '//*[@id="lnkPart"]/tr[%s]/td[10]/text()'
NEXT_PAGE = '//a[contains(@class, "Next")]/@href'

