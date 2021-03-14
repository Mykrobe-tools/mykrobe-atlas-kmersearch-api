import connexion

from openapi_server.db import get_variant_searcher, get_amino_acid_mutation_searcher
from openapi_server.models import VariantSearchResults
from openapi_server.models.variant_search_query import VariantSearchQuery  # noqa: E501


def variant_search_post(variant_search_query=None):  # noqa: E501
    """variant_search_post

     # noqa: E501

    :param variant_search_query: 
    :type variant_search_query: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        variant_search_query = VariantSearchQuery.from_dict(connexion.request.get_json())  # noqa: E501

    if variant_search_query.gene and variant_search_query.genbank:
        search_instance = get_amino_acid_mutation_searcher(variant_search_query.genbank)
        results = search_instance.search(variant_search_query.gene, variant_search_query.ref, variant_search_query.pos, variant_search_query.alt)
    else:
        search_instance = get_variant_searcher()
        results = search_instance.search(variant_search_query.ref, variant_search_query.pos, variant_search_query.alt)

    return VariantSearchResults.from_dict(results)
