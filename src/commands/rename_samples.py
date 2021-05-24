import argparse

from wrappers.cobs import Cobs


def rename_samples(infile, classic_index_dir):
    mapping = {}

    with open(infile, 'r') as f:
        for line in f:
            line = line.strip()
            old, new = line.split('\t')
            mapping[old] = new
        cobs = Cobs(classic_index_dir)
        cobs.rename_samples(mapping)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile')
    parser.add_argument('--classic_index_dir')
    args = parser.parse_args()

    rename_samples(args.infile, args.classic_index_dir)
