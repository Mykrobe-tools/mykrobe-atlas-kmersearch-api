from hypothesis import given
from hypothesis.strategies import lists, text

from openapi_server.models import SearchResults
from test.conftest import integration_test
from test.strategies import cobs_results, thresholds, seqs
from wrappers.cobs import COBS_TERM_SIZE


class CobsMock:
    def __init__(self, mock_search_results=None):
        self.mock_search_results = mock_search_results if mock_search_results else []

    def search(self, _seq, _threshold):
        return self.mock_search_results


@given(seq=seqs(), threshold=thresholds(), mock_search_results=lists(elements=cobs_results()))
def test_search_response(seq, threshold, mock_search_results, search, monkeypatch):
    monkeypatch.setattr('openapi_server.controllers.search_controller.get_cobs', lambda: CobsMock(mock_search_results))

    response = search(seq, threshold)
    assert response.status_code == 200, response.data

    results = SearchResults.from_dict(response.json)
    assert results.query == seq
    assert results.threshold == threshold

    for i, result in enumerate(results.results):
        assert result.num_kmers == len(seq) - COBS_TERM_SIZE + 1
        assert result.num_kmers_found == mock_search_results[i][0]
        assert result.percent_kmers_found == result.num_kmers_found / result.num_kmers
        assert result.sample_name == mock_search_results[i][1]


@given(seq=text(max_size=COBS_TERM_SIZE-1), threshold=thresholds())
def test_invalid_seq_lengths(seq, threshold, search, monkeypatch):
    monkeypatch.setattr('openapi_server.controllers.search_controller.get_cobs', lambda: CobsMock())

    response = search(seq, threshold)
    assert response.status_code == 400


@integration_test
def test_missing_threshold(search, monkeypatch):
    @given(seq=seqs())
    def _(seq):
        response = search(seq)
        assert response.status_code == 400

    _()


@integration_test
def test_integration(search):
    sample_names = ['a', 'b']

    response = search('AGTCAACGCTAAGGCATTTCCCCCCTGCCTCCTGCCTGCTGCCAAGCCCT', 0.1)
    assert response.status_code == 200

    results = SearchResults.from_dict(response.json)
    count = 0
    for result in results.results:
        assert result.num_kmers_found > 0
        assert result.sample_name in sample_names
        count += 1
    assert count > 0