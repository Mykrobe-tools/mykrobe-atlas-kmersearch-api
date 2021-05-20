from pathlib import Path
from time import sleep

from pytest import fixture

from test.conftest import integration_test
from wrappers.cobs import Cobs


SAMPLE_PATHS = ['test/data/input/sample.kmer31.q5cleaned_8.ctx', 'test/data/input/sample.kmer31.q5cleaned_26.ctx']
TEST_QUERY = 'AGTCAACGCTAAGGCATTTCCCCCCTGCCTCCTGCCTGCTGCCAAGCCCT'


@fixture(scope='session')
def built_classic_dir():
    classic_dir = Path('/data/classic')

    sample_paths = SAMPLE_PATHS
    sample_names = ['a', 'b']

    cobs = Cobs(classic_dir)
    cobs.build(sample_paths, sample_names)

    return classic_dir


@integration_test
def test_creating_new_signature_sizes(tmp_path):
    classic_index_dir = tmp_path / 'classic'
    classic_index_dir.mkdir()
    (classic_index_dir / '1000').mkdir()

    sample_paths = SAMPLE_PATHS
    sample_names = ['a', 'b']

    cobs = Cobs(classic_index_dir)
    cobs.build(sample_paths, sample_names)

    assert len(list(classic_index_dir.glob('*'))) == 15


@integration_test
def test_renaming_samples(built_classic_dir):
    sleep(1)  # so that the generated-from-timestamp new index filename will be different
    cobs = Cobs(built_classic_dir)
    cobs.rename_samples({'a': 'x'})

    results = cobs.search(TEST_QUERY, 0.1)
    samples = [y for x, y in results]

    assert 'x' in samples
