import connexion
import six

from openapi_server.models.search_query import SearchQuery  # noqa: E501
from openapi_server.models.search_results import SearchResults  # noqa: E501
from openapi_server import util


def search_post(search_query):  # noqa: E501
    """search_post

     # noqa: E501

    :param search_query: 
    :type search_query: dict | bytes

    :rtype: SearchResults
    """
    if connexion.request.is_json:
        search_query = SearchQuery.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
