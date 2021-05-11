import logging
from os import environ

import pytest
from hypothesis import settings, HealthCheck
from pytest import fixture

from openapi_server.factories.app import create_app


@fixture
def app():
    logging.getLogger('connexion.operation').setLevel('ERROR')
    app = create_app()

    return app


@fixture
def client(app):
    return app.app.test_client()


@fixture
def make_request(client):
    def _(path, method, json=None, ensure=False, success_code=200, query_params=None):
        response = client.open(path=path, method=method, json=json, query_string=query_params)
        if ensure:
            assert response.status_code == success_code, response.data.decode()
        return response
    return _


@fixture
def search(make_request):
    def _(seq, threshold, *args, **kwargs):
        return make_request(f'/api/v1/search', 'POST', json={
            'seq': seq,
            'threshold': threshold,
        }, *args, **kwargs)

    return _


@fixture
def variant_search(make_request):
    def _(ref, pos, alt, gene=None, genbank=None, *args, **kwargs):
        body = {
            'ref': ref,
            'pos': pos,
            'alt': alt,
        }

        if gene and genbank:
            body['gene'] = gene
            body['genbank'] = genbank

        return make_request(f'/api/v1/variant_search', 'POST', json=body, *args, **kwargs)

    return _


@fixture
def build(make_request):
    def _(sample_paths, sample_names, *args, **kwargs):
        return make_request(f'/api/v1/build', 'POST', json={
            'sample_paths': sample_paths,
            'sample_names': sample_names,
        }, *args, **kwargs)

    return _


INTEGRATION_TEST = environ.get('INTEGRATION_TEST') == 'true'
integration_test = pytest.mark.skipif(not INTEGRATION_TEST, reason='not running integration tests')


settings.register_profile('default', suppress_health_check=(HealthCheck.function_scoped_fixture,))
settings.load_profile('default')
