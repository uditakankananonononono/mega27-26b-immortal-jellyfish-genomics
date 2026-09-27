"""D9 recompute of benchmark arm 1 (Clytia calibration): per gene, recall with
ALL query species vs HUMAN-ONLY queries, identical tBLASTn output, frozen
cluster_loci + MIN_BITS=100."""
import json, sys
sys.path.insert(0, ".")
from jellyfish.loci import cluster_loci
MIN_BITS = 100
raw = json.load(open("results/x-tblastn-bc.json"))["Clytia"]
genes = sorted({k.split("_", 1)[1] for k in raw})
multi, human_only, human_recovered_unique = [], [], []
for g in genes:
    allhits = [h for k, hs in raw.items() if k.split("_", 1)[1] == g for h in hs]
    hum = [h for k, hs in raw.items() if k == f"human_{g}" for h in hs]
    m = any(l["total_bits"] >= MIN_BITS for l in cluster_loci(allhits))
    h = any(l["total_bits"] >= MIN_BITS for l in cluster_loci(hum)) if hum else False
    if m: multi.append(g)
    if h: human_only.append(g)
    if m and not h: human_recovered_unique.append(g)
out = {"genome": "Clytia", "panel": 47,
       "multi_species_recall": f"{len(multi)}/47", "human_only_recall": f"{len(human_only)}/47",
       "multi_pct": round(100 * len(multi) / 47, 1), "human_pct": round(100 * len(human_only) / 47, 1),
       "recovered_only_via_nonhuman": sorted(set(multi) - set(human_only)),
       "note": "post-D9 recompute; identical merged tBLASTn output, frozen clustering"}
json.dump(out, open("results/x-benchmark-recall.json", "w"), indent=1)
print(json.dumps(out, indent=1))
