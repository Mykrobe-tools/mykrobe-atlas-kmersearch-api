from datetime import datetime
from os import environ
from pathlib import Path
from tempfile import TemporaryDirectory

import cobs_index as cobs

COBS_CLASSIC_INDEXES_DIR = environ.get('COBS_CLASSIC_INDEXES_DIR', '/data/classic')
COBS_TERM_SIZE = 31
COBS_POSITIVE_RATE = 0.4


class Cobs:
    def __init__(self):
        index_paths = [p for p in Path(COBS_CLASSIC_INDEXES_DIR).iterdir() if Path.is_file(p)]
        self.search_instances = [cobs.Search(str(index_path)) for index_path in index_paths]

    def search(self, query, threshold):
        results = []

        for search_instance in self.search_instances:
            results += search_instance.search(query, threshold=threshold)

        return results

    @staticmethod
    def build(sample_paths, sample_names):
        with TemporaryDirectory() as tmpdir:
            doclist = cobs.DocumentList(tmpdir)

            for path in sample_paths:
                doclist.add(path.strip())

            for doc, name in zip(doclist, sample_names):
                doc.name = name

            p = cobs.ClassicIndexParameters()
            p.term_size = COBS_TERM_SIZE
            p.false_positive_rate = COBS_POSITIVE_RATE
            setattr(p, 'continue', True)
            classic_path = Path(COBS_CLASSIC_INDEXES_DIR) / datetime.now().strftime("%Y-%m-%d_%H:%M:%S.cobs_classic")
            cobs.classic_construct_list(doclist, str(classic_path), p)
