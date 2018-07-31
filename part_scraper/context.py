# -*- coding: utf-8 -*-
"""
Created on Fri May  5 12:32:34 2017

@author: jrosenfe
"""

from OpenSSL import SSL
from scrapy.core.downloader.contextfactory import ScrapyClientContextFactory


class CustomContextFactory(ScrapyClientContextFactory):
    """
    Custom context factory that allows SSL negotiation.
    """
    
    def __init__(self):
        # Use SSLv23_METHOD so we can use protocol negotiation
        self.method = SSL.SSLv23_METHOD

