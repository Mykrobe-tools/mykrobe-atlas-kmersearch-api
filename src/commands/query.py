import argparse

from wrappers.cobs import Cobs


def query(q, threshold, classic_index_dir):
    cobs = Cobs(classic_index_dir)
    results = cobs.search(q, threshold)

    for score, doc_name in results:
        print(doc_name, score)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('query')
    parser.add_argument('threshold', type=float)
    parser.add_argument('classic_index_dir')
    args = parser.parse_args()

    query(args.query, args.threshold, args.classic_index_dir)