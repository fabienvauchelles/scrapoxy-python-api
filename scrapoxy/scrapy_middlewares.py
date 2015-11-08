# -*- coding: utf-8 -*-

import base64
import re


class Proxy:

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)


    def __init__(self, crawler):
        proxy = crawler.settings.get('PROXY')
        if proxy:
            parts = re.match(r'(\w+://)(\w+:\w+@)?(.+)', proxy)

            if parts.group(2):
                self._proxy_auth = u'Basic ' + base64.encodestring(parts.group(2)[:-1]).strip()

            self._proxy = parts.group(1) + parts.group(3)


    def process_request(self, request, spider):
        if request.meta.get('no-proxy'):
            # Ignore
            return

        # Don't overwrite with a random one (server-side state for IP)
        if hasattr(self, '_proxy'):
            request.meta['proxy'] = self._proxy

            if hasattr(self, '_proxy_auth'):
                request.headers['proxy-authorization'] = self._proxy_auth
