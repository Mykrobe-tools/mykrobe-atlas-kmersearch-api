from os import environ
from tempfile import TemporaryDirectory

import cobs_index as cobs


COBS_INDEX_PATH = environ.get('COBS_INDEX_PATH', '/data/500.cobs_compact')
COBS_TERM_SIZE = 31
COBS_POSITIVE_RATE = 0.4


class Cobs:
    def __init__(self, index_path=COBS_INDEX_PATH):
        self.search_instance = cobs.Search(index_path)

    def search(self, query, threshold):
        return self.search_instance.search(query, threshold=threshold)

    @staticmethod
    def build(path_to_file_list, sample_names):
        with TemporaryDirectory() as tmpdir:
            doclist = cobs.DocumentList(tmpdir)

            with open(path_to_file_list) as f:
                for path in f:
                    doclist.add(path.strip())

            for doc, name in zip(doclist, sample_names):
                doc.name = name

            p = cobs.CompactIndexParameters()
            p.term_size = COBS_TERM_SIZE
            p.false_positive_rate = COBS_POSITIVE_RATE
            p.clobber = True
            cobs.compact_construct_list(doclist, COBS_INDEX_PATH, p)
