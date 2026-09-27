# The Genome-First Annotation Recovery (GFAR) workflow - formal specification

Amendments P1 #1 and #10 (judge round: "method novelty not formalized - just BLAST
applied carefully?" and "non-model-organism framework benchmark"). This document
names the workflow, fixes its inputs, outputs, stages, parameters, complexity, and
failure modes, and states the framework-level benchmark that evaluates the workflow
itself (as opposed to any single gene finding).

## 1. Problem

Given a newly sequenced eukaryotic genome with no gene models, no transcriptome
assembly, and no trained ab initio predictor for its clade (an "annotation
desert"), recover the loci of a defined panel of genes, score the evidence for
each recovery under assembly uncertainty, and rank candidates for follow-up -
without ever training on the target genome and without transferring annotations
from a reference by synteny (which the desert does not preserve; amendment #13).

## 2. Inputs and outputs

Inputs:
- A: raw target assembly (FASTA contigs/scaffolds; no annotation track required).
- P: gene panel - for each gene, one or more protein queries, each exact-gene
  verified against its source database (D9 lesson: accessions drift; verification
  report required per query file).
- X: cross-species query expansion set - orthologous proteins from k related
  species per panel gene (here k=4 cnidarians + human), shrinking the
  query-to-target evolutionary distance along several independent paths.
- C: comparator assemblies of the same or sister lineages (for concordance).

Outputs, per gene per assembly:
- candidate loci (scaffold, span, summed bitscore);
- n_strong: number of loci with total_bits >= MIN_BITS;
- significance call: significant iff n_strong >= 3 (frozen H1 criterion);
- AEES in [0,1]: assembly-aware evidence score (section 4);
- status label: "detected" / "not detected" (never "absent" - assembly-gap honesty).

## 3. Stages (all parameters frozen pre-outcome)

S0 Panel verification. Every query file is re-fetched by exact gene match
(UniProt gene: field) and verified (accession -> gene symbol agreement).
Unverifiable queries are quarantined with a public report (data/xpanel_quarantine,
data/xpanel_fixed/verify_report.json: 47/47 verified).

S1 Mapping. tblastn of every query against every assembly, e-value <= 1e-10,
all HSPs with bitscore recorded. No gene model, no splice aligner, no training.

S2 Locus clustering. Per query, per scaffold: HSPs with bits >= MIN_BITS=100 are
merged when gaps <= 500 bp; a locus is the merged span with
total_bits = sum of member HSP bits.

S3 Calls. Strong locus: total_bits >= 100. Gene significant: n_strong >= 3.

S4 Assembly concordance. The same gene is mapped independently in >=2 assemblies
of the target lineage; concordance (both / one / none) feeds AEES and is the
primary defense against assembly-artifact calls (D4/D9 practice).

S5 Evidence scoring. AEES per section 4.

S6 Validation battery (every claim must pass at least one, most pass several):
  - shuffled-query arm (bcshuf): empirical false-positive rate (here 0);
  - verified decoy panel (non-aging genes): pipeline yield on genes it should
    mostly miss (here 8-10/23 vs 20/24 panel; Fisher p = 0.0027);
  - reciprocal best hit (RBH) orthology of top candidates (20/20);
  - dN/dS on recovered loci (purifying selection expected on real genes);
  - orthogonal engines: phmmer profile-HMM and DIAMOND ORF-blastp concordance;
  - micro-synteny scan (expected negative in deserts; logged honestly).

## 4. AEES (Assembly-aware Evolutionary Evidence Score), frozen weights

For a gene's best locus:
  bitscore_norm = min(total_bits/500, 1)
  qcov          = query coverage of best locus in [0,1]
  pident        = best percent identity / 100
  concordance   = 1.0 (both T. dohrnii assemblies), 0.5 (one), 0.0 (none);
                  single-assembly genomes redistribute the weight proportionally
  AEES = 0.35*bitscore_norm + 0.25*qcov + 0.15*pident + 0.25*concordance
Weights frozen in jellyfish/xaees.py before outcomes were read; sensitivity
analysis (amendment #7) shows rank stability under weight perturbation
(top-5 overlap 4.21/5 over random weightings).

## 5. Complexity

Let q = number of queries (125 here), G = assembly size in residues, H = number
of returned HSPs. Mapping is the q independent tblastn runs (embarrassingly
parallel); clustering is O(H log H) per scaffold; scoring is O(genes). The whole
workflow runs on 2 cores / 2 GB RAM for ~500 Mb assemblies in hours
(demonstrated in this repository), i.e. it is cheap enough for a student laptop.

## 6. Failure modes and mitigations

- Mislabeled source accessions -> S0 verification + quarantine (D9: 37/47
  NCBI-fetched queries were mislabeled; caught by panel audit, fixed, rerun).
- Assembly gaps -> two-assembly concordance; "not detected" labeling, never
  "absent"; gap-explicit AEES concordance component.
- Query-target distance -> cross-species query set X (cnidarian queries find
  loci the human query misses: the ATG5 pattern).
- ORF fragmentation (for ORF-space engines) -> disclosed sensitivity asymmetry;
  concordance read on significance + best-locus identity, not raw counts.
- Multi-domain count inflation (profile engines) -> same disclosure.
- Contamination -> assembly-level contamination screen (FPI, amendment #4).

## 7. Framework benchmark (item 10)

The workflow itself is benchmarked, not just its findings:
- arm 1 (query expansion): GFAR full set vs human-query-only mapping of the same
  panel on the same assemblies: 35/47 vs 27/47 multi-copy genes recovered -
  the cross-species expansion is worth +8 genes.
- arm 2 (desert standard): GFAR vs the standard desert route (de novo
  transcriptome/ab initio prediction with available data): 35/47 vs 0/47 - the
  standard route recovers nothing on these assemblies without training data.
- Orthogonal reproduction: phmmer reproduces 20/20 significant calls and the
  exact ATG5 3-locus pattern; the workflow's conclusions are engine-independent.

## 8. Pseudocode

  for assembly in assemblies:
      db <- tblastn_db(assembly)
      for query in verified_panel(P, X):
          hsps <- tblastn(query, db, e=1e-10)
          loci <- cluster(hsps, min_bits=100, merge_gap=500bp)
          ledger[assembly][gene(query)] <- loci
  for gene in panel:
      n_strong <- count(loci with total_bits >= 100)
      significant <- n_strong >= 3
      aees <- 0.35*bits + 0.25*qcov + 0.15*pident + 0.25*concordance
  run validation battery (S6); report with honest-negative register
