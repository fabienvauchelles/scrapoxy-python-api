"""
An extension to upscale / downscale Scrapoxy.

When Scrapy starts, Scrapoxy is upscaled to max instances.
When Scrapy stops, Scrapoxy is downscaled to min instances.

You must fill :
API_SCRAPOXY with the commander URL
API_SCRAPOXY_PASSWORD with credential

You can change the delay with WAIT_FOR_SCALE parameters (120 seconds by default).
"""

# -*- coding: utf-8 -*-

from scrapoxy.commander import Commander
from scrapy import signals

import logging
import time


class ScaleMiddleware(object):

    def __init__(self, crawler):
        self._commander = Commander(
            crawler.settings.get('API_SCRAPOXY'),
            crawler.settings.get('API_SCRAPOXY_PASSWORD')
        )

        self._WAIT_FOR_SCALE = crawler.settings.get('WAIT_FOR_SCALE') or 120

        crawler.signals.connect(self.spider_opened, signals.spider_opened)
        crawler.signals.connect(self.spider_closed, signals.spider_closed)


    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)


    def spider_opened(self, spider):
        spider.logger.debug(u'[ScaleMiddleware] Upscale Scrapoxy')

        min_sc, required_sc, max_sc = self._commander.get_scaling()
        required_sc = max_sc

        self._commander.update_scaling(min_sc, required_sc, max_sc)

        spider.log(u'[ScaleMiddleware] Sleeping {0} seconds to finish upscale'.format(self._WAIT_FOR_SCALE), level=logging.WARNING)
        time.sleep(self._WAIT_FOR_SCALE)


    def spider_closed(self, spider):
        spider.logger.debug(u'[ScaleMiddleware] Downscale Scrapoxy')

        min_sc, required_sc, max_sc = self._commander.get_scaling()
        required_sc = min_sc

        self._commander.update_scaling(min_sc, required_sc, max_sc)
