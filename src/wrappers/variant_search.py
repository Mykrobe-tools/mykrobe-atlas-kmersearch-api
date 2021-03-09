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
        results.extend([{"sample_name": sample_name, "genotype": "1/1"} for sample_name in
                        ref_alt_samples["alt"].difference(ref_alt_samples["ref"])])
        results.extend([{"sample_name": sample_name, "genotype": "0/0"} for sample_name in
                        ref_alt_samples["ref"].difference(ref_alt_samples["alt"])])
        results.extend([{"sample_name": sample_name, "genotype": "0/1"} for sample_name in
                        ref_alt_samples["alt"].intersection(ref_alt_samples["ref"])])
        return results

    def search_for_alleles(self, ref_seqs, alt_seqs):
        results = {"ref": set(), "alt": set()}
        for ref in ref_seqs:
            res = self.cobs.search(ref, threshold=1)
            for _, sample_name in res:
                results['ref'].add(sample_name)
        for alt in alt_seqs:
            res = self.cobs.search(alt, threshold=1)
            for _, sample_name in res:
                results['alt'].add(sample_name)
        return results
