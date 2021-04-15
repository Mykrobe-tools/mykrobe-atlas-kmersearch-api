import shutil
import subprocess
from datetime import datetime
from os import environ
from pathlib import Path
from tempfile import TemporaryDirectory

import cobs_index as cobs

COBS_CLASSIC_INDEXES_DIR = environ.get('COBS_CLASSIC_INDEXES_DIR', '/data/classic')
COBS_SAMPLE_DIR = environ.get('COBS_SAMPLE_DIR', '/data/samples')
COBS_CLASSIC_FILE_EXTENSION = 'cobs_classic'
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

        p = cobs.ClassicIndexParameters()
        p.term_size = COBS_TERM_SIZE
        p.false_positive_rate = COBS_POSITIVE_RATE
        setattr(p, 'continue', True)

        Cobs.group_samples_by_signature_size(sample_paths, sample_names, p)
        Cobs.build_new_indexes(p)
        Cobs.combine_classic_indexes(p)

        for sample_dir in Path(COBS_SAMPLE_DIR).iterdir():
            for sample in sample_dir.glob('*'):
                sample.unlink()

    @staticmethod
    def group_samples_by_signature_size(sample_paths, sample_names, params):
        # cobs.DocumentEntry doesn't have a constructor, so the only way to construct one is to iterate a DocumentList
        with TemporaryDirectory() as tmpdir:
            doclist = cobs.DocumentList(tmpdir)
            for original_sample_path in sample_paths:
                doclist.add(original_sample_path.strip())

            # Copy sample file to the group with the smallest signature size that is larger than its own
            for doc, name in zip(doclist, sample_names):
                signature_size = cobs.calc_signature_size(doc.num_terms(COBS_TERM_SIZE), params.num_hashes, params.false_positive_rate)

                sorted_subdirs = sorted([int(x.name) for x in Path(COBS_SAMPLE_DIR).iterdir()])
                sorted_subdirs = [Path(COBS_SAMPLE_DIR) / str(x) for x in sorted_subdirs]

                for index_dir in sorted_subdirs:
                    if index_dir.is_dir() and int(index_dir.name) > signature_size:
                        file_extension = doc.path.split('.')[-1]
                        new_sample_path = index_dir / (name + '.' + file_extension)
                        shutil.copyfile(doc.path, new_sample_path)
                        break

    @staticmethod
    def build_new_indexes(params):
        for sample_dir in Path(COBS_SAMPLE_DIR).iterdir():
            doclist = cobs.DocumentList(str(sample_dir))
            for doc in doclist:
                doc.name = Path(doc.path).name.split('.')[-2]

            classic_path = Path(COBS_CLASSIC_INDEXES_DIR) / sample_dir.name / (datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + '.' + COBS_CLASSIC_FILE_EXTENSION)
            cobs.classic_construct_list(doclist, str(classic_path), params)

    @staticmethod
    def combine_classic_indexes(params):
        for path in Path(COBS_CLASSIC_INDEXES_DIR).iterdir():
            classic_files = list(path.glob('*.' + COBS_CLASSIC_FILE_EXTENSION))
            if len(classic_files) > 1:
                combined_path = path / (datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + '.' + COBS_CLASSIC_FILE_EXTENSION)

                # Not sure why using exposed Python function raised an IO error. Probably permission issue from tornado thread
                subprocess.check_output([
                    'cobs', 'classic-combine', str(path), str(path), combined_path,
                    '-m', str(params.mem_bytes),
                    '-T', str(params.num_threads),
                    '--keep-temporary',
                ])

                for file in classic_files:
                    file.unlink()