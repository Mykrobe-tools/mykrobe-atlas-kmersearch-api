from flask import g

from wrappers.cobs import Cobs
from wrappers.variant_search import VariantSearch


def get_cobs():
    if 'cobs' not in g:
        g.cobs = Cobs()

    return g.cobs


def get_variant_searcher():
    if 'vs' not in g:
        g.vs = VariantSearch(get_cobs())

    return g.vs


def close_db():
    pass
