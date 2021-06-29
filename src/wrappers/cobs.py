import subprocess
from collections import defaultdict
from datetime import datetime
from os import environ
from pathlib import Path
from tempfile import TemporaryDirectory

import cobs_index as cobs

from utils.file import peek

COBS_CLASSIC_INDEXES_DIR = environ.get('COBS_CLASSIC_INDEXES_DIR', '/data/classic')
COBS_CLASSIC_FILE_EXTENSION = 'cobs_classic'
COBS_TERM_SIZE = 31
COBS_FALSE_POSITIVE_RATE = float(environ.get('COBS_FALSE_POSITIVE_RATE', 0.4))


class Cobs:
    def __init__(self, classic_index_dir=None):
        self.classic_index_dir = classic_index_dir or COBS_CLASSIC_INDEXES_DIR
        self.index_paths = []
        self.search_instances = []

        self.reconstruct_instances()

    def reconstruct_instances(self):
        self.index_paths = []
        for path in Path(self.classic_index_dir).iterdir():
            if path.is_dir():
                self.index_paths += [p for p in path.iterdir() if Cobs.is_classic_index(p)]
        self.search_instances = [cobs.Search(str(index_path)) for index_path in self.index_paths]

    def search(self, query, threshold):
        results = []

        for search_instance in self.search_instances:
            results += search_instance.search(query, threshold=threshold)

        flatten = []
        for r in results:
            flatten.append((r.score, r.doc_name))
        return flatten

    def build(self, sample_paths, sample_names, term_size=None, false_positive_rate=None, signature_size=0,
              keep_temporary=False, combine=True):
        """

        :param sample_paths:
        :param sample_names:
        :param term_size:
        :param false_positive_rate:
        :param signature_size: In vanilla COBS, the default value for this parameter is 0, but its default behaviour is
                                what we want to avoid. Therefore, we also set the default for this param in our function
                                to be 0, and handle that case our way, preventing vanilla COBS' default behaviour to
                                ever be triggered.
        :param keep_temporary:
        :param combine:
        :return:
        """

        assert len(sample_paths) == len(sample_names)

        p = cobs.ClassicIndexParameters()
        p.term_size = term_size or COBS_TERM_SIZE
        p.false_positive_rate = false_positive_rate or COBS_FALSE_POSITIVE_RATE
        p.signature_size = signature_size
        p.keep_temporary = keep_temporary
        setattr(p, 'continue', True)

        samples_by_sig_size = self.group_samples_by_signature_size(sample_paths, sample_names, p)
        self.build_new_indexes(samples_by_sig_size, p)
        if combine:
            self.combine_classic_indexes(p)

        self.reconstruct_instances()

    def group_samples_by_signature_size(self, sample_paths, sample_names, params):
        sig_sizes = sorted([int(x.name) for x in Path(self.classic_index_dir).iterdir() if x.is_dir() and x.name.isnumeric()])
        samples_by_sig_size = defaultdict(list)

        # cobs.DocumentEntry doesn't have a constructor, so the only way to construct one is to iterate a DocumentList
        with TemporaryDirectory() as tmpdir:
            doclist = cobs.DocumentList(tmpdir)
            for original_sample_path in sample_paths:
                doclist.add(original_sample_path.strip())

            for doc, name in zip(doclist, sample_names):
                if params.signature_size != 0:
                    correct_sig_size = params.signature_size
                    self.create_signature_size_dir(correct_sig_size)
                else:
                    signature_size = cobs.calc_signature_size(doc.num_terms(COBS_TERM_SIZE), params.num_hashes, params.false_positive_rate)

                    current_max_sig_size = sig_sizes[-1]
                    correct_sig_size = 0
                    if current_max_sig_size < signature_size:
                        new_sig_sizes = self.create_new_signature_thresholds(current_max_sig_size, signature_size)
                        correct_sig_size = new_sig_sizes[-1]
                        sig_sizes += new_sig_sizes
                    else:
                        for sig_size in sig_sizes:
                            if sig_size >= signature_size:
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
            combined_path = path / Cobs.generate_index_filename()

            classic_files = list(path.glob('*.' + COBS_CLASSIC_FILE_EXTENSION))
            if len(classic_files) > 1:
                # Not sure why using exposed Python function raised an IO error. Probably permission issue from tornado thread
                cmd = [
                    'cobs', 'classic-combine', str(path), str(path), combined_path,
                    '-m', str(params.mem_bytes),
                    '-T', str(params.num_threads),
                ]
                if params.keep_temporary:
                    cmd.append('--keep-temporary')
                subprocess.check_output(cmd)

                if not params.keep_temporary:
                    for file in classic_files:
                        file.unlink()
            elif len(classic_files) == 1:
                classic_files[0].rename(combined_path)

    def rename_samples(self, mapping):
        for index_path in self.index_paths:
            if not mapping:
                break

            new_path = index_path.parent / Cobs.generate_index_filename()

            with open(index_path, 'rb') as infile, open(new_path, 'wb') as outfile:
                # Rewrite the unchanged part (first 47 bytes) of the header
                outfile.write(infile.read(47))

                at_least_one_changed = False
                magic_word = 'CLASSIC_INDEX'
                ahead = peek(infile, len(magic_word))
                while ahead.decode() != magic_word:
                    sample_name = infile.readline().strip().decode()

                    if sample_name in mapping:
                        key = sample_name
                        sample_name = mapping[sample_name]
                        del mapping[key]

                        at_least_one_changed = True

                    outfile.write((sample_name + '\n').encode())

                    ahead = peek(infile, len(magic_word))

                if at_least_one_changed:
                    chunk_size = 4 * 1024 * 1024
                    data = infile.read(chunk_size)
                    while data != b'':
                        outfile.write(data)
                        data = infile.read(chunk_size)

            if at_least_one_changed:
                index_path.unlink()
            else:
                new_path.unlink()

        self.reconstruct_instances()

    @staticmethod
    def generate_index_filename():
        return datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + '.' + COBS_CLASSIC_FILE_EXTENSION

    @staticmethod
    def is_classic_index(path: Path):
        return path.is_file() and path.name.split('.')[-1] == COBS_CLASSIC_FILE_EXTENSION

    def create_new_signature_thresholds(self, current_max_sig_size, signature_size):
        new_sig_sizes = []

        while current_max_sig_size < signature_size:
            new_sig_size = 2 * current_max_sig_size
            self.create_signature_size_dir(new_sig_size)
            new_sig_sizes.append(new_sig_size)

            current_max_sig_size = new_sig_size

        return new_sig_sizes

    def create_signature_size_dir(self, signature_size):
        (Path(self.classic_index_dir) / str(signature_size)).mkdir(exist_ok=True)
