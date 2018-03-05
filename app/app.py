# -*- coding: utf-8 -*-
"""
    Main Application.
"""

from app.crawler import Crawler
from app.manager import PersistManager


# USAGE =================================================

async def run(loop):

    manager = PersistManager(use_index=True)  # enable 'use_index' to use Elasticsearch (Part 3)
    crawler = Crawler(loop=loop, manager=manager)

    await crawler.get_history()  # Retrieve 5 minute history (Part 1)
    await crawler.run_updates()  # Constant updates (Part 2)
