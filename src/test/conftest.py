import logging

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
    def _(ref, pos, alt, *args, **kwargs):
        return make_request(f'/api/v1/variant_search', 'POST', json={
            'ref': ref,
            'pos': pos,
            'alt': alt,
        }, *args, **kwargs)

    return _


settings.register_profile('default', suppress_health_check=(HealthCheck.function_scoped_fixture,))
settings.load_profile('default')
