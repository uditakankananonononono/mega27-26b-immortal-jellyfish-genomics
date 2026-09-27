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
and upstream-motif, telomere, and SRA census analyses. The test suite (54 tests at last full run, including the expansion modules) covers the pipeline.

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

Run the local tests with `python3 -m pytest -q`. For a fresh-clone verification of the **committed downstream artifacts** (no genomes or raw RNA reads needed), run from the repository root:

```sh
python3 -m pytest -q
cp results/x-stats.json /tmp/x-stats.baseline.json
cp results/x-genage-aees.json /tmp/x-genage.baseline.json
python3 experiments/x_stats.py
python3 experiments/x_genage_rank.py
cmp /tmp/x-stats.baseline.json results/x-stats.json
cmp /tmp/x-genage.baseline.json results/x-genage-aees.json
python3 experiments/x_makepaper.py
```

This checks only ledger-derived statistics, the GenAge ranking, and body-page rendering on the host's Python/LibreOffice installation. It is **not** a fresh-machine end-to-end reproduction of the mappings: `experiments/x_map.py` currently hard-codes the original workspace's BLAST binary and database paths, raw genomes/BLAST databases and RNA reads are not shipped in Git, and the CLI's `run` subcommand does not exist. Reproducing raw mapping needs a new environment bootstrap, source fetch/verification and path configuration. Do not claim that this repository can regenerate every table, figure, and ranking with one command yet. A fresh-clone downstream check was run at commit e7d197e on 2026-09-27; tests passed and x-stats/genage JSON matched byte for byte.
