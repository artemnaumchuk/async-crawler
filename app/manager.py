# -*- coding: utf-8 -*-
"""
    PersistManager.
    Manage file writing and operation on Elasticsearch indexes.
"""

import json
import os
from elasticsearch import Elasticsearch

from app.config import FILE_NAME, ELASTIC_HOST, ELASTIC_INDEX


class PersistManager(object):

    def __init__(self, use_index=False):

        self.filename = FILE_NAME
        self.use_index = use_index

        if self.use_index:
            self.elasticsearch = Elasticsearch(hosts=[ELASTIC_HOST])
            self.elasticsearch.indices.create(index=ELASTIC_INDEX, ignore=400)

    # private methods -------------------------------

    def _save_to_file(self, data):
        if not os.path.isfile(self.filename):
            with open('data.json', 'w') as f_handle:
                f_handle.write('[]')

        with open(self.filename, 'a+') as f_handle:
            f_handle.seek(0, 2)
            f_handle.truncate(f_handle.tell() - 1)
            if f_handle.tell() > 2:
                f_handle.write(',')
            f_handle.write(json.dumps(data, indent=1))
            f_handle.write(']')

    def _save_index(self, data):
        self.elasticsearch.index(index=ELASTIC_INDEX, doc_type='currency', body=data)

    # public API -----------------------------------

    def persist(self, data, lock):
        with lock:
            self._save_to_file(data)
            if self.use_index:
                self._save_index(data)
