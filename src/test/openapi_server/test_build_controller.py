from hypothesis import given
from hypothesis.strategies import text, lists

from openapi_server.models import Samples
from test.strategies import sample_names


@given(path_to_file_list=text(), sample_names=lists(sample_names()))
def test_response(path_to_file_list, sample_names, build, monkeypatch):
    monkeypatch.setattr('openapi_server.controllers.build_controller.Cobs.build', lambda _x, _y: None)

    response = build(path_to_file_list, sample_names)

    assert response.status_code == 200

    added_samples = Samples.from_dict(response.json)
    for sample in added_samples.samples:
        assert sample.name in sample_names