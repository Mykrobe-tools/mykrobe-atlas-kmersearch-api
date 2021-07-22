import argparse
import json

from wrappers.amino_acid_mutation_search import AminoAcidMutationSearch
from wrappers.cobs import Cobs


def query(gene, ref, pos, alt, classic_index_dir, ref_path, genbank):
    cobs = Cobs(classic_index_dir)
    variant_search = AminoAcidMutationSearch(cobs, ref_path, genbank)
    results = variant_search.search(gene, ref, pos, alt)

    print(json.dumps(results))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('gene')
    parser.add_argument('ref')
    parser.add_argument('pos')
    parser.add_argument('alt')
    parser.add_argument('classic_index_dir')
    parser.add_argument('ref_path')
    parser.add_argument('genbank')
    args = parser.parse_args()

    query(args.gene, args.ref, args.pos, args.alt, args.classic_index_dir, args.ref_path, args.genbank)
