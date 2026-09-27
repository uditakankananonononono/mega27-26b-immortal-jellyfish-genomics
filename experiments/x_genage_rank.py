"""P1 #16: genome-wide discovery arm - rank the full GenAge human set by
AEES-like evidence in T. dohrnii and compare with the panel-B ranking.
Inputs: results/x-ledger-genage.json (per-genome ledgers from x_map genage).
Outputs: results/x-genage-aees.json + printed top/bottom summary.
Concordance component: detected in both Td assemblies = 1.0, one = 0.5.
Panel comparison: where do panel-B genes sit inside the genome-wide ranking
(Wilcoxon rank-sum vs non-panel GenAge genes), and which NON-panel GenAge genes
rank high (candidate discoveries the panel missed)."""
import json, sys
sys.path.insert(0, ".")
from jellyfish.xaees import locus_score, W_BITS, W_QCOV, W_PIDENT, W_CONC
from scipy.stats import mannwhitneyu

led = json.load(open("results/x-ledger-genage.json"))
have = [g for g in ("Tdohrnii", "TdohrniiOviedo") if g in led]
assert "Tdohrnii" in have, "need Tdohrnii ledger"
panel = set(json.load(open("results/x-aees.json"))["Tdohrnii"].keys())

td, tdo = led["Tdohrnii"], led.get("TdohrniiOviedo", {})
genes = sorted(set(td) | set(tdo))
out = {}
for g in genes:
    rec = td.get(g, {})
    present = rec.get("n_strong", 0) >= 1 and rec.get("best")
    conc = 0.0
    if present and tdo.get(g, {}).get("n_strong", 0) >= 1:
        conc = 1.0
    elif present or tdo.get(g, {}).get("n_strong", 0) >= 1:
        conc = 0.5
    if present:
        bits, qcov, pid = locus_score(rec["best"])
        aees = W_BITS*bits + W_QCOV*qcov + W_PIDENT*pid + W_CONC*conc
        out[g] = {"aees": round(aees, 4), "n_strong": rec["n_strong"],
                  "concordance": conc, "in_panel": g in panel,
                  "best_bits": rec["best"]["total_bits"]}
    else:
        out[g] = {"aees": 0.0, "n_strong": 0, "concordance": conc,
                  "in_panel": g in panel, "best_bits": 0}
ranked = sorted(out, key=lambda g: -out[g]["aees"])
detected = [g for g in ranked if out[g]["aees"] > 0]
panel_scores = [out[g]["aees"] for g in out if out[g]["in_panel"] and g in genes]
nonpanel_scores = [out[g]["aees"] for g in out if not out[g]["in_panel"]]
u, p = mannwhitneyu(panel_scores, nonpanel_scores, alternative="greater")
novel = [g for g in detected[:60] if not out[g]["in_panel"]][:25]
summary = {"n_genes": len(genes), "n_detected": len(detected),
           "panel_size": sum(1 for g in out if out[g]["in_panel"]),
           "panel_vs_nonpanel_mannwhitney_p": p,
           "top25_overall": [(g, out[g]["aees"]) for g in ranked[:25]],
           "top_novel_nonpanel": novel,
           "panel_genes_in_top60": sum(1 for g in ranked[:60] if out[g]["in_panel"])}
json.dump({"summary": summary, "scores": out}, open("results/x-genage-aees.json", "w"), indent=1)
print(json.dumps(summary, indent=1)[:1200])
print("GENAGERANKDONE")
