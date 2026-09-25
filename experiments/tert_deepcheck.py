"""TERT deep-check: stitch + Pfam-scan EVERY strong TERT locus in all 3 genomes.
Distinguishes a true telomerase (Reverse_transcriptase_2 + Telomerase_RBD /
TERT_ten) from genomic RT noise (retrotransposons) and from wrong-domain loci.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from jellyfish.loci import cluster_loci, region_bounds
from jellyfish.predict import stitch
from Bio import SeqIO
import pyhmmer

FASTAS = {"Tdohrnii": "../data/genomes/GCA_027922465.2/ncbi_dataset/data/GCA_027922465.2/GCA_027922465.2_TUR_r2.0.1_genomic.fna",
          "TdohrniiOviedo": "../data/genomes/GCA_025167195.1/ncbi_dataset/data/GCA_025167195.1/GCA_025167195.1_ASM2516719v1_genomic.fna",
          "Aaurita": "../data/genomes/GCA_004194415.1/ncbi_dataset/data/GCA_004194415.1/GCA_004194415.1_ABSv1_genomic.fna"}
TERT_DOMAINS = {"Reverse_transcriptase_2", "Telomerase_RBD", "TERT_ten", "Telomere_mint"}

def main():
    hits = json.load(open("results/tblastn_hits.json"))
    out = {}
    # collect all TERT HSPs per genome, cluster
    for genome in FASTAS:
        hs = []
        for key, h in hits[genome].items():
            if isinstance(h, dict): continue
            if key.endswith("_TERT"):
                hs.extend(h)
        loci = cluster_loci(hs)
        strong = [l for l in loci if l["total_bits"] >= 100]
        idx = SeqIO.index(FASTAS[genome], "fasta")
        entries = []
        os.makedirs("data/tert_loci", exist_ok=True)
        for i, loc in enumerate(strong):
            lo, hi = region_bounds(loc)
            rec = idx[loc["contig"]]
            hi = min(hi, len(rec.seq))
            seq = str(rec.seq[lo-1:hi])
            locus_hsps = [x for x in hs if x["contig"] == loc["contig"]
                          and min(x["sstart"], x["send"]) <= loc["end"]
                          and max(x["sstart"], x["send"]) >= loc["start"]]
            pred = stitch(locus_hsps, seq, lo)
            if not pred or len(pred["protein"]) < 30:
                continue
            name = f"{genome}_TERTloc{i}_{loc['contig']}"
            fn = f"data/tert_loci/{name}.faa"
            with open(fn, "w") as fh:
                fh.write(f">{name}\n{pred['protein']}\n")
            entries.append({"name": name, "contig": loc["contig"],
                            "bits": loc["total_bits"], "aa_len": len(pred["protein"])})
        out[genome] = entries
        print(genome, len(entries), "TERT locus proteins", flush=True)
    # one combined faa for scanning
    with open("data/tert_loci/all.faa", "w") as fh:
        import glob
        for f in sorted(glob.glob("data/tert_loci/*.faa")):
            if f.endswith("all.faa"): continue
            fh.write(open(f).read())
    # chunked hmmsearch (same as domain_scan)
    with pyhmmer.easel.SequenceFile("data/tert_loci/all.faa", digital=True) as sf:
        seqs = list(sf)
    results = { (s.name.decode() if isinstance(s.name, bytes) else s.name): [] for s in seqs }
    with pyhmmer.plan7.HMMFile("/tmp/Pfam-A.hmm.gz") as hf:
        chunk = []
        def flush(chunk):
            if not chunk: return
            for hmm, hh in zip(chunk, pyhmmer.hmmsearch(chunk, seqs, cpus=2, E=1e-3)):
                fam = hmm.name.decode() if isinstance(hmm.name, bytes) else hmm.name
                for hit in hh:
                    if hit.included:
                        for d in hit.domains:
                            if d.i_evalue < 1e-5:
                                nm = hit.name.decode() if isinstance(hit.name, bytes) else hit.name
                                results[nm].append({"family": fam, "iEvalue": d.i_evalue, "env": [d.env_from, d.env_to]})
        for hmm in hf:
            chunk.append(hmm)
            if len(chunk) >= 2000:
                flush(chunk); chunk = []
        flush(chunk)
    for genome, entries in out.items():
        for e in entries:
            doms = results.get(e["name"], [])
            e["families"] = sorted({d["family"] for d in doms})
            e["tert_domains"] = sorted({d["family"] for d in doms} & TERT_DOMAINS)
            e["is_telomerase"] = bool(e["tert_domains"])
    json.dump(out, open("results/tert_deepcheck.json", "w"), indent=1)
    for genome, entries in out.items():
        t = [e for e in entries if e["is_telomerase"]]
        print(genome, "TELOMERASE-DOMAIN loci:", [(e["name"], e["tert_domains"]) for e in t], flush=True)

if __name__ == "__main__":
    main()
