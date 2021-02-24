from os import environ

import cobs_index as cobs


COBS_INDEX_PATH = environ.get('COBS_INDEX_PATH', '/data/500.cobs_compact')
COBS_TERM_SIZE = int(environ.get('COBS_TERM_SIZE', 31))


def search(query, threshold, index_path=COBS_INDEX_PATH):
    s = cobs.Search(index_path)
    return s.search(query, threshold=threshold)