from hypothesis import given
from hypothesis.strategies import text

from test.strategies import snps, positions, fasta_strings
from wrappers.amino_acid_mutation_search import AminoAcidMutationSearch


class CobsMock:
    def __init__(self, mock_search_results=None):
        self.mock_search_results = mock_search_results if mock_search_results else []

    def search(self, _seq, threshold):
        return self.mock_search_results


@given(gene=text(), ref_path=text(), genbank_path=text(), ref=snps(), pos=positions(), alt=snps(), mock_probes=fasta_strings(), mock_genotypes=text())
def test_search(gene, ref_path, genbank_path, ref, pos, alt, mock_probes, mock_genotypes, monkeypatch):
    monkeypatch.setattr('wrappers.amino_acid_mutation_search.AminoAcidMutationSearch.create_variant_probe_set', lambda _x, var_name: mock_probes)
    monkeypatch.setattr('wrappers.variant_search.VariantSearch.genotype_alleles',
                        lambda _x, _y, _z: mock_genotypes)
    monkeypatch.setattr('wrappers.amino_acid_mutation_search.Fasta', lambda _: {})

    cobs = CobsMock()
    search_instance = AminoAcidMutationSearch(cobs, ref_path, genbank_path)

    result = search_instance.search(gene, ref, pos, alt)

    assert result['query'] == "_".join([gene, "".join([ref, str(pos), alt])])
    assert result['results'] == mock_genotypes