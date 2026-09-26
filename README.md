# mega27-26b-immortal-jellyfish-genomics

Comparative genomics of the immortal jellyfish *Turritopsis dohrnii* against mortal cnidarian
relatives, aimed at aging/longevity and neurodegeneration biology.

## What is true here (verified against the repo's own result files)

**Closed phase (complete).** Public gene databases (NCBI gene/nucleotide/protein, UniProt) hold
near-zero gene-level records for T. dohrnii and A. aurita for the 21-gene DNA-repair/telomerase
panel — an annotation desert (documented in `results/desert_audit.json`). The pipeline therefore
works genome-first: tBLASTn of query proteins directly against the raw assemblies
(`results/tblastn_hits.json`, `results/locus_ledger.json`). This maps real loci in the draft
assemblies — e.g. FEN1 in T. dohrnii at 47.6% identity over 521/567 alignment columns,
e-value 3e-159 — alongside executable ML arms (`results/ml_cnn.json`, `results/ml_gnn.json`)
and upstream-motif, telomere, and SRA census analyses. 34 legacy tests cover the pipeline.

**Expansion (in progress, pre-registered).** `docs/EXPANSION-PREREGISTRATION.md` (locked in
commit `08d8be0` BEFORE any expansion outcome data was touched) freezes two new panels —
24 aging/longevity genes and 24 neurodegeneration genes — hypotheses H1-H6, BH FDR control,
and the controls (shuffled-query false-positive rate; reproduction of closed-phase calls).
Five assemblies are used: two independent T. dohrnii assemblies (891 contigs and 74,835
scaffolds — assembly-quality asymmetry is a stated confound), T. rubra, A. aurita, and
Clytia (annotated calibration). Queries are 125 proteins (47 human + 78 cnidarian).
Results chapters of the 50+ text-body-page paper are auto-generated from result files.

## Honest-negative register

Database-level nulls (the annotation desert) are documented at equal prominence and are NOT
terminal: the genome-first arm exists precisely because database-first fails. Any expansion
hypothesis that fails is reported as a negative and rerouted through
`docs/X-PIVOT-LADDER.md`, never silently dropped.

## Layout

- `jellyfish/` — pipeline + expansion code (`xpanel.py`, `xstats.py`, mapping, ML)
- `experiments/` — fetch, map, stats, section/paper builders
- `paper_x/` — expansion paper sections (auto-generated results chapters + prose)
- `docs/` — pre-registration, pivot ladder, judge-round rules and logs
- `results/` — closed-phase and expansion result files (machine-readable)

Run: `pip install -e . && pytest`
Expansion reproduction: `python experiments/x_map.py actrl|bc|bcshuf` then
`python experiments/x_stats.py` then `python experiments/x_makepaper.py`.
