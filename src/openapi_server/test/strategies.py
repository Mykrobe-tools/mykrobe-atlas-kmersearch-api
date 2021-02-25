from hypothesis.strategies import composite, integers, text, floats

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
