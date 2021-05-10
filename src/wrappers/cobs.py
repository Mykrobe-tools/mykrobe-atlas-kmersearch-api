import subprocess
from collections import defaultdict
from datetime import datetime
from os import environ
from pathlib import Path
from tempfile import TemporaryDirectory

import cobs_index as cobs

COBS_CLASSIC_INDEXES_DIR = environ.get('COBS_CLASSIC_INDEXES_DIR', '/data/classic')
COBS_CLASSIC_FILE_EXTENSION = 'cobs_classic'
COBS_TERM_SIZE = 31
COBS_FALSE_POSITIVE_RATE = float(environ.get('COBS_FALSE_POSITIVE_RATE', 0.4))


class Cobs:
    def __init__(self, classic_index_dir=COBS_CLASSIC_INDEXES_DIR):
        self.classic_index_dir = classic_index_dir

        index_paths = []
        for path in Path(self.classic_index_dir).iterdir():
            if path.is_dir():
                index_paths += [p for p in path.iterdir() if Cobs.is_classic_index(p)]
        self.search_instances = [cobs.Search(str(index_path)) for index_path in index_paths]

    def search(self, query, threshold):
        results = []

        for search_instance in self.search_instances:
            results += search_instance.search(query, threshold=threshold)

        flatten = []
        for r in results:
            flatten.append((r.score, r.doc_name))
        return flatten

    def build(self, sample_paths, sample_names):
        assert len(sample_paths) == len(sample_names)

        p = cobs.ClassicIndexParameters()
        p.term_size = COBS_TERM_SIZE
        p.false_positive_rate = COBS_FALSE_POSITIVE_RATE
        setattr(p, 'continue', True)

        samples_by_sig_size = self.group_samples_by_signature_size(sample_paths, sample_names, p)
        self.build_new_indexes(samples_by_sig_size, p)
        self.combine_classic_indexes(p)

    def group_samples_by_signature_size(self, sample_paths, sample_names, params):
        sig_sizes = sorted([int(x.name) for x in Path(self.classic_index_dir).iterdir() if x.is_dir() and x.name.isnumeric()])
        samples_by_sig_size = defaultdict(list)

        # cobs.DocumentEntry doesn't have a constructor, so the only way to construct one is to iterate a DocumentList
        with TemporaryDirectory() as tmpdir:
            doclist = cobs.DocumentList(tmpdir)
            for original_sample_path in sample_paths:
                doclist.add(original_sample_path.strip())

            for doc, name in zip(doclist, sample_names):
                signature_size = cobs.calc_signature_size(doc.num_terms(COBS_TERM_SIZE), params.num_hashes, params.false_positive_rate)

                current_max_sig_size = sig_sizes[-1]
                correct_sig_size = 0
                if current_max_sig_size <= signature_size:
                    new_sig_size = 2 * current_max_sig_size

                    self.create_new_signature_threshold(new_sig_size)
                    correct_sig_size = new_sig_size

                    sig_sizes.append(new_sig_size)
                else:
                    for sig_size in sig_sizes:
                        if sig_size > signature_size:
                            correct_sig_size = sig_size
                            break

                sample = {'path': doc.path, 'name': name}
                samples_by_sig_size[correct_sig_size].append(sample)

        return samples_by_sig_size

    def build_new_indexes(self, samples_by_sig_size, params):
        for sig_size, samples in samples_by_sig_size.items():
            params.signature_size = sig_size

            with TemporaryDirectory() as tmpdir:
                doclist = cobs.DocumentList(tmpdir)
                for sample in samples:
                    doclist.add(sample['path'])

                for i, doc in enumerate(doclist):
                    doc.name = samples[i]['name']

                classic_path = Path(self.classic_index_dir) / str(sig_size)
                cobs.classic_construct_from_documents(doclist, str(classic_path), params)

    def combine_classic_indexes(self, params):
        for path in Path(self.classic_index_dir).iterdir():
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

    @staticmethod
    def is_classic_index(path: Path):
        return path.is_file() and path.name.split('.')[-1] == COBS_CLASSIC_FILE_EXTENSION

    def create_new_signature_threshold(self, new_sig_size):
        (Path(self.classic_index_dir) / str(new_sig_size)).mkdir()
