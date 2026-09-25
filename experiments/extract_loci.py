"""Cluster HSPs into loci per gene x genome, extract top-locus regions via blastdbcmd."""
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from jellyfish.loci import cluster_loci, region_bounds

from Bio import SeqIO
FASTAS = {"Tdohrnii": "../data/genomes/GCA_027922465.2/ncbi_dataset/data/GCA_027922465.2/GCA_027922465.2_TUR_r2.0.1_genomic.fna",
       "TdohrniiOviedo": "../data/genomes/GCA_025167195.1/ncbi_dataset/data/GCA_025167195.1/GCA_025167195.1_ASM2516719v1_genomic.fna",
       "Aaurita": "../data/genomes/GCA_004194415.1/ncbi_dataset/data/GCA_004194415.1/GCA_004194415.1_ABSv1_genomic.fna"}
MIN_BITS = 100  # locus must carry at least this much total evidence

def main():
    os.makedirs("data/loci", exist_ok=True)
    main.IDX = {}
    hits = json.load(open("results/tblastn_hits.json"))
    ledger = {}
    for genome, genes in hits.items():
        ledger[genome] = {}
        # merge hits across query species per panel gene
        per_gene = {}
        for key, hs in genes.items():
            if isinstance(hs, dict): continue
            _, sym = key.split("_", 1)
            per_gene.setdefault(sym, []).extend(hs)
        for sym, hs in per_gene.items():
            loci = cluster_loci(hs)
            strong = [l for l in loci if l["total_bits"] >= MIN_BITS]
            ledger[genome][sym] = {"n_loci": len(loci), "strong_loci": strong, "all_loci_summary":
                [{k: l[k] for k in ("contig","start","end","n_hsps","total_bits")} for l in loci[:5]]}
            if strong:
                top = strong[0]
                lo, hi = region_bounds(top)
                if genome not in main.IDX:
                    main.IDX[genome] = SeqIO.index(FASTAS[genome], "fasta")
                rec = main.IDX[genome][top["contig"]]
                hi = min(hi, len(rec.seq))
                sub = rec.seq[lo-1:hi]
                fn = f"data/loci/{genome}_{sym}.fa"
                with open(fn, "w") as fh:
                    fh.write(f">{top['contig']}:{lo}-{hi}\n")
                    for i in range(0, len(sub), 60):
                        fh.write(str(sub[i:i+60]) + "\n")
                top["extracted_file"] = fn
                top["extracted_range"] = [lo, hi]
        print(genome, "done", flush=True)
    json.dump(ledger, open("results/locus_ledger.json", "w"), indent=1)

if __name__ == "__main__":
    main()
