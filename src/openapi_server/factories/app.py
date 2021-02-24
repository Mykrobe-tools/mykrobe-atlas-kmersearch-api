import connexion
from openapi_server.error_handlers import internal_server_error_handler
from werkzeug.exceptions import InternalServerError

from openapi_server import encoder


def create_app():
    app = connexion.App(__name__, specification_dir='../openapi/')
    app.app.json_encoder = encoder.JSONEncoder

    app.add_api('openapi.yaml', arguments={'title': 'K-mer Search API'})

    app.add_error_handler(InternalServerError, internal_server_error_handler)

    return app