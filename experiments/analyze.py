"""Comparative analysis: DNA-repair/telomerase gene-set signatures across
aging-resistance strategies. Human (aging reference) vs Hydra vulgaris
(non-aging regenerative cnidarian). T. dohrnii/A. aurita arm: public gene-level
records verified ABSENT (nucleotide/gene/protein db + UniProt, synonyms tried);
the genome-assembly path is documented as the follow-up."""
import json, os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from jellygen.ncbi import parse_fasta
from jellygen.compare import (DNA_REPAIR_GENES, TELOMERASE_GENES, gc_content,
                              codon_usage, pairwise_signature_distance,
                              cosine, kmer_spectrum, copy_number_signal)

DATA = os.path.join(os.path.dirname(__file__), "..", "data")
OUT = os.path.join(os.path.dirname(__file__), "..", "results")
os.makedirs(os.path.join(OUT, "figures"), exist_ok=True)

species = ["human", "hvulgaris"]
genes = DNA_REPAIR_GENES + TELOMERASE_GENES
sets = {}
counts = {}
for sp in species:
    seqs, n_rec = [], 0
    per_gene = {}
    for g in genes:
        fn = os.path.join(DATA, f"{sp}_{g}.fasta")
        if not os.path.exists(fn):
            per_gene[g] = 0
            continue
        recs = parse_fasta(open(fn).read())
        per_gene[g] = len(recs)
        for _, s in recs:
            if len(s) >= 300:
                seqs.append(s.upper())
    sets[sp] = seqs
    counts[sp] = per_gene

res = {"per_species_gene_records": counts,
       "n_sequences": {sp: len(s) for sp, s in sets.items()},
       "database_gap": {
           "turritopsis_dohrnii": "0 records in NCBI nucleotide/gene/protein for all 18 repair/telomerase genes (synonyms Turritopsis nutricula tried); UniProt: 4 total entries, none repair/telomerase. Only raw genome assemblies exist (e.g. GCA_051903475.1).",
           "aurelia_aurita": "0 gene-level records for the panel; UniProt 114 entries, none in panel."},
       "hypothesis_reference": "Pascual-Torner et al. 2022 PNAS: comparative genomics of T. dohrnii vs C. hemisphaerica reported expansions of DNA-repair and replication-associated genes."}

if all(sets.values()):
    res["mean_gc"] = {sp: float(np.mean([gc_content(s) for s in sets[sp]]))
                      for sp in species}
    res["signature_distance_human_vs_hydra"] = pairwise_signature_distance(
        sets["human"], sets["hvulgaris"], k=4)
    # human self-distance as calibration (split-half)
    h = sets["human"]
    half = len(h) // 2
    res["signature_distance_human_halfsplit"] = pairwise_signature_distance(
        h[:half], h[half:], k=4)
    # per-gene copy signal: hydra vs human record counts
    res["copy_number"] = counts
    repair_h = sum(counts["hvulgaris"].get(g, 0) for g in DNA_REPAIR_GENES)
    repair_hs = sum(counts["human"].get(g, 0) for g in DNA_REPAIR_GENES)
    res["repair_record_totals"] = {"hydra": repair_h, "human": repair_hs}

with open(os.path.join(OUT, "results.json"), "w") as f:
    json.dump(res, f, indent=1)

fig, ax = plt.subplots(1, 2, figsize=(9, 3.5))
present = [g for g in genes if counts["human"].get(g) or counts["hvulgaris"].get(g)]
x = np.arange(len(present))
ax[0].bar(x - 0.2, [counts["human"].get(g, 0) for g in present], 0.4, label="human")
ax[0].bar(x + 0.2, [counts["hvulgaris"].get(g, 0) for g in present], 0.4, label="hydra")
ax[0].set_xticks(x, present, rotation=90, fontsize=6)
ax[0].set_ylabel("records fetched"); ax[0].legend(); ax[0].set_title("Repair/telomerase panel coverage")
if "mean_gc" in res:
    ax[1].bar(["human", "hydra"], [res["mean_gc"]["human"], res["mean_gc"]["hvulgaris"]])
    ax[1].set_ylabel("mean GC fraction"); ax[1].set_title("GC signature of repair gene set")
fig.tight_layout(); fig.savefig(os.path.join(OUT, "figures", "jellyfish.png"), dpi=150)
print(json.dumps({k: v for k, v in res.items() if k != "database_gap"}, indent=1)[:800])
