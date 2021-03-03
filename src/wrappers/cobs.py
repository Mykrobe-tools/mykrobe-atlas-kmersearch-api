from os import environ

import cobs_index as cobs


COBS_INDEX_PATH = environ.get('COBS_INDEX_PATH', '/data/500.cobs_compact')
COBS_TERM_SIZE = 31


class Cobs:
    def __init__(self, index_path=COBS_INDEX_PATH):
        self.search_instance = cobs.Search(index_path)

    def search(self, query, threshold):
        return self.search_instance.search(query, threshold=threshold)
