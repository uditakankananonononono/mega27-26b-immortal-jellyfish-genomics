"""Upstream regulatory motif analysis for verified loci + the TERT locus.

Per genome: extract 2 kb upstream (strand-aware) of each verified gene locus,
compute k-mer enrichment (z-scores) vs a random genomic background, then
compare T. dohrnii vs A. aurita: k-mers enriched (z>=3) upstream of the SAME
gene in both species = candidate conserved regulatory motifs.
"""
import json, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from jellyfish.motifs import enrichment, tfbs_counts
from jellyfish.predict import revcomp
from Bio import SeqIO

FASTAS = {"Tdohrnii": "../data/genomes/GCA_027922465.2/ncbi_dataset/data/GCA_027922465.2/GCA_027922465.2_TUR_r2.0.1_genomic.fna",
          "Aaurita": "../data/genomes/GCA_004194415.1/ncbi_dataset/data/GCA_004194415.1/GCA_004194415.1_ABSv1_genomic.fna"}
VERIFIED = {"Tdohrnii": ["DKC1","ERCC1","LIG4","MLH1","MSH2","POLD1","POT1","RAD51","XRCC1"],
            "Aaurita": ["DKC1","ERCC1","LIG4","MLH1","MSH2","POLD1","POT1","RAD51"]}
UP = 2000
random.seed(27)

def upstream_seq(idx, contig, start, end, strand, contig_len):
    if strand == "+":
        lo = max(1, start - UP)
        s = str(idx[contig].seq[lo-1:start-1])
    else:
        hi = min(contig_len, end + UP)
        s = revcomp(str(idx[contig].seq[end:hi]))
    return s

def main():
    ledger = json.load(open("results/locus_ledger.json"))
    out = {}
    for genome, genes in VERIFIED.items():
        idx = SeqIO.index(FASTAS[genome], "fasta")
        # background: 150 random 2kb windows from random contigs
        contigs = list(idx.keys())
        bg = []
        tries = 0
        while len(bg) < 150 and tries < 3000:
            tries += 1
            c = random.choice(contigs)
            L = len(idx[c].seq)
            if L < 10000:
                continue
            i = random.randint(0, L - UP - 1)
            bg.append(str(idx[c].seq[i:i+UP]))
        out[genome] = {}
        upseqs = {}
        for gene in genes:
            strong = ledger[genome].get(gene, {}).get("strong_loci", [])
            if not strong:
                continue
            top = strong[0]
            L = len(idx[top["contig"]].seq)
            s = upstream_seq(idx, top["contig"], top["start"], top["end"], top["strand"], L)
            if len(s) < 500:
                continue
            upseqs[gene] = s
            res = enrichment([s], bg, k=6, window=50)
            top_kmers = sorted(res.items(), key=lambda kv: -kv[1]["z"])[:15]
            out[genome][gene] = {"upstream_len": len(s),
                                 "top_kmers": [(k, v["z"]) for k, v in top_kmers],
                                 "tfbs": tfbs_counts(s)}
        json.dump(upseqs, open(f"data/upstream_{genome}.json", "w"))
        print(genome, len(out[genome]), "upstream regions", flush=True)
    json.dump(out, open("results/upstream_motifs.json", "w"), indent=1)
    # cross-species shared enriched kmers per gene
    shared = {}
    for gene in VERIFIED["Tdohrnii"]:
        if gene not in out.get("Tdohrnii", {}) or gene not in out.get("Aaurita", {}):
            continue
        t = {k for k, z in out["Tdohrnii"][gene]["top_kmers"] if z >= 3}
        a = {k for k, z in out["Aaurita"][gene]["top_kmers"] if z >= 3}
        shared[gene] = sorted(t & a)
    json.dump(shared, open("results/shared_upstream_kmers.json", "w"), indent=1)
    print("shared:", shared, flush=True)

if __name__ == "__main__":
    main()
