from pytest import fixture

from test.conftest import integration_test
from wrappers.cobs import Cobs


@fixture
def make_classic_index_dir(tmp_path):
    def _(existing_sig_sizes=None):
        if not existing_sig_sizes:
            existing_sig_sizes = [9000000, 10000000]

        classic_index_dir = tmp_path / 'classic'
        classic_index_dir.mkdir()

        for t in existing_sig_sizes:
            (classic_index_dir / str(t)).mkdir()

        return classic_index_dir

    return _


@integration_test
def test_building_indices(make_classic_index_dir):
    tmp_classic_index_dir = make_classic_index_dir()
    check_building_and_searching_test_data(str(tmp_classic_index_dir))


@integration_test
def test_creating_new_signature_size(make_classic_index_dir):
    tmp_classic_index_dir = make_classic_index_dir([1000])
    check_building_and_searching_test_data(str(tmp_classic_index_dir))


def check_building_and_searching_test_data(tmp_classic_index_dir):
    sample_paths = ['test/data/input/sample.kmer31.q5cleaned_8.ctx', 'test/data/input/sample.kmer31.q5cleaned_26.ctx']
    sample_names = ['a', 'b']

    cobs = Cobs(tmp_classic_index_dir)
    cobs.build(sample_paths, sample_names)

    cobs = Cobs(tmp_classic_index_dir)
    results = cobs.search('AGTCAACGCTAAGGCATTTCCCCCCTGCCTCCTGCCTGCTGCCAAGCCCT', 0.1)

    assert len(results) == 2