# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class SearchQuery(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, seq=None, threshold=None):  # noqa: E501
        """SearchQuery - a model defined in OpenAPI

        :param seq: The seq of this SearchQuery.  # noqa: E501
        :type seq: str
        :param threshold: The threshold of this SearchQuery.  # noqa: E501
        :type threshold: float
        """
        self.openapi_types = {
            'seq': str,
            'threshold': float
        }

        self.attribute_map = {
            'seq': 'seq',
            'threshold': 'threshold'
        }

        self._seq = seq
        self._threshold = threshold

    @classmethod
    def from_dict(cls, dikt) -> 'SearchQuery':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The SearchQuery of this SearchQuery.  # noqa: E501
        :rtype: SearchQuery
        """
        return util.deserialize_model(dikt, cls)

    @property
    def seq(self):
        """Gets the seq of this SearchQuery.


        :return: The seq of this SearchQuery.
        :rtype: str
        """
        return self._seq

    @seq.setter
    def seq(self, seq):
        """Sets the seq of this SearchQuery.


        :param seq: The seq of this SearchQuery.
        :type seq: str
        """
        if seq is not None and len(seq) < 31:
            raise ValueError("Invalid value for `seq`, length must be greater than or equal to `31`")  # noqa: E501

        self._seq = seq

    @property
    def threshold(self):
        """Gets the threshold of this SearchQuery.


        :return: The threshold of this SearchQuery.
        :rtype: float
        """
        return self._threshold

    @threshold.setter
    def threshold(self, threshold):
        """Sets the threshold of this SearchQuery.


        :param threshold: The threshold of this SearchQuery.
        :type threshold: float
        """

        self._threshold = threshold
