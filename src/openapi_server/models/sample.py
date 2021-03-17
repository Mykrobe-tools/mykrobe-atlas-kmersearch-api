# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class Sample(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, name=None):  # noqa: E501
        """Sample - a model defined in OpenAPI

        :param name: The name of this Sample.  # noqa: E501
        :type name: str
        """
        self.openapi_types = {
            'name': str
        }

        self.attribute_map = {
            'name': 'name'
        }

        self._name = name

    @classmethod
    def from_dict(cls, dikt) -> 'Sample':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Sample of this Sample.  # noqa: E501
        :rtype: Sample
        """
        return util.deserialize_model(dikt, cls)

    @property
    def name(self):
        """Gets the name of this Sample.


        :return: The name of this Sample.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Sample.


        :param name: The name of this Sample.
        :type name: str
        """

        self._name = name
