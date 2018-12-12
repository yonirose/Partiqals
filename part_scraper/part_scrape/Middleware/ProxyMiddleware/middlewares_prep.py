import re
import random
import base64
import logging
from urllib.parse import urlparse

from scrapy.exceptions import IgnoreRequest

from utils.proxies import get_proxies 
import db_setup as db
log = logging.getLogger('scrapy.proxies')


class Mode:
    RANDOMIZE_PROXY_EVERY_REQUESTS, RANDOMIZE_PROXY_ONCE, SET_CUSTOM_PROXY = range(3)


class RandomProxy(object):
    def __init__(self, settings):
        self.mode = settings.get('PROXY_MODE')
        self.proxy_list = settings.get('PROXY_LIST')
        self.chosen_proxy = ''
        self.read_proxy_list()
    
    def read_proxy_list(self):
        get_proxies(proxy_type='elite')
        log.info('Read a new proxy list')
        
        if self.mode == Mode.RANDOMIZE_PROXY_EVERY_REQUESTS or self.mode == Mode.RANDOMIZE_PROXY_ONCE:
            if self.proxy_list is None:
                raise KeyError('PROXY_LIST setting is missing')
            self.proxies = {}
            with open(self.proxy_list) as fin:
                for line in fin.readlines():
                    parts = re.match('(\w+://)([^:]+?:[^@]+?@)?(.+)', line.strip())
                    if not parts:
                        continue

                    # Cut trailing @
                    if parts.group(2):
                        user_pass = parts.group(2)[:-1]
                    else:
                        user_pass = ''
                    self.proxies[parts.group(1) + parts.group(3)] = user_pass
            if self.mode == Mode.RANDOMIZE_PROXY_ONCE:
                self.chosen_proxy = random.choice(list(self.proxies.keys()))
        elif self.mode == Mode.SET_CUSTOM_PROXY:
            custom_proxy = settings.get('CUSTOM_PROXY')
            self.proxies = {}
            parts = re.match('(\w+://)([^:]+?:[^@]+?@)?(.+)', custom_proxy.strip())
            if not parts:
                raise ValueError('CUSTOM_PROXY is not well formatted')

            if parts.group(2):
                user_pass = parts.group(2)[:-1]
            else:
                user_pass = ''

            self.proxies[parts.group(1) + parts.group(3)] = user_pass
            self.chosen_proxy = parts.group(1) + parts.group(3)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        # Don't overwrite with a random one (server-side state for IP)
        if 'proxy' in request.meta:
            if request.meta["exception"] is False:
                return
        request.meta["exception"] = False
        if len(self.proxies) == 0:
            self.read_proxy_list()
            # raise ValueError('All proxies are unusable, cannot proceed')

        if self.mode == Mode.RANDOMIZE_PROXY_EVERY_REQUESTS:
            proxy_address = random.choice(list(self.proxies.keys()))
        else:
            proxy_address = self.chosen_proxy

        proxy_user_pass = self.proxies[proxy_address]

        if proxy_user_pass:
            basic_auth = 'Basic ' + base64.b64encode(proxy_user_pass.encode()).decode()
            request.headers['Proxy-Authorization'] = basic_auth
        #else:
        #    log.debug('Proxy user pass not found')

        request.meta['proxy'] = proxy_address
        log.info('Using proxy <%s>, %d proxies left' % (
                proxy_address, len(self.proxies)
            ))
    
    def process_response(self, request, response, spider):
        if response.status == 200:
            db.prepdb.delete_one({'path': urlparse(response.url).path})
            db.prepdb.update_one({'dist': spider.name.split('_')[0],
                                  'current_count': {'$exists': 1}},
                                 {'$inc': {'current_count': 1}})
        return response
    
    def process_exception(self, request, exception, spider):
        if 'proxy' not in request.meta:
            return
        if self.mode == Mode.RANDOMIZE_PROXY_EVERY_REQUESTS or self.mode == Mode.RANDOMIZE_PROXY_ONCE:
            proxy = request.meta['proxy']
            try:
                del self.proxies[proxy]
            except KeyError:
                pass
            request.meta["exception"] = True
            if self.mode == Mode.RANDOMIZE_PROXY_ONCE:
                self.chosen_proxy = random.choice(list(self.proxies.keys()))
            log.info('Removing failed proxy <%s>, %d proxies left' % (
                proxy, len(self.proxies)))
