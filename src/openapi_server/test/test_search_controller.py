from math import ceil

from hypothesis import given
from hypothesis.strategies import text, floats, lists, integers

from openapi_server.models import SearchResults
from openapi_server.test.strategies import cobs_results


class CobsMock:
    def __init__(self, mock_search_results):
        self.mock_search_results = mock_search_results

    def search(self, _seq, _threshold):
        return self.mock_search_results


@given(seq=text(min_size=1), threshold=floats(allow_nan=False), mock_search_results=lists(elements=cobs_results()), mock_term_size=integers(min_value=1))
def test_search(seq, threshold, mock_search_results, mock_term_size, search, monkeypatch):
    cobs_mock = CobsMock(mock_search_results)
    monkeypatch.setattr('openapi_server.controllers.search_controller.cobs', cobs_mock)
    monkeypatch.setattr('openapi_server.controllers.search_controller.COBS_TERM_SIZE', mock_term_size)

    response = search(seq, threshold)
    assert response.status_code == 200

    results = SearchResults.from_dict(response.json)
    assert results.query == seq
    assert results.threshold == threshold

    for i, result in enumerate(results.results):
        assert result.num_kmers == ceil(len(seq) / mock_term_size)
        assert result.num_kmers_found == mock_search_results[i][0]
        assert result.percent_kmers_found == result.num_kmers_found / result.num_kmers
        assert result.sample_name == mock_search_results[i][1]
