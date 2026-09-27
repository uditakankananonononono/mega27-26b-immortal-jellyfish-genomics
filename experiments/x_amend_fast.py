#!/usr/bin/env python3
"""Amendment P1 fast items: (7) AEES weight sensitivity, (17) enrichment statistics."""
import json, random
from jellyfish.xaees import locus_score, TD_ASSEMBLIES
from jellyfish.xstats import fisher, bh_adjust

led = json.load(open("results/x-ledger-bc.json"))
ann = json.load(open("results/x-aging-annotation.json"))

# --- item 7: weight sensitivity on the Tdohrnii ranking ---
td = led["Tdohrnii"]
tdo = led["TdohrniiOviedo"]
td_both = {g for g, r in td.items() if r.get("n_strong", 0) >= 1}
tdo_both = {g for g, r in tdo.items() if r.get("n_strong", 0) >= 1}
genes = sorted(td.keys())

def score(gene, w):
    rec = td.get(gene, {})
    if rec.get("n_strong", 0) < 1 or not rec.get("best"):
        return 0.0
    bits, qcov, pid = locus_score(rec["best"])
    conc = 1.0 if gene in tdo_both else 0.5
    return w[0]*bits + w[1]*qcov + w[2]*pid + w[3]*conc

def ranking(w):
    return sorted(genes, key=lambda g: -score(g, w))

W_FROZEN = (0.35, 0.25, 0.15, 0.25)
W_EQUAL = (0.25, 0.25, 0.25, 0.25)
r_frozen = ranking(W_FROZEN)
r_equal = ranking(W_EQUAL)
frozen_top5 = set(r_frozen[:5])
rnd = random.Random(270927)
atg5_ranks, top5_overlap = [], []
for _ in range(200):
    w = [rnd.random() for _ in range(4)]
    s = sum(w)
    w = tuple(x/s for x in w)
    r = ranking(w)
    atg5_ranks.append(r.index("ATG5") + 1)
    top5_overlap.append(len(set(r[:5]) & frozen_top5))
sens = {
    "frozen_weights": W_FROZEN, "note": "weights frozen pre-registration in jellyfish/xaees.py",
    "atg5_rank_frozen": r_frozen.index("ATG5") + 1,
    "atg5_rank_equal": r_equal.index("ATG5") + 1,
    "atg5_rank_random_min": min(atg5_ranks), "atg5_rank_random_max": max(atg5_ranks),
    "top5_overlap_random_mean": round(sum(top5_overlap)/len(top5_overlap), 2),
    "frozen_top5": r_frozen[:5],
}
json.dump(sens, open("results/x-aees-sensitivity.json", "w"), indent=1)
print("sensitivity:", json.dumps(sens)[:400])

# --- item 17: enrichment of aging-DB membership among high-AEES genes ---
aees = json.load(open("results/x-aees.json"))["Tdohrnii"]
high = {g for g, v in aees.items() if v["aees"] >= 0.75}
univ = set(aees.keys())
tests = []
for key, label in [("genage_human_hits", "GenAge human"), ("genage_model_hits", "GenAge models"),
                   ("cellage_hits", "CellAge"), ("longevitymap_hits", "LongevityMap")]:
    mem = set(ann[key]) & univ
    a = len(high & mem); b = len(high - mem)
    c = len(mem - high); d = len(univ - high - mem)
    _, p = fisher(a, b, c, d)
    oratio = (a * d) / max(1, b * c)
    tests.append({"db": label, "high_member": a, "high_nonmember": b,
                  "low_member": c, "low_nonmember": d,
                  "odds_ratio": round(oratio, 2), "p": p})
qs = bh_adjust([t["p"] for t in tests])
for t, q in zip(tests, qs):
    t["q"] = q
out = {"high_threshold": 0.75, "n_high": len(high), "n_universe": len(univ),
       "high_genes": sorted(high), "tests": tests}
json.dump(out, open("results/x-enrichment.json", "w"), indent=1)
print("enrichment:", json.dumps(tests, indent=1))
