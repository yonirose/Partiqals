# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 09:15:39 2016

@author: jrosenfe
"""

import requests
from lxml.html import fromstring

def get_proxies(fname='proxy_list.txt', proxy_type='all'):
    '''
    proxy_type can take the following types: all, elite, anonymous, transparent
    '''
    
    null = '' # It is actually used when eval is invoked
    proxy_list = []
    #proxy_source = r'http://www.gatherproxy.com/proxylist/country/?c=United%20States'
    proxy_source = r'http://www.gatherproxy.com/proxylist/anonymity/?t=Elite'
    response = requests.get(proxy_source)
    if response.status_code == 200:
        parser = fromstring(response.text)
        raw_data = parser.xpath('//*[@id="tblproxy"]/script/text()')
        with open(fname, 'w') as f:
            for proxy in raw_data:
                proxy = eval(proxy[proxy.index('{'):proxy.index('}')+1])
                proxy['PROXY_PORT'] = str(int(proxy['PROXY_PORT'], 16))
                proxy_list.append(proxy)
                if proxy_type == 'all' or proxy['PROXY_TYPE'] == proxy_type.capitalize():
                    f.write('http://%s:%s\n' % (proxy['PROXY_IP'], proxy['PROXY_PORT']))
    else:
        print('Connection error. Response code %s' % response.status_code)
    
    return proxy_list 
