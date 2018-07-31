# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 14:35:35 2017

@author: jrosenfe
"""

# process line parameters
ERROR_FILE_NAME = 'analyze_err.log'
MIN_NUM_CHARS = 3

# HTML analysis parameters
MIN_FONT_SIZE = 3

CANNY_TH1 = 30
CANNY_TH2 = 200
APERTURE_SIZE = 5 # Can only take these values: 3, 5, and 7

MIN_HORIZ_LINE_LENGTH = 20
MIN_VERT_LINE_LENGTH = 10
VERT_LINE_SPACING = 4
BOUND_Y_SPACING = 8
BOUND_X_SPACING = 2

VERT_LINE_SLOPE = 0 # 0 means a straight line
HORIZ_LINE_SLOPE = 0 # 0 means a straight line
MIN_NUM_VERT_LINES = 20 # 20

SCAN_DOWN_DELTA = 6
SCAN_UP_DELTA = 1
PADDING_DELTA = 6

CHAR_LENGTH_PIXEL = 6
CHAR_HEIGHT_PIXEL = 8

SINGLE_PARAM_RANGE = 0.05 # Given in percentage 0 to 1

WHITE_SPACE_HEIGTH = 10

TOP_TABLE_ROW = 10

# PDF analysis parameters
MAX_PDF_PAGES = 10

SIMILAR_SCORE = 0.4 # Used in query.py
ELEM_SIMILAR_SCORE = 0.2 # Used in pdf_analyze.py

MIN_NUM_WORDS = 1
MAX_NUM_WORDS = 10

KEEP_GRIDFS_PDF = False
KEEP_PDF_IN_DB = False

# Dispacther process
NUM_PROC = 2

# PDF agent spider
PDF_AGENT_URL = 'https://www.datasheetpro.com/search/'
# SINGLE_PDF_XPATH = "/html/body/div[3]/div/div[1]/article[1]/div/div[2]/a/@href"
# MANY_PDF_XPATH = "/html/body/div[3]/div/div[1]/article[1]/div[1]/div[2]/a/@href"
# AGENT_PDF_XPATH = "/html/body/div[3]/div/div[1]/article[1]/div[1]/div[2]/a/@href"
AGENT_PDF_XPATH = '/html/body/div[3]/div/div[1]/article/div[1]/div[2]/a/@href'

# Spiders
PERC_TO_SCAN = 0.0005 # Used in main spider. Values are between 0 to 1
BATCH_SIZE = 173
SCRAPY_LOG_NAME = 'scrapy_log.log'
SPIDER_LIST = ['digikey']
