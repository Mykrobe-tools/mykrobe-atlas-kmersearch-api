from test.conftest import integration_test
from wrappers.cobs import Cobs


@integration_test
def test_building_indices():
    sample_paths = ['test/data/input/sample.kmer31.q5cleaned_8.ctx', 'test/data/input/sample.kmer31.q5cleaned_26.ctx']
    sample_names = ['a', 'b']

    cobs = Cobs()
    cobs.build(sample_paths, sample_names)

    cobs = Cobs()
    results = cobs.search('AGTCAACGCTAAGGCATTTCCCCCCTGCCTCCTGCCTGCTGCCAAGCCCT', 0.1)

    assert len(results) == 2