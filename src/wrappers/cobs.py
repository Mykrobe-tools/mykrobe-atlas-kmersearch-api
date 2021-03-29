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
        index_paths = []
        for path in Path(COBS_CLASSIC_INDEXES_DIR).iterdir():
            if path.is_dir():
                index_paths += [p for p in path.iterdir() if p.is_file()]
        self.search_instances = [cobs.Search(str(index_path)) for index_path in index_paths]

    def search(self, query, threshold):
        results = []

        for search_instance in self.search_instances:
            results += search_instance.search(query, threshold=threshold)

        flatten = []
        for r in results:
            flatten.append((r.score, r.doc_name))
        return flatten

    @staticmethod
    def build(sample_paths, sample_names):
        assert len(sample_paths) == len(sample_names)

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

            signature_size = cobs.calc_signature_size(len(sample_paths), p.num_hashes, p.false_positive_rate)
            classic_path = Path(COBS_CLASSIC_INDEXES_DIR) / str(signature_size)
            classic_path.mkdir(parents=True, exist_ok=True)

            classic_path /= datetime.now().strftime("%Y-%m-%d_%H:%M:%S.cobs_classic")
            cobs.classic_construct_list(doclist, str(classic_path), p)
