# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from openapi_server.models.base_model_ import Model
from openapi_server.models.sample import Sample
from openapi_server import util

from openapi_server.models.sample import Sample  # noqa: E501

class Samples(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, samples=None):  # noqa: E501
        """Samples - a model defined in OpenAPI

        :param samples: The samples of this Samples.  # noqa: E501
        :type samples: List[Sample]
        """
        self.openapi_types = {
            'samples': List[Sample]
        }

        self.attribute_map = {
            'samples': 'samples'
        }

        self._samples = samples

    @classmethod
    def from_dict(cls, dikt) -> 'Samples':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Samples of this Samples.  # noqa: E501
        :rtype: Samples
        """
        return util.deserialize_model(dikt, cls)

    @property
    def samples(self):
        """Gets the samples of this Samples.


        :return: The samples of this Samples.
        :rtype: List[Sample]
        """
        return self._samples

    @samples.setter
    def samples(self, samples):
        """Sets the samples of this Samples.


        :param samples: The samples of this Samples.
        :type samples: List[Sample]
        """

        self._samples = samples
