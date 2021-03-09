from hypothesis.strategies import composite, integers, text, floats, from_regex

from wrappers.cobs import COBS_TERM_SIZE


@composite
def cobs_results(draw):
    return draw(integers()), draw(text())


@composite
def thresholds(draw):
    return draw(floats(allow_nan=False))


@composite
def seqs(draw):
    return draw(text(min_size=COBS_TERM_SIZE))


@composite
def snps(draw):
    return draw(text())


@composite
def positions(draw):
    return draw(integers())


@composite
def fasta_strings(draw):
    return draw(from_regex(r'^>')).encode()
