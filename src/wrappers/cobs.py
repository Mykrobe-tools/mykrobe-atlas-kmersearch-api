from os import environ

import cobs_index as cobs


COBS_INDEX_PATH = environ.get('COBS_INDEX_PATH', '/data/500.cobs_compact')


def search(query, threshold, index_path=COBS_INDEX_PATH):
    s = cobs.Search(index_path)
    return s.search(query, threshold=threshold)


def build(document_dir_path, output_path, term_size, clobber, false_positive_rate):
    p = cobs.CompactIndexParameters()
    p.term_size = term_size
    p.clobber = clobber
    p.false_positive_rate = false_positive_rate

    cobs.compact_construct(document_dir_path, output_path, index_params=p)