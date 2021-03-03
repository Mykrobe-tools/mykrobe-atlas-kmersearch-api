import itertools
import subprocess
import tempfile
from os import environ

from pyfasta import Fasta

from wrappers.cobs import COBS_TERM_SIZE

TB_REF = environ.get('TB_REF', '/data/NC_000962.3.fasta')


class VariantSearch:
    def __init__(self, cobs, reference_path=TB_REF):
        self.cobs = cobs
        self.reference_path = reference_path

    def search(self, ref_base, pos, alt_base):
        var_name = "".join([ref_base, str(pos), alt_base])
        fasta_string = self.create_variant_probe_set(var_name=var_name)
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
        return {"query": var_name, "results": self.genotype_alleles(refs, alts)}

    def create_variant_probe_set(self, var_name):
        fasta_string = subprocess.check_output(
            [
                "mykrobe",
                "variants",
                "make-probes",
                "-k",
                str(COBS_TERM_SIZE),
                "-v",
                var_name,
                self.reference_path,
            ]
        )
        return fasta_string

    def genotype_alleles(self, refs, alts):
        ref_alt_samples = self.search_for_alleles(refs, alts)
        results = []
        for sample_name in set(itertools.chain.from_iterable(ref_alt_samples.values())):
            if (
                sample_name in ref_alt_samples["ref"]
                and sample_name in ref_alt_samples["alt"]
            ):
                results.append({"sample_name": sample_name, "genotype": "0/1"})
            elif sample_name in ref_alt_samples["ref"]:
                results.append({"sample_name": sample_name, "genotype": "0/0"})
            elif sample_name in ref_alt_samples["alt"]:
                results.append({"sample_name": sample_name, "genotype": "1/1"})
        return results

    def search_for_alleles(self, ref_seqs, alt_seqs):
        results = {"ref": [], "alt": []}
        for ref in ref_seqs:
            res = self.cobs.search(ref, threshold=1)
            results["ref"].extend([r[1] for r in res])
        for alt in alt_seqs:
            res = self.cobs.search(alt, threshold=1)
            results["alt"].extend([r[1] for r in res])
        return results
