from hypothesis.strategies import composite, integers, text


@composite
def cobs_results(draw):
    return draw(integers()), draw(text())
