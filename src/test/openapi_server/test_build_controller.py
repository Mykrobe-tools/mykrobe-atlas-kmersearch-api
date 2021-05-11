from hypothesis import given
from hypothesis.strategies import text, lists

from openapi_server.models import Samples
from test.conftest import integration_test
from test.strategies import sample_names


@given(sample_paths=lists(text()), sample_names=lists(sample_names()))
def test_response(sample_paths, sample_names, build, monkeypatch):
    monkeypatch.setattr('wrappers.cobs.Cobs.build', lambda _x, _y, _z: None)

    response = build(sample_paths, sample_names)

    assert response.status_code == 200

    added_samples = Samples.from_dict(response.json)
    for sample in added_samples.samples:
        assert sample.name in sample_names


@integration_test
def test_integration(build):
    sample_paths = ['test/data/input/sample.kmer31.q5cleaned_8.ctx', 'test/data/input/sample.kmer31.q5cleaned_26.ctx']
    sample_names = ['a', 'b']

    response = build(sample_paths, sample_names)

    assert response.status_code == 200