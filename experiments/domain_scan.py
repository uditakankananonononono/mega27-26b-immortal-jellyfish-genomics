"""Pfam domain verification of predicted proteins (pyhmmer vs Pfam-A).

For each predicted candidate protein, report significant domains (iE-value < 1e-5).
A candidate locus is DOMAIN-VERIFIED for its panel gene when it carries the gene's
expected diagnostic domain(s) (table below). This arbitrates the borderline
tblastn hits (e.g. TERT at 26% identity: true iff Reverse_transcriptase_2 /
Telomerase_RBD / TERT_ten domains land).
"""
import json, os, sys
import pyhmmer

EXPECTED = {
    "TERT": {"Reverse_transcriptase_2", "Telomerase_RBD", "TERT_ten", "Telomerase_reverse"},
    "POLD1": {"DNA_pol_delta_4", "DNA_pol_B_2", "DNA_pol_B_exo1", "DNA_pol_B_thumb", "DNA_pol_B"},
    "POLE": {"DNA_pol_B_exo1", "DNA_pol_B_2", "DNA_pol_B", "DNA_pol_B_thumb"},
    "POLD2": {"DNA_pol_delta_4", "PD40"},
    "RAD51": {"Rad51", "AAA", "Rad51_DUP"},
    "BRCA1": {"BRCT", "zf-RING_2", "RINGv"},
    "PARP1": {"PARP", "PARP_reg", "zf-PARP", "BRCT", "WGR"},
    "MLH1": {"MutL_C", "HATPase_c", "DNA_mis_repair"},
    "MSH2": {"MutS_III", "MutS_V", "MutS_II", "MutS_I", "DNA_mis_repair"},
    "FEN1": {"XPG_N", "XPG_I"},
    "DKC1": {"DKC1", "PUS_3", "Pseudouridine_synth"},
    "POT1": {"POT1", "POT1_2"},
    "TERF1": {"TERF1", "Myb_DNA-binding"},
    "TERF2": {"TERF2", "Myb_DNA-binding"},
    "ERCC1": {"ERCC1", "HhH-GPD"},
    "ERCC2": {"DEAD", "Helicase_C", "ERCC2"},
    "XRCC1": {"XRCC1_N", "BRCT", "XRCC1_2"},
    "XRCC5": {"Ku", "Ku80"},
    "LIG4": {"DNA_ligase_IV", "DNA_ligase_A_M", "BRCT"},
    "OGG1": {"OGG_N", "HhH-GPD", "Endonuclease_3"},
}
ALIASES = {"Telomerase_reverse": "Telomerase_RT"}

def scan(hmm_path, proteins, block=1000):
    with pyhmmer.easel.SequenceFile(proteins, digital=True) as sf:
        seqs = list(sf)
    def _nm(x):
        return x.decode() if isinstance(x, bytes) else x
    results = {_nm(s.name): [] for s in seqs}
    with pyhmmer.plan7.HMMFile(hmm_path) as hf:
        chunk = []
        def flush(chunk):
            if not chunk:
                return
            for hmm, hits in zip(chunk, pyhmmer.hmmsearch(chunk, seqs, cpus=2, E=1e-3)):
                fam = _nm(hmm.name)
                acc = hmm.accession.decode() if isinstance(hmm.accession, bytes) else (hmm.accession or "")
                for hit in hits:
                    if hit.included:
                        for d in hit.domains:
                            if d.i_evalue < 1e-5:
                                results[_nm(hit.name)].append(
                                    {"family": fam, "accession": acc,
                                     "iEvalue": d.i_evalue, "score": d.score,
                                     "env": [d.env_from, d.env_to]})
        n = 0
        for hmm in hf:
            chunk.append(hmm)
            n += 1
            if len(chunk) >= block:
                flush(chunk); chunk = []
                print("scanned", n, "HMMs", flush=True)
        flush(chunk)
    return results

def main():
    hmm_path = "/tmp/Pfam-A.hmm.gz"
    os.makedirs("data/proteins_all", exist_ok=True)
    import glob
    # concat all predicted proteins into one file
    with open("data/proteins_all/all.faa", "w") as out:
        for f in sorted(glob.glob("data/proteins/*.faa")):
            out.write(open(f).read())
    res = scan(hmm_path, "data/proteins_all/all.faa")
    verdicts = {}
    for qname, doms in res.items():
        genome, sym = qname.split("_", 1)[:2] if qname.count("_") >= 1 else (qname, "")
        # qname format: {genome}_{sym} but genome itself has no underscore; sym may not either
        genome, sym = qname.rsplit("_", 1)
        fams = {d["family"] for d in doms}
        exp = EXPECTED.get(sym, set())
        verified = bool(fams & exp)
        verdicts[qname] = {"genome": genome, "gene": sym, "domains": doms,
                           "expected_hit": sorted(fams & exp), "domain_verified": verified}
    json.dump(verdicts, open("results/domain_verification.json", "w"), indent=1)
    for genome in ("Tdohrnii", "TdohrniiOviedo", "Aaurita"):
        n = sum(1 for v in verdicts.values() if v["genome"] == genome and v["domain_verified"])
        tot = sum(1 for v in verdicts.values() if v["genome"] == genome)
        print(genome, f"{n}/{tot} domain-verified", flush=True)

if __name__ == "__main__":
    main()
