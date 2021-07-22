import argparse
import json

from wrappers.cobs import Cobs
from wrappers.variant_search import VariantSearch


def query(ref, pos, alt, classic_index_dir, ref_path):
    cobs = Cobs(classic_index_dir)
    variant_search = VariantSearch(cobs, ref_path)
    results = variant_search.search(ref, pos, alt)

    print(json.dumps(results))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('ref')
    parser.add_argument('pos')
    parser.add_argument('alt')
    parser.add_argument('classic_index_dir')
    parser.add_argument('ref_path')
    args = parser.parse_args()

    query(args.ref, args.pos, args.alt, args.classic_index_dir, args.ref_path)
