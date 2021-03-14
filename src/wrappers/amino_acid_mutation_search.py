import subprocess
import tempfile

from pyfasta import Fasta

from wrappers.cobs import COBS_TERM_SIZE
from wrappers.variant_search import VariantSearch


class AminoAcidMutationSearch(VariantSearch):
    def __init__(self, cobs, reference, genbank):
        super().__init__(cobs, reference)
        self.genbank = genbank

    def create_variant_probe_set(self, var_name):
        ### Run mykrobe variants make-probes  -v G100T ../mykrobe-atlas-cli/src/mykrobe/data/NC_000962.3.fasta
        fasta_string = subprocess.check_output(
            [
                "mykrobe",
                "variants",
                "make-probes",
                "-k",
                str(COBS_TERM_SIZE),
                "-v",
                var_name,
                "-g",
                self.genbank,
                self.reference_path,
            ]
        )
        return fasta_string

    def search(self, gene, ref, pos, alt):
        mut_name = "".join([ref, str(pos), alt])
        gene_mut_name = "_".join([gene, mut_name])

        fasta_string = self.create_variant_probe_set(var_name=gene_mut_name)
        with tempfile.NamedTemporaryFile() as fp:
            fp.write(fasta_string)
            fp.seek(0)
            fasta = Fasta(fp.name)
        refs = []
        alts = []
        for k, v in fasta.items():
            if "ref" in k:
                refs.append(str(v))
            else:
                alts.append(str(v))
        return {"query": gene_mut_name, "results": self.genotype_alleles(refs, alts)}