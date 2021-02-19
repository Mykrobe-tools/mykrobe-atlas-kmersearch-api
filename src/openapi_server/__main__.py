#!/usr/bin/env python3
from os import environ

import connexion

from openapi_server import encoder


DEBUG = bool(int(environ.get('DEBUG', '0')))


def main():
    app = connexion.App(__name__, specification_dir='./openapi/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml',
                arguments={'title': 'K-mer Search API'},
                pythonic_params=True)

    app.run(port=8000, server='tornado' if not DEBUG else None, debug=DEBUG)


if __name__ == '__main__':
    main()
