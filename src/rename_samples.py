import click

from wrappers.cobs import Cobs


@click.command()
@click.argument('infile', type=click.File('r'))
def rename_samples(infile):
    mapping = {}

    lines = infile.readlines()
    for line in lines:
        line = line.strip()
        old, new = line.split('\t')
        mapping[old] = new

    cobs = Cobs()
    cobs.rename_samples(mapping)


if __name__ == '__main__':
    rename_samples()
