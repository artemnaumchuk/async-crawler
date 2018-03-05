#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import logging

from app import run

if __name__ == '__main__':

    loop = asyncio.get_event_loop()
    loop.set_debug(False)
    task = loop.create_task(run(loop))
    loop.run_until_complete(task)
