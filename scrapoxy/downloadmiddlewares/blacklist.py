"""
An extension to detect blacklisted status and restart Scrapoxy instances.

You must fill :
API_SCRAPOXY with the commander URL
API_SCRAPOXY_PASSWORD with credential
BLACKLIST_HTTP_STATUS_CODES with the list of blacklisted HTTP codes
"""

# -*- coding: utf-8 -*-

from scrapy.exceptions import IgnoreRequest
from scrapoxy.commander import Commander

import logging
import random
import time



class BlacklistError(Exception):
    def __init__(self, response, message, *args, **kwargs):
        super(BlacklistError, self).__init__(*args, **kwargs)

        self.response = response
        self.message = message


    def __str__(self):
        return self.message



class BlacklistDownloaderMiddleware(object):

    def __init__(self, crawler):
        """Access the settings of the crawler to connect to Scrapoxy.
        """
        self._http_status_codes = crawler.settings.get('BLACKLIST_HTTP_STATUS_CODES', [503])
        self._sleep_min = crawler.settings.get('SCRAPOXY_SLEEP_MIN', 60)
        self._sleep_max = crawler.settings.get('SCRAPOXY_SLEEP_MAX', 180)

        self._commander = Commander(
            crawler.settings.get('API_SCRAPOXY'),
            crawler.settings.get('API_SCRAPOXY_PASSWORD')
        )


    @classmethod
    def from_crawler(cls, crawler):
        """Call constructor with crawler parameters
        """
        return cls(crawler)


    def process_response(self, request, response, spider):
        """Detect blacklisted response and stop the instance if necessary.
        """
        try:
            if response.status in self._http_status_codes:
                raise BlacklistError(response, u'HTTP status {}'.format(response.status))

            return response

        except BlacklistError as ex:
            spider.log(u'Ignoring Blacklisted response {0}: {1}'.format(response.url, ex.message), level=logging.DEBUG)

            name = response.headers.get(u'x-cache-proxyname')
            self._stop_and_sleep(spider, name)

            raise IgnoreRequest()


    def _stop_and_sleep(self, spider, name):
        if name:
            alive = self._commander.stop_instance(name)
            if alive < 0:
                spider.log(u'Remove: cannot find instance {}'.format(name), level=logging.ERROR)
            elif alive == 0:
                spider.log(u'Remove: instance removed (no instance remaining)', level=logging.WARNING)
            else:
                spider.log(u'Remove: instance removed ({} instances remaining)'.format(alive), level=logging.DEBUG)
        else:
            spider.log(u'Cannot find instance name in headers', level=logging.ERROR)

        delay = random.randrange(self._sleep_min, self._sleep_max)
        spider.log(u'Sleeping {} seconds'.format(delay), level=logging.INFO)
        time.sleep(delay)
