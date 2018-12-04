# -*- coding: utf-8 -*-
"""
Created on Fri Nov 30 09:03:29 2018

@author: jrosenfe
"""

class BaseError(Exception):
   ''' Base class for other exceptions '''
   pass


class CaptchaError(BaseError):
    ''' Raised when captcha word appears in the response url '''
    pass