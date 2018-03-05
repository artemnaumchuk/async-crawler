# -*- coding: utf-8 -*-
"""
    Constants and config values.
"""
# HTTP Code
HTTP_SUCCESS = 200

# ULRs
URL_MARKETS = 'https://poloniex.com/public?command=returnTicker'
URL_HISTORY = 'https://poloniex.com/public?command=returnChartData&period={period}&start={start}&end={end}&currencyPair={currency}'

# Elasticsearch
ELASTIC_HOST = 'localhost:9200'
ELASTIC_HTTP_AUTH = None
ELASTIC_INDEX = 'olhc'

# Filename
FILE_NAME = 'data.json'

# Offsets and Periods
UPD_FREQUENCY = 30  # sec
HISTORY_PERIOD = 300  # sec

# Thread pool size
THREAD_POOL_SIZE = 5

# Logging format
LOG_FORMAT = '%(levelname)s: %(asctime)s - %(message)s'
