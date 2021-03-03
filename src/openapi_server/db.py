from flask import g

from wrappers.cobs import Cobs


def get_cobs():
    if 'cobs' not in g:
        g.cobs = Cobs()

    return g.cobs


def close_db():
    pass
