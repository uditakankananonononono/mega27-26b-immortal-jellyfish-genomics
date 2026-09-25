"""Stitch candidate proteins for every extracted locus -> results/predicted_proteins.json + data/proteins/*.faa"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from jellyfish.loci import cluster_loci
from jellyfish.predict import stitch

MIN_BITS = 100

def read_fasta(path):
    lines = open(path).read().splitlines()
    return lines[0], "".join(lines[1:])

def main():
    os.makedirs("data/proteins", exist_ok=True)
    hits = json.load(open("results/tblastn_hits.json"))
    ledger = json.load(open("results/locus_ledger.json"))
    out = {}
    for genome, genes in hits.items():
        out[genome] = {}
        per_gene = {}
        for key, hs in genes.items():
            if isinstance(hs, dict): continue
            _, sym = key.split("_", 1)
            per_gene.setdefault(sym, []).extend(hs)
        for sym, hs in per_gene.items():
            info = ledger[genome].get(sym, {})
            strong = info.get("strong_loci", [])
            if not strong:
                continue
            top = strong[0]
            fn = top.get("extracted_file")
            if not fn or not os.path.exists(fn):
                continue
            lo = top["extracted_range"][0]
            _, seq = read_fasta(fn)
            # HSPs belonging to the top locus: same contig, overlapping span
            locus_hsps = [h for h in hs if h["contig"] == top["contig"]
                          and min(h["sstart"], h["send"]) <= top["end"]
                          and max(h["sstart"], h["send"]) >= top["start"]]
            pred = stitch(locus_hsps, seq, lo)
            if pred and len(pred["protein"]) >= 30:
                pred["gene"] = sym; pred["genome"] = genome
                pred["contig"] = top["contig"]
                out[genome][sym] = pred
                with open(f"data/proteins/{genome}_{sym}.faa", "w") as fh:
                    fh.write(f">{genome}_{sym}|{top['contig']}|{pred['n_segments']}seg\n")
                    p = pred["protein"]
                    for i in range(0, len(p), 60):
                        fh.write(p[i:i+60] + "\n")
        print(genome, len(out[genome]), "predicted", flush=True)
    json.dump(out, open("results/predicted_proteins.json", "w"), indent=1)

if __name__ == "__main__":
    main()
