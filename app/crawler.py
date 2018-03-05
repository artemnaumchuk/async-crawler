# -*- coding: utf-8 -*-
"""
    Data crawler.
    Preform public API for data managing.
    Use asyncio for public methods with ThreadPoolExecutor on bulk operations
"""
import asyncio
import concurrent
import logging
import threading
import time

from pip._vendor import requests

from app.config import (URL_HISTORY, HISTORY_PERIOD, UPD_FREQUENCY, URL_MARKETS, HTTP_SUCCESS, LOG_FORMAT, THREAD_POOL_SIZE)

# Logging
logging.basicConfig(format=LOG_FORMAT, datefmt='%m/%d/%Y %I:%M:%S')
logger = logging.getLogger('APP')
logger.setLevel(logging.INFO)


class Crawler(object):

    def __init__(self, loop, manager):
        self.initial_time = time.time()
        self.loop = loop
        self.manager = manager
        self.markets = None

    # private methods -------------------------------

    def _fetch(self, url):
        """ Perform http requests.
        """
        response = requests.get(url)
        if response.status_code != HTTP_SUCCESS:
                raise Exception('Error fetch data. External resource respond with {}'.format(response.status_code))
        data = response.json()
        return data

    async def _init_market(self):
        """ Handle market init process.
        """
        if not self.markets:
            try:
                markets = self._fetch(URL_MARKETS)
                self.markets = list(markets.keys())
            except Exception as ex:
                logger.exception('Error initialization markets', exc_info=True)
                raise

            # Success
            logger.info('Market successfully initialized')
            return

    # public API -----------------------------------

    def persist(self, data, lock):
        """  Adapter for PersistManager.
        """
        return self.manager.persist(data, lock)

    async def get_history(self):
        """ Retrieve 5 min history.
        """
        if not self.markets:
            await self._init_market()

        def get_item_history(currency, lock, offset=HISTORY_PERIOD): # single item maintain
            url = URL_HISTORY.format(period=offset, start=self.initial_time - offset, end=self.initial_time, currency=currency)
            try:
                data = self._fetch(url)
            except Exception as ex:
                logger.exception('Error getting history', exc_info=True)

            for entry in data:
                entry['currencyPair'] = currency
                try:
                    self.persist(entry, lock)
                except Exception as ex:
                    logger.exception('Impossible to store data', exc_info=True)
                    raise

        lock = threading.Lock()
        pool_executor = concurrent.futures.ThreadPoolExecutor(max_workers=THREAD_POOL_SIZE)
        _tasks = [self.loop.run_in_executor(pool_executor, get_item_history, item, lock) for item in self.markets]

        await asyncio.wait(_tasks)

        # Success
        logger.info('History successfully updated')
        return

    async def run_updates(self, timeout=UPD_FREQUENCY):
        """ Retrieve constant data updates.
        """
        def update_item(currency):  # single item maintain
            curr_time = time.time()
            url = URL_HISTORY.format(period=300, start=curr_time - 300, end=curr_time, currency=currency)
            try:
                data = self._fetch(url)

            except Exception as ex:
                logger.exception('Error update values', exc_info=True)
                raise

            # TODO: Persist new values

        pool_executor = concurrent.futures.ThreadPoolExecutor(max_workers=THREAD_POOL_SIZE)

        while True:
            _tasks = [self.loop.run_in_executor(pool_executor, update_item, item) for item in self.markets]
            await asyncio.sleep(timeout, loop=self.loop)
            await asyncio.wait(_tasks)

            # Success
            logger.info('Data successfully updated')
        return

