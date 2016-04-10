"""
An extension to wait at least 1 instance on Scrapoxy.

You can change the delay with WAIT_FOR_START parameters (120 seconds by default).
"""

# -*- coding: utf-8 -*-

import logging
import time


class WaitMiddleware(object):

    def __init__(self, crawler):
        self._WAIT_FOR_START = crawler.settings.get('WAIT_FOR_START') or 120


    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)


    def process_response(self, request, response, spider):
        if response.status != 407:
            return response

        spider.log(u'[WaitMiddleware] Sleeping {0} seconds because no proxy is found: {1}'.format(self._WAIT_FOR_START, response.body), level=logging.WARNING)
        time.sleep(self._WAIT_FOR_START)

        return request.replace(
            dont_filter=True,
        )
