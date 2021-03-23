import connexion

from openapi_server.models import Sample
from openapi_server.models.new_samples import NewSamples  # noqa: E501
from openapi_server.models.samples import Samples  # noqa: E501
from wrappers.cobs import Cobs


def build_post(new_samples=None):  # noqa: E501
    """build_post

     # noqa: E501

    :param new_samples: 
    :type new_samples: dict | bytes

    :rtype: Samples
    """
    if connexion.request.is_json:
        new_samples = NewSamples.from_dict(connexion.request.get_json())  # noqa: E501

    Cobs.build(new_samples.sample_paths, new_samples.sample_names)

    return Samples([
        Sample(name=name) for name in new_samples.sample_names
    ])
