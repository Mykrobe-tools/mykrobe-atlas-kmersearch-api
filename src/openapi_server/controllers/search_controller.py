import connexion

from openapi_server.models import SearchResult
from openapi_server.models.search_query import SearchQuery  # noqa: E501
from openapi_server.models.search_results import SearchResults  # noqa: E501
from wrappers import cobs


def search_post(search_query=None):  # noqa: E501
    """search_post

     # noqa: E501

    :param search_query: 
    :type search_query: dict | bytes

    :rtype: SearchResults
    """
    if connexion.request.is_json:
        search_query = SearchQuery.from_dict(connexion.request.get_json())  # noqa: E501

    results = cobs.search(search_query.seq, search_query.threshold)

    return SearchResults(
        query=search_query.seq,
        threshold=search_query.threshold,
        results=[SearchResult(
            num_kmers_found=occurrences,
            sample_name=doc) for occurrences, doc in results]
    )
