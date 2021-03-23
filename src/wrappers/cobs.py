import subprocess
import tempfile
from datetime import datetime
from distutils.dir_util import copy_tree
from os import environ
from pathlib import Path
from tempfile import TemporaryDirectory

import cobs_index as cobs

COBS_CLASSIC_INDEXES_DIR = environ.get('COBS_CLASSIC_INDEXES_DIR', '/data/classic')
COBS_INDEX_PATH = environ.get('COBS_INDEX_PATH', '/data/combined.cobs_compact')
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
            setattr(p, 'continue', True)
            classic_path = Path(COBS_CLASSIC_INDEXES_DIR) / datetime.now().strftime("%Y-%m-%d_%H:%M:%S.cobs_classic")
            cobs.classic_construct_list(doclist, str(classic_path), p)

            # COBS' `compact-construct-combine` command doesn't accept the `keep_temporary` param, even though the real
            # function does, so we have to resort to making a temporary copy of the classic dir here
            try:
                with tempfile.TemporaryDirectory() as tmp_dir:
                    copy_tree(COBS_CLASSIC_INDEXES_DIR, tmp_dir)
                    subprocess.check_call(['cobs', 'compact-construct-combine', tmp_dir, COBS_INDEX_PATH])
            except FileNotFoundError as e:
                if tmp_dir not in str(e):
                    raise
                pass
