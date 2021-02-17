# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from openapi_server.models.search_query import SearchQuery  # noqa: E501
from openapi_server.models.search_results import SearchResults  # noqa: E501
from openapi_server.test import BaseTestCase


class TestSearchController(BaseTestCase):
    """SearchController integration test stubs"""

    def test_search_post(self):
        """Test case for search_post

        
        """
        search_query = {
  "threshold" : 0.8008281904610115,
  "seq" : "seq"
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/search',
            method='POST',
            headers=headers,
            data=json.dumps(search_query),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
