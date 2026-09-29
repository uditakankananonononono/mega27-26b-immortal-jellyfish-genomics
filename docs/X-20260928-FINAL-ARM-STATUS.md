# 26b final-arm status, 2026-09-28 12:40 IST

All four arms were separately locked before their new computations in
X-20260928-{A,B,C,D}-LOCK.md. This is a research-progress status, not a
final judge PASS. The A-D results were integrated into the corrected Sep 28 research draft at
repository commit 0ea4b4e (subsequent source-ledger commits do not alter the PDF).
Private Drive PDF ID 1Rm3TpzFnK3SSQpkWsc2VxQhmFpGajqrk and editable DOCX ID
1v_y39hU4CokskEVzx3DhQLEn0CjnB3vz are the current versions. The later
reversal-pivot feasibility audit is in X-20260929-REVERSAL-PIVOT-FEASIBILITY.md
and is not a computed biological finding.

A, panel-free discovery: 23,314 Kyushu high-confidence T. dohrnii predicted
proteins and 9,324 independently published T. rubra predicted proteins, no
GenAge selection. Low-memory MMseqs easy-linclust at locked 30% identity/70%
both coverage produced 24,270 provisional clusters; 85 with M>=3/R>=1;
top-20 frozen before independent Oviedo/Clytia predicted-protein search.
All top-20 all-cluster BH q values are 1.0; annotation totals differ sharply,
and holdout representative hits are not family orthology/unique-locus proof.
No structurally validated enriched family: gate FAIL, not a discovery.
Results: x-20260928-A-train-ranking.json, x-20260928-A-holdout.json.

B, ATG5: full ENA PacBio DRR267480 source verified at 3,594,233,174 bytes,
MD5 8481187208c3a4892fea222346c02c46. All 1,704,140 subreads mapped
against one global full-genome minimap2 index (the split-index pilot was
invalidated and discarded). 12 primary MAPQ60 reads cross 267 bp at copy A,
27 at copy B; zero at either copy span >=5 kb on BOTH flanks, so the locked
structural resolution gate FAILS. Crossing reads appear in consecutive DRR
ordinal blocks, not verified independent ZMWs. Extra copy remains UNRESOLVED,
not biologically refuted or proven. Result: x-20260928-B-structural.json.

C, RNA: nine paired stage runs, 35,894,929,318 compressed bytes; one ENA
BioSample per stage across the three individual-labeled experiments. Study
calls them biological triplicates but run-level accession identity does not
prove independent specimens/extractions. Main-assembly HC GFF and proteins
are available. No complete full-genome fragment count matrix or DE run, so
no stage expression claim. See X-20260928-C-INDEPENDENCE-STATUS.md.

D, reproducibility: clean-clone source-verified genome + HC protein/GFF fetch,
local BLAST DB build and one ATG5 raw query smoke passed; manifest and exact
hashes are committed. No full raw pipeline reproduction; absolute paths and
resource requirements remain. See X-20260928-D-BOOTSTRAP-STATUS.md.

Next: seek a truly independent high-contiguity assembly or phased molecular evidence if the structural ATG5 question is to be pursued further; seek per-run RNA specimen provenance rather than assume it from experiment titles; and make the full raw pipeline portable in a sufficiently provisioned environment. A's null result must be kept and not tuned into a positive. All-issues PASS is not established.
