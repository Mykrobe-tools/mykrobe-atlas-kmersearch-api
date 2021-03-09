#!/usr/bin/env python3
from os import environ

from openapi_server.factories.app import create_app

DEBUG = bool(int(environ.get('DEBUG', '0')))


def main():
    app = create_app()

    app.run(port=8000, server='tornado' if not DEBUG else None, debug=DEBUG)


if __name__ == '__main__':
    main()
