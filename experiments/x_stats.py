"""H1-H6 pre-registered tests for the 26b expansion.

Inputs: results/x-ledger-bc.json, results/x-ledger-bcshuf.json,
        results/x-ledger-actrl.json, results/locus_ledger.json (closed phase)
Output: results/x-stats.json, results/x-negatives.json
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from jellyfish.xpanel import SYMBOLS_B, SYMBOLS_C, panel_of
from jellyfish.xstats import (bh_adjust, fisher, binom_ge, jaccard,
                              separation_statistic, permutation_p_labels)

TD = ["Tdohrnii", "TdohrniiOviedo"]
OTHERS = ["Trubra", "Aaurita"]
ALL_GENOMES = TD + OTHERS

def present(ledger, genome, sym):
    e = ledger.get(genome, {}).get(sym)
    return bool(e and e.get("n_strong"))

def copies(ledger, genome, sym):
    e = ledger.get(genome, {}).get(sym)
    return e.get("n_strong", 0) if e else 0

def td_present(ledger, sym):
    return any(present(ledger, g, sym) for g in TD)

def main():
    bc = json.load(open("results/x-ledger-bc.json"))
    shuf = json.load(open("results/x-ledger-bcshuf.json"))
    out = {"panels": {"B": SYMBOLS_B, "C": SYMBOLS_C}}

    # H6 controls: shuffled FPR per genome (fraction of shuffled genes with strong locus)
    fpr = {}
    n_shuf = {}
    for g in ALL_GENOMES + ["Clytia"]:
        genes_hit = [s for s, e in shuf.get(g, {}).items() if e.get("n_strong")]
        n_shuf[g] = len(shuf.get(g, {}))
        fpr[g] = len(genes_hit) / max(1, len(shuf.get(g, {})))
    out["H6_negative_control"] = {"fpr_per_genome": fpr, "n_shuffled_genes": n_shuf,
                                  "pass": all(v <= 0.05 for v in fpr.values())}

    # presence matrix
    pres = {}
    for g in ALL_GENOMES:
        pres[g] = {s for s in set(SYMBOLS_B) | set(SYMBOLS_C) if present(bc, g, s)}
    out["presence_counts"] = {g: len(pres[g]) for g in ALL_GENOMES}

    # H1 / H2: mapping fraction in T. dohrnii (any assembly) vs control rate
    # number of shuffled queries actually run (constant from the bcshuf run;
    # the ledger is empty when FPR=0, so ledger length cannot supply it)
    N_SHUFFLED_QUERIES = 125
    p0 = max(max(fpr.get(g, 0) for g in TD), 1 / (N_SHUFFLED_QUERIES + 1))
    h = {}
    for label, syms in (("H1_panelB", SYMBOLS_B), ("H2_panelC", SYMBOLS_C)):
        k = sum(1 for s in syms if td_present(bc, s))
        h[label] = {"genes_present": k, "n": len(syms), "fraction": k / len(syms),
                    "control_p0": p0, "p": binom_ge(k, len(syms), p0),
                    "present": sorted(s for s in syms if td_present(bc, s)),
                    "absent": sorted(s for s in syms if not td_present(bc, s))}
    qs = bh_adjust([h["H1_panelB"]["p"], h["H2_panelC"]["p"]])
    h["H1_panelB"]["q"], h["H2_panelC"]["q"] = qs
    out.update(h)

    # H3: per-gene copy contrast, panels A? (A reuse closed-phase ledger) + B
    # Panel B copy-signal: Tdohrnii (max across assemblies) vs others
    genes_b = SYMBOLS_B
    tab_p, detail = [], {}
    td_total = sum(copies(bc, g, s) for g in TD for s in genes_b)
    ot_total = sum(copies(bc, g, s) for g in OTHERS for s in genes_b)
    for s in genes_b:
        td_c = max(copies(bc, g, s) for g in TD)
        ot_c = max(copies(bc, g, s) for g in OTHERS)
        # copy-share contrast: this gene's strong-locus share in Td vs others,
        # 2x2 [[td_c, ot_c], [td_total - td_c, ot_total - ot_c]] (Fisher exact)
        _, p = fisher(td_c, ot_c, td_total - td_c, ot_total - ot_c)
        tab_p.append(p)
        detail[s] = {"td_max_copies": td_c, "other_max_copies": ot_c, "p": p}
    q3 = bh_adjust(tab_p)
    for s, q in zip(genes_b, q3):
        detail[s]["q"] = q
    out["H3_copy_contrast"] = {"per_gene": detail,
                               "n_q_lt_0.05": sum(1 for q in q3 if q < 0.05)}

    # H4: aging-strategy separation (Tdohrnii assemblies vs non-reverting)
    obs = separation_statistic(pres, TD, OTHERS)
    p4, n_perm, _ = permutation_p_labels(pres, TD, OTHERS, obs)
    out["H4_separation"] = {"stat": obs, "p": p4, "n_permutations": n_perm,
                            "caveat": "two T. dohrnii entries are assemblies of the SAME species; within-group similarity partly reflects assembly redundancy"}

    # H5: B/C overlap in T. dohrnii vs independence (universe = 47 unique symbols)
    uni = sorted(set(SYMBOLS_B) | set(SYMBOLS_C))
    inB = {s for s in uni if s in SYMBOLS_B and td_present(bc, s)}
    inC = {s for s in uni if s in SYMBOLS_C and td_present(bc, s)}
    a = len(inB & inC); b_ = len(inB - inC); c = len(inC - inB)
    d = len(uni) - a - b_ - c
    _, p5 = fisher(a, b_, c, d)
    out["H5_BC_overlap"] = {"a_both": a, "b_only": b_, "c_only": c, "neither": d,
                            "p": p5, "universe_n": len(uni)}

    # H6 positive control: closed-phase panel A presence vs actrl rerun
    actrl = json.load(open("results/x-ledger-actrl.json"))
    closed = json.load(open("results/locus_ledger.json"))
    mism = []
    for g in ("Tdohrnii", "TdohrniiOviedo", "Aaurita"):
        for sym, e in closed.get(g, {}).items():
            was = bool(e.get("strong_loci"))
            now = bool(actrl.get(g, {}).get(sym, {}).get("n_strong"))
            if was != now:
                mism.append({"genome": g, "gene": sym, "closed": was, "now": now})
    out["H6_positive_control"] = {"n_compared": sum(len(closed.get(g, {})) for g in ("Tdohrnii","TdohrniiOviedo","Aaurita")),
                                  "n_mismatch": len(mism), "mismatches": mism[:20]}

    json.dump(out, open("results/x-stats.json", "w"), indent=1)
    # gene-by-gene neuro map (for the paper)
    neuromap = {}
    for s in SYMBOLS_C:
        neuromap[s] = {g: {"present": present(bc, g, s),
                           "copies": copies(bc, g, s),
                           "best": bc.get(g, {}).get(s, {}).get("best")}
                       for g in ALL_GENOMES}
    json.dump(neuromap, open("results/x-neuromap.json", "w"), indent=1)
    agemap = {}
    for s in SYMBOLS_B:
        agemap[s] = {g: {"present": present(bc, g, s),
                         "copies": copies(bc, g, s),
                         "best": bc.get(g, {}).get(s, {}).get("best")}
                     for g in ALL_GENOMES}
    json.dump(agemap, open("results/x-agemap.json", "w"), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k.startswith("H6")}, indent=1))
    print("STATSDONE")

if __name__ == "__main__":
    main()
