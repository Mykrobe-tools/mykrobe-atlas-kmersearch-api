# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server import util


class NewSamples(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, sample_paths=None, sample_names=None):  # noqa: E501
        """NewSamples - a model defined in OpenAPI

        :param sample_paths: The sample_paths of this NewSamples.  # noqa: E501
        :type sample_paths: List[str]
        :param sample_names: The sample_names of this NewSamples.  # noqa: E501
        :type sample_names: List[str]
        """
        self.openapi_types = {
            'sample_paths': List[str],
            'sample_names': List[str]
        }

        self.attribute_map = {
            'sample_paths': 'sample_paths',
            'sample_names': 'sample_names'
        }

        self._sample_paths = sample_paths
        self._sample_names = sample_names

    @classmethod
    def from_dict(cls, dikt) -> 'NewSamples':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The NewSamples of this NewSamples.  # noqa: E501
        :rtype: NewSamples
        """
        return util.deserialize_model(dikt, cls)

    @property
    def sample_paths(self):
        """Gets the sample_paths of this NewSamples.


        :return: The sample_paths of this NewSamples.
        :rtype: List[str]
        """
        return self._sample_paths

    @sample_paths.setter
    def sample_paths(self, sample_paths):
        """Sets the sample_paths of this NewSamples.


        :param sample_paths: The sample_paths of this NewSamples.
        :type sample_paths: List[str]
        """

        self._sample_paths = sample_paths

    @property
    def sample_names(self):
        """Gets the sample_names of this NewSamples.


        :return: The sample_names of this NewSamples.
        :rtype: List[str]
        """
        return self._sample_names

    @sample_names.setter
    def sample_names(self, sample_names):
        """Sets the sample_names of this NewSamples.


        :param sample_names: The sample_names of this NewSamples.
        :type sample_names: List[str]
        """

        self._sample_names = sample_names