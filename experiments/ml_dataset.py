"""Build ML datasets from strong-locus upstream regions + matched random negatives.

Class 1: 2 kb upstream of every strong locus (all genes) in the genome (dedup).
Class 0: same number of random genomic 2 kb windows.
Output: data/ml/{genome}_pos.json, data/ml/{genome}_neg.json
"""
import json, random, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from jellyfish.predict import revcomp
from Bio import SeqIO

FASTAS = {"Tdohrnii": "../data/genomes/GCA_027922465.2/ncbi_dataset/data/GCA_027922465.2/GCA_027922465.2_TUR_r2.0.1_genomic.fna",
          "Aaurita": "../data/genomes/GCA_004194415.1/ncbi_dataset/data/GCA_004194415.1/GCA_004194415.1_ABSv1_genomic.fna"}
UP = 2000
random.seed(26)

def main():
    os.makedirs("data/ml", exist_ok=True)
    ledger = json.load(open("results/locus_ledger.json"))
    for genome, fna in FASTAS.items():
        idx = SeqIO.index(fna, "fasta")
        seen, pos = set(), []
        for gene, info in ledger[genome].items():
            for loc in info.get("strong_loci", []):
                key = (loc["contig"], loc["start"] // 1000)
                if key in seen:
                    continue
                seen.add(key)
                c = loc["contig"]
                L = len(idx[c].seq)
                if loc["strand"] == "+":
                    lo = max(1, loc["start"] - UP)
                    s = str(idx[c].seq[lo-1:loc["start"]-1])
                else:
                    hi = min(L, loc["end"] + UP)
                    s = revcomp(str(idx[c].seq[loc["end"]:hi]))
                if len(s) >= 1000 and s.count("N") / len(s) < 0.1:
                    pos.append(s[:UP])
        contigs = [c for c in idx.keys() if len(idx[c].seq) > 20000]
        neg = []
        tries = 0
        while len(neg) < len(pos) and tries < 20000:
            tries += 1
            c = random.choice(contigs)
            L = len(idx[c].seq)
            i = random.randint(0, L - UP - 1)
            s = str(idx[c].seq[i:i+UP])
            if s.count("N") / len(s) < 0.1:
                neg.append(s)
        json.dump(pos, open(f"data/ml/{genome}_pos.json", "w"))
        json.dump(neg, open(f"data/ml/{genome}_neg.json", "w"))
        print(genome, "pos", len(pos), "neg", len(neg), flush=True)

if __name__ == "__main__":
    main()
