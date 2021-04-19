from flask import g

from wrappers.amino_acid_mutation_search import AminoAcidMutationSearch
from wrappers.cobs import Cobs
from wrappers.variant_search import VariantSearch, TB_REF


def get_cobs():
    # Not caching cobs since index paths could be changed at any time
    return Cobs()


def get_variant_searcher():
    if 'variant_searcher' not in g:
        g.variant_searcher = VariantSearch(get_cobs())

    return g.variant_searcher


def get_amino_acid_mutation_searcher(genbank_path, ref_path=TB_REF):
    if 'amino_acid_mutation_searcher' not in g:
        g.amino_acid_mutation_searcher = AminoAcidMutationSearch(get_cobs(), ref_path, genbank_path)

    return g.amino_acid_mutation_searcher


def close_db():
    pass
