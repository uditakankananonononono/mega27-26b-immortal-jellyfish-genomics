# MEGA27-26b EXPANSION PREREGISTRATION
## Immortal-jellyfish comparative genomics -> aging/longevity + neurology
Locked 2026-09-26 ~15:50 IST BEFORE any expansion outcome data is fetched or
analyzed. Committed and pushed before downloads begin; the commit SHA is the
temporal proof.

## 0. Authority and scope
User directive (WhatsApp, 2026-09-26 15:38:44 IST, verbatim): "from now on
remember every paper should be 50+ pages only including content (no headings,
appendix, reference) also jellyfish research needs to improve and connect with
other major problems like aging lonegtivity research, neurology etc".
Amendment (15:39:36 IST, verbatim): "diagrams dont count in the page count".
EXPANSION, not rebuild: all existing work is preserved (unified via merge of
the divergent master annotation-desert-paper branch into main's full pipeline
branch; 41/41 tests pass at the merge commit).

## 1. Starting state (verified locally, not assumed)
- jellyfish/ package: loci clustering, panel definition (21-gene panel A
  incl. POLD1/POLD2/POLE arm), ML (CNN/GNN), motifs, mutations, telomere,
  predict, cli.
- results/: tblastn presence maps for Tdohrnii (GCA_027922465.2),
  TdohrniiOviedo (GCA_025167195.1), Aaurita (GCA_004194415.1) built with
  NCBI tBLASTn 2.17.0, evalue 1e-5, MIN_BITS 100 (thresholds already frozen
  by the closed phase and REUSED unchanged here).
- Boundary status: panel A loci ARE mappable in T. dohrnii genomes
  (locus_ledger.json), i.e. database absence != genome absence is already
  demonstrated for panel A. The README on master was stale on this point and
  is corrected in this expansion.

## 2. New data (accessions fixed here, before fetching)
- T. rubra GCA_039566895.2 (chromosome-level; non-reverting congener) - NEW.
- Reuse: Tdohrnii GCA_027922465.2, TdohrniiOviedo GCA_025167195.1,
  Aaurita GCA_004194415.1 (same pipeline, same thresholds).
- Optional calibration: Clytia hemisphaerica GCF_902728285.1 (annotated) if
  download/time permits; its RefSeq proteins are query sources regardless.
- Query proteins: human RefSeq canonical accessions (list frozen below);
  cnidarian homologs (Clytia/Acropora RefSeq protein search by gene name).
- All URLs + SHA256 logged in data/README-X.md.

## 3. New panels (gene lists frozen here)
PANEL B (aging/longevity, 24): FOXO3 SIRT1 SIRT6 MTOR IGF1 IGF1R INSR AKT1
PTEN TP53 CDKN2A ATM ATR BLM WRN NFE2L2 HSF1 ATG5 ATG7 BECN1 TFEB PRKAA1
GHR APOE.
PANEL C (neurology/neurodegeneration, 24): APP PSEN1 PSEN2 MAPT SNCA LRRK2
PARK7 PINK1 PRNP GBA HTT SOD1 TARDBP FUS C9orf72 GRN SQSTM1 OPTN VCP UBQLN2
TREM2 BDNF NGF (APOE shared with B, counted once).
Rationale: B = core longevity/hallmark-of-aging maintenance machinery
(GenAge-consistent); C = major monogenic neurodegeneration + neurotrophin
genes. Both route the jellyfish findings to aging/longevity and neurology
as the user directed. Ancient-conserved genes are expected to map; recently
evolved vertebrate genes are expected NOT to map - both outcomes are
informative and are reported at equal prominence.

## 4. Method (reuses the closed phase's validated BLAST pipeline)
1. tBLASTn 2.17.0, evalue 1e-5, max_target_seqs 20, identical outfmt and
   qcov computation as experiments/map_panel.py; loci clustered with
   jellyfish.loci.cluster_loci; strong locus = total_bits >= 100 (frozen).
2. POSITIVE CONTROL: panel A queries re-run on the rebuilt DBs must
   reproduce the closed phase's presence calls; any mismatch is a pipeline
   bug and blocks panel B/C interpretation until resolved.
3. NEGATIVE CONTROL: shuffled versions of every query protein (fixed seed
   26b) run on every genome; FPR must be <=5% of shuffled queries yielding
   a strong locus, else results are flagged invalid and recalibration
   happens on controls ONLY.
4. Copy-signal per gene per genome = number of strong loci (as in
   locus_ledger), reported with best pident/qcov/bits.

## 5. Hypotheses and pre-registered tests (BH FDR q<0.05 within each family)
H1 (panel-B mapping): >=50% of Panel B genes have >=1 strong locus in at
   least one T. dohrnii assembly (binomial vs control rate). Records the
   aging/longevity gene content actually present in the immortal jellyfish.
H2 (panel-C mapping): same test for Panel C; the gene-by-gene map is the
   neurology connection (human disease annotation carried from panel def).
H3 (expansion contrast): per-gene copy-signal contrast T. dohrnii vs
   T. rubra vs A. aurita across panels A+B (Fisher exact per gene, BH
   across genes). No surviving contrast = honest negative; the
   Pascual-Torner 2022 expansion claim is tested, not assumed.
H4 (aging-strategy separation): presence/copy matrix (genes x 4 genomes)
   separates rejuvenating (Tdohrnii x2) from non-reverting cnidarians
   (Trubra, Aaurita); pre-registered metric: mean within-Tdohrnii Jaccard
   distance minus mean Tdohrnii-vs-others distance; permutation p over
   genome labels (all 30 permutations of 4 labels, exact), BH.
H5 (shared maintenance machinery): overlap of mapped B and C genes in
   T. dohrnii vs expectation under independence (Fisher exact, BH): tests
   whether the same maintenance genes serve both longevity and neuronal
   maintenance hypotheses.
H6 (controls): positive control reproduces panel A calls; negative control
   FPR <=5%. Failure = invalid run, reported.
Exploratory (labeled as such): any ML reuse of the closed phase's CNN/GNN
arms on the expanded feature set; small-n caveat stated.

## 6. Honest-negative register
Any H1-H6 failure is a reported negative at equal prominence. No post-hoc
panel edits, no threshold changes after seeing T. dohrnii results, no metric
shopping. Deviations logged in docs/X-DEVIATIONS.md and labeled exploratory.

## 7. Deliverables
1. jellyfish/xpanel.py (panels B/C definitions), experiments/x_*.py
   (fetch, map, controls, stats), unit tests for every new module.
2. results/x-presence-bc.json, results/x-controls.json, results/x-stats.json,
   results/x-negatives.json, results/x-ledger.json.
3. paper/MEGA27-26b-EXPANSION.docx: 50+ pages of TEXT body content;
   headings, references, appendix and diagrams/figures excluded from count
   (user rule + amendment). Page-count methodology documented in the paper
   itself (word-count-based estimate, stated formula).
4. docs/X-FINDINGS.md linking every claim to result files + SHAs;
   README updated to the true unified state.
