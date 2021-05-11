from hypothesis import given
from hypothesis.strategies import dictionaries, text

from openapi_server.models import VariantSearchResults
from test.conftest import integration_test
from test.strategies import snps, positions


class CobsMock:
    pass


class VariantSearcherMock:
    def __init__(self, mock_search_results=None):
        self.mock_search_results = mock_search_results if mock_search_results else {}

    def search(self, _ref, _pos, _alt):
        return self.mock_search_results


class AminoAcidMutationSearcherMock:
    def __init__(self, mock_search_results=None):
        self.mock_search_results = mock_search_results if mock_search_results else {}

    def search(self, _gene, _ref, _pos, _alt):
        return self.mock_search_results


@given(ref=snps(), pos=positions(), alt=snps(), mock_search_results=dictionaries(text(), text()))
def test_variant_search_response(ref, pos, alt, mock_search_results, variant_search, monkeypatch):
    monkeypatch.setattr('openapi_server.controllers.variant_search_controller.get_variant_searcher', lambda: VariantSearcherMock(mock_search_results))

    response = variant_search(ref, pos, alt)
    assert response.status_code == 200
    assert VariantSearchResults.from_dict(response.json) == VariantSearchResults.from_dict(mock_search_results)


@given(gene=text(min_size=1), genbank=text(min_size=1), ref=snps(), pos=positions(), alt=snps(), mock_search_results=dictionaries(text(), text()))
def test_amino_acid_mutation_search_response(gene, genbank, ref, pos, alt, mock_search_results, variant_search, monkeypatch):
    monkeypatch.setattr('openapi_server.db.get_cobs', lambda: CobsMock())
    monkeypatch.setattr('openapi_server.controllers.variant_search_controller.get_amino_acid_mutation_searcher',
                        lambda _: AminoAcidMutationSearcherMock(mock_search_results))

    response = variant_search(ref, pos, alt, gene, genbank)
    assert response.status_code == 200
    assert VariantSearchResults.from_dict(response.json) == VariantSearchResults.from_dict(mock_search_results)


@integration_test
def test_integration(search, build):
    sample_paths = ['test/data/input/sample.kmer31.q5cleaned_8.ctx', 'test/data/input/sample.kmer31.q5cleaned_26.ctx']
    sample_names = ['a', 'b']
    build(sample_paths, sample_names)

    response = search('AGTCAACGCTAAGGCATTTCCCCCCTGCCTCCTGCCTGCTGCCAAGCCCT', 0.1)
    assert response.status_code == 200

    results = VariantSearchResults.from_dict(response.json)
    count = 0
    for _ in results.results:
        count += 1
    assert count > 0