from hypothesis import given
from hypothesis.strategies import lists, sets, text

from openapi_server.test.strategies import snps, positions, fasta_strings, cobs_results
from wrappers.variant_search import VariantSearch


class CobsMock:
    def __init__(self, mock_search_results=None):
        self.mock_search_results = mock_search_results if mock_search_results else []

    def search(self, _seq, threshold):
        return self.mock_search_results


@given(ref_seqs=lists(snps(), min_size=1), alt_seqs=lists(snps(), min_size=1), mock_search_results=lists(elements=cobs_results()))
def test_search_for_alleles(ref_seqs, alt_seqs, mock_search_results):
    cobs = CobsMock(mock_search_results)
    vs = VariantSearch(cobs)

    results = vs.search_for_alleles(ref_seqs, alt_seqs)

    assert results['ref'] == set([r[1] for r in mock_search_results])
    assert results['alt'] == set([r[1] for r in mock_search_results])


@given(ref_seqs=lists(snps()), alt_seqs=lists(snps()), mock_ref_samples=sets(text()), mock_alt_samples=sets(text()))
def test_genotype_alleles(ref_seqs, alt_seqs, mock_ref_samples, mock_alt_samples, monkeypatch):
    monkeypatch.setattr('wrappers.variant_search.VariantSearch.search_for_alleles',
                        lambda _x, _y, _z: {'ref': mock_ref_samples, 'alt': mock_alt_samples})

    cobs = CobsMock()
    vs = VariantSearch(cobs)

    results = vs.genotype_alleles(refs=ref_seqs, alts=alt_seqs)

    for r in results:
        if r['genotype'] == '0/1':
            assert r['sample_name'] in mock_ref_samples and r['sample_name'] in mock_alt_samples
        elif r['genotype'] == '0/0':
            assert r['sample_name'] in mock_ref_samples and r['sample_name'] not in mock_alt_samples
        elif r['genotype'] == '1/1':
            assert r['sample_name'] not in mock_ref_samples and r['sample_name'] in mock_alt_samples
        else:
            raise ValueError("shouldn't happen")


@given(ref=snps(), pos=positions(), alt=snps(), mock_probes=fasta_strings(), mock_genotypes=text())
def test_search(ref, pos, alt, mock_probes, mock_genotypes, monkeypatch):
    monkeypatch.setattr('wrappers.variant_search.VariantSearch.create_variant_probe_set', lambda _x, var_name: mock_probes)
    monkeypatch.setattr('wrappers.variant_search.VariantSearch.genotype_alleles',
                        lambda _x, _y, _z: mock_genotypes)
    monkeypatch.setattr('wrappers.variant_search.Fasta', lambda _: {})

    cobs = CobsMock()
    vs = VariantSearch(cobs)

    result = vs.search(ref, pos, alt)

    assert result['query'] == "".join([ref, str(pos), alt])
    assert result['results'] == mock_genotypes