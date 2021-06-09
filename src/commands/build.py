import argparse

from wrappers.cobs import Cobs


def build(infile, classic_index_dir, term_size, false_positive_rate, signature_size, keep_temporary, combine):
    sample_names = []
    sample_paths = []

    with open(infile, 'r') as f:
        for line in f:
            line = line.strip()
            name, path = line.split('\t')
            sample_names.append(name)
            sample_paths.append(path)

        cobs = Cobs(classic_index_dir)
        cobs.build(sample_paths, sample_names, term_size, false_positive_rate, signature_size, keep_temporary, combine)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', help='Tab separated file of sample name => sample path')
    parser.add_argument('--classic_index_dir')
    parser.add_argument('--term_size', type=int)
    parser.add_argument('--false_positive_rate', type=float)
    parser.add_argument('--signature_size', type=int, default=0)
    parser.add_argument('--keep_temporary', action='store_true')
    parser.add_argument('--dont_combine', action='store_true')
    args = parser.parse_args()

    build(args.infile, args.classic_index_dir, args.term_size, args.false_positive_rate, args.signature_size,
          args.keep_temporary, not args.dont_combine)
