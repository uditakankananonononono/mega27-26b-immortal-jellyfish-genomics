"""Unique-substitution analysis on domain-verified genes.

Per (genome, verified gene): align predicted jellyfish protein to each
available reference ortholog (human, Nematostella, Hydra, Clytia); find
conserved reference positions (>=75% agreement over >=3 covering refs) where
the jellyfish residue differs. Compare T. dohrnii vs A. aurita substitution
patterns. Output results/unique_mutations.json.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from jellyfish.mutations import unique_substitutions_with_stats

VERIFIED = {"Tdohrnii": ["DKC1","ERCC1","LIG4","MLH1","MSH2","POLD1","POT1","RAD51","XRCC1"],
            "TdohrniiOviedo": ["DKC1","ERCC1","LIG4","MLH1","MSH2","POLD1","POT1","RAD51","XRCC1"],
            "Aaurita": ["DKC1","ERCC1","LIG4","MLH1","MSH2","POLD1","POT1","RAD51"]}
REF_SPECIES = ["human", "Nematostella", "Hydra", "Clytia"]

def read_fasta_seq(path):
    lines = open(path).read().splitlines()
    return "".join(l for l in lines if not l.startswith(">"))

def main():
    out = {}
    for genome, genes in VERIFIED.items():
        out[genome] = {}
        for gene in genes:
            pred_path = f"data/proteins/{genome}_{gene}.faa"
            if not os.path.exists(pred_path):
                continue
            query = read_fasta_seq(pred_path)
            refs = []
            for sp in REF_SPECIES:
                p = f"data/panel/{sp}_{gene}.faa"
                if os.path.exists(p):
                    refs.append(read_fasta_seq(p))
            if len(refs) < 3:
                out[genome][gene] = {"error": f"only {len(refs)} refs"}
                continue
            subs, stats = unique_substitutions_with_stats(query, refs)
            rec = {"n_unique_substitutions": len(subs), "substitutions": subs,
                   "query_len": len(query), "n_refs": len(refs)}
            rec.update(stats)
            out[genome][gene] = rec
        print(genome, "done", flush=True)
    json.dump(out, open("results/unique_mutations.json", "w"), indent=1)

if __name__ == "__main__":
    main()
