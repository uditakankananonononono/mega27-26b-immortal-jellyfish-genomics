# 26b final-arm status, 2026-09-28 10:36 IST

All four arms were separately locked before their new computations in
X-20260928-{A,B,C,D}-LOCK.md. This is a research-progress status, not a
final judge PASS. The previous audited manuscript remains the last published
Drive revision; these new results have not yet been integrated into a revised
paper.

A, panel-free discovery: 23,314 Kyushu high-confidence T. dohrnii predicted
proteins and 9,324 independently published T. rubra predicted proteins, no
GenAge selection. Low-memory MMseqs easy-linclust at locked 30% identity/70%
both coverage produced 24,270 provisional clusters; 85 with M>=3/R>=1;
top-20 frozen before independent Oviedo/Clytia predicted-protein search.
All top-20 all-cluster BH q values are 1.0; annotation totals differ sharply,
and holdout representative hits are not family orthology/unique-locus proof.
No structurally validated enriched family: gate FAIL, not a discovery.
Results: x-20260928-A-train-ranking.json, x-20260928-A-holdout.json.

B, ATG5: full ENA PacBio DRR267480 source is public (3,594,233,174 bytes,
MD5 8481187208c3a4892fea222346c02c46). An exact-range resumable fetcher
is retrieving it in bounded foreground chunks; current partial bytes are
quarantined, not mapped or interpreted. At this status, 361,758,720 bytes
were saved, far short of the source. No unique-flank read test has run.
Extra copy remains unresolved, same as the audited paper.

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

Next: finish B source fetch/MD5, inspect unique-flank mapping without changing
its lock; seek independent RNA specimen metadata rather than assume from
experiment titles; make the rest of the raw pipeline portable and test full
outputs in a sufficiently provisioned environment. A's null result must be
kept and not tuned into a positive. All-issues PASS is not established.
