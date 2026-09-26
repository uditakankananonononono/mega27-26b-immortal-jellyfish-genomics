"""Generate results chapters 06/07/08 from result JSONs + gene backgrounds."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "paper_x"))
from gene_bg_b import GENE_BG_B
from gene_bg_c import GENE_BG_C
from jellyfish.xpanel import PANEL_B, PANEL_C

SEC = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "paper_x", "sections")
GENOMES = [("Tdohrnii", "T. dohrnii (contig assembly)"),
           ("TdohrniiOviedo", "T. dohrnii (Oviedo scaffold assembly)"),
           ("Trubra", "T. rubra"),
           ("Aaurita", "A. aurita")]

def fmt_best(b):
    if not b:
        return "no locus above threshold"
    return (f"best locus on contig {b['contig']}:{b['start']}-{b['end']}, "
            f"{b['n_hsps']} high-scoring pairs, total bit score {b['total_bits']}, "
            f"peak identity {b['best_pident']}%, peak query coverage {round(b['best_qcov']*100)}%")

def gene_para(sym, bg, amap):
    e = amap[sym]
    td = e["Tdohrnii"]["present"] or e["TdohrniiOviedo"]["present"]
    both = e["Tdohrnii"]["present"] and e["TdohrniiOviedo"]["present"]
    tr = e["Trubra"]["present"]; aa = e["Aaurita"]["present"]
    parts = [bg]
    if td:
        which = "both T. dohrnii assemblies" if both else ("the contig assembly only" if e["Tdohrnii"]["present"] else "the Oviedo assembly only")
        parts.append(f"MAPPED: {sym} is present in {which}.")
        for g, _ in GENOMES:
            if e[g]["present"]:
                parts.append(f"In {dict(GENOMES)[g]}: {e[g]['copies']} strong locus/i; {fmt_best(e[g]['best'])}.")
    else:
        parts.append(f"NOT MAPPED: no strong locus for {sym} in either T. dohrnii assembly at the frozen threshold.")
    comp = []
    comp.append("present in T. rubra" if tr else "absent in T. rubra")
    comp.append("present in A. aurita" if aa else "absent in A. aurita")
    parts.append("Comparator status: " + ", ".join(comp) + ".")
    return " ".join(parts)

def main():
    agemap = json.load(open("results/x-agemap.json"))
    neuromap = json.load(open("results/x-neuromap.json"))
    stats = json.load(open("results/x-stats.json"))

    with open(os.path.join(SEC, "06_results_panelB.txt"), "w") as f:
        f.write("# Results: the aging and longevity panel, gene by gene\n\n")
        h1 = stats["H1_panelB"]
        f.write(f"Panel headline (pre-registered H1): {h1['genes_present']} of {h1['n']} Panel B genes map in at least one T. dohrnii assembly "
                f"(fraction {h1['fraction']:.2f}); binomial p = {h1['p']:.3g} against the negative-control rate {h1['control_p0']:.3g}, "
                f"Benjamini-Hochberg q = {h1['q']:.3g} within the H1-H2 family. "
                f"Present: {', '.join(h1['present']) if h1['present'] else 'none'}. "
                f"Absent: {', '.join(h1['absent']) if h1['absent'] else 'none'}.\n\n")
        for sym, grp, note in PANEL_B:
            f.write(gene_para(sym, f"{sym} ({grp}). {GENE_BG_B[sym]}", agemap) + "\n\n")

    with open(os.path.join(SEC, "07_results_panelC.txt"), "w") as f:
        f.write("# Results: the neurology and neurodegeneration panel, gene by gene\n\n")
        h2 = stats["H2_panelC"]
        f.write(f"Panel headline (pre-registered H2): {h2['genes_present']} of {h2['n']} Panel C genes map in at least one T. dohrnii assembly "
                f"(fraction {h2['fraction']:.2f}); binomial p = {h2['p']:.3g} against the negative-control rate {h2['control_p0']:.3g}, "
                f"Benjamini-Hochberg q = {h2['q']:.3g}. "
                f"Present: {', '.join(h2['present']) if h2['present'] else 'none'}. "
                f"Absent: {', '.join(h2['absent']) if h2['absent'] else 'none'}.\n\n")
        for sym, grp, note in PANEL_C:
            f.write(gene_para(sym, f"{sym} ({grp}). {GENE_BG_C[sym]}", neuromap) + "\n\n")

    with open(os.path.join(SEC, "08_htests.txt"), "w") as f:
        f.write("# The pre-registered hypothesis tests\n\n")
        h3 = stats["H3_copy_contrast"]
        surv = [g for g, d in h3["per_gene"].items() if d["q"] < 0.05]
        f.write(f"H3 (copy-number contrast, Panel B, T. dohrnii vs mortal comparators): {h3['n_q_lt_0.05']} genes survive Benjamini-Hochberg at q < 0.05"
                + (f": {', '.join(surv)}. These are nominations for mechanistic follow-up, not demonstrated adaptations." if surv else
                   ". Under the honest-negative register this is reported as a negative for the expansion hypothesis in this panel.") + "\n\n")
        h4 = stats["H4_separation"]
        f.write(f"H4 (species separation on the presence map): statistic {h4['stat']:.3f}, exact permutation p = {h4['p']:.3g} over {h4['n_permutations']} label assignments. "
                f"Caveat carried from the preregistration: {h4['caveat']}.\n\n")
        h5 = stats["H5_BC_overlap"]
        f.write(f"H5 (aging-neurology shared core in T. dohrnii): {h5['a_both']} genes mapped in both panels, {h5['b_only']} B-only, {h5['c_only']} C-only, "
                f"{h5['neither']} neither, over a {h5['universe_n']}-gene universe; Fisher exact p = {h5['p']:.3g}.\n\n")
        h6n = stats["H6_negative_control"]; h6p = stats["H6_positive_control"]
        f.write("H6 (controls). Negative control, shuffled-query false-positive rate per genome: "
                + "; ".join(f"{g} {v:.3f}" for g, v in h6n["fpr_per_genome"].items())
                + f" - criterion <=0.05 everywhere: {'PASS' if h6n['pass'] else 'FAIL'}. "
                f"Positive control, closed-phase panel A calls reproduced: {h6p['n_compared'] - h6p['n_mismatch']} of {h6p['n_compared']} agreement"
                + (f"; mismatches: {h6p['mismatches']}." if h6p['n_mismatch'] else ".") + "\n")

if __name__ == "__main__":
    main()
    print("sections generated")
