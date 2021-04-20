from wrappers.amino_acid_mutation_search import AminoAcidMutationSearch
from wrappers.cobs import Cobs
from wrappers.variant_search import VariantSearch, TB_REF


def get_cobs():
    # Not caching cobs since index paths could be changed at any time
    return Cobs()


def get_variant_searcher():
    return VariantSearch(get_cobs())


def get_amino_acid_mutation_searcher(genbank_path, ref_path=TB_REF):
    return AminoAcidMutationSearch(get_cobs(), ref_path, genbank_path)


def close_db():
    pass
