"""
An extension to use Scrapoxy as a proxy for Scrapy.

You must fill PROXY in settings:
PROXY = 'http://127.0.0.1:8888/?noconnect'

Don't forget the ?noconnect to use HTTPS over HTTP.
"""

# -*- coding: utf-8 -*-

import base64
import re


class ProxyMiddleware(object):

    def __init__(self, crawler):
        proxy = crawler.settings.get('PROXY')
        if proxy:
            parts = re.match(r'(\w+://)(\w+:\w+@)?(.+)', proxy)

            if parts.group(2):
                self._proxy_auth = u'Basic ' + base64.encodestring(parts.group(2)[:-1].encode()).decode().strip()

            self._proxy = parts.group(1) + parts.group(3)


    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)


    def process_request(self, request, spider):
        if request.meta.get('no-proxy'):
            # Ignore
            return

        # Don't overwrite with a random one (server-side state for IP)
        if hasattr(self, '_proxy'):
            request.meta['proxy'] = self._proxy

            if hasattr(self, '_proxy_auth'):
                request.headers['proxy-authorization'] = self._proxy_auth
