# Deviations from pre-registration (locked 08d8be0) - expansion run 2026-09-26/27

Frozen: panels, thresholds (evalue 1e-5, 50kb span, 100 bits), hypotheses H1-H6,
test FAMILIES (binomial-vs-control, Fisher per gene BH, exact label permutation,
Fisher overlap), controls. Nothing below changes a frozen panel, threshold, or
hypothesis; every item is logged, nothing silently merged.

## D1. H1/H2 control-rate constant - implementation bug fixed on first stats run
The coded continuity constant divided by the number of shuffled GENES WITH HITS
(0), yielding p0=1.0 and degenerate p=1.0. The frozen test is "binomial vs
control rate"; the control rate comes from the 125 shuffled QUERIES. Fixed to
p0 = max(FPR, 1/126) = 0.00794 (conservative upper bound, FPR observed 0/125).
Fix made once, before any results were reported; the degenerate output is in
git history (pre-patch x-stats.json superseded).

## D2. H3 Fisher table - implementation bug fixed on first stats run
The coded per-gene table was single-binary 2x2 ([[td>=2, td<2],[ot>=2, ot<2]]),
which is always p=1.0 (non-test). The frozen test is a per-gene copy-signal
contrast by Fisher exact. Implemented as copy-share: 2x2
[[td_copies, other_copies],[td_total - td_copies, other_total - other_copies]]
(Td = 2 assemblies pooled max, others = T. rubra + A. aurita pooled). Result:
no gene survives q<0.05 - H3 is an HONEST NEGATIVE (no T. dohrnii-enriched
copy expansion in panel B).

## D3. H4 permutation count
Prereg text says "all 30 permutations of 4 labels"; the exact number of
distinct label assignments of 4 genomes into groups of 2 is C(4,2)=6 (3 up to
symmetry). The code enumerates all 6 exactly - the prereg's "30" was a
counting slip; the frozen TEST (exact label permutation) is unchanged.
H4 result: stat -0.038, p=0.333 - HONEST NEGATIVE, no aging-strategy
separation of the presence matrix. Assembly-redundancy caveat kept.

## D4. H5 near-vacuity disclosed
Panels B and C share exactly one symbol (APOE), so the frozen overlap test is
close to vacuous: observed overlap 0 (APOE not detected), Fisher p=1.4e-6
(significantly LESS than independence). Reported as-is; scientifically the
shared-maintenance question is better addressed by the exploratory
pathway-level analysis (future arm), not by re-tuning this test.

## D5. H6 positive control: superset reproduction
52/60 closed-phase panel-A calls reproduced exactly; the 8 mismatches are ALL
gains (closed: not detected, now: detected: ERCC2/TERF2/XRCC5 in both T.
dohrnii assemblies, ERCC2/XRCC5 in A. aurita) - zero losses. Cause: the actrl
query set (133 proteins incl. additional cnidarian homologs) is a superset of
the closed-phase queries. Judged PASS (reproduction with improved recall),
not a frozen-criterion change. Negative control: 0/125 shuffled queries with
a strong locus in every genome (FPR 0.0, <=5% criterion met); spot-checked
manually (3 shuffled queries vs Tdohrnii DB: zero raw HSPs) so the zero is
real, not an empty-run artifact.

## D6. Extension datasets (post-prereg, exploratory only)
N. vectensis, M. virulenta, H. vulgaris assemblies added 2026-09-27 as
exploratory datasets 6-8. They are NOT part of frozen H1-H6 inputs and will
be used only in clearly-labeled exploratory arms.

## D7. AEES scoring layer (post-hoc, additive)
AEES v1 (jellyfish/xaees.py, judge round R1 novelty) is an additive scoring
layer over frozen pipeline outputs; it does not change presence/copy calls
used in H1-H6. Reported as exploratory.

## D8 (2026-09-27 10:23): x_map result-file overwrite (implementation bug, found pre-report)
Second invocations of x_map.py with a genome subset (ext2 on 3 ext genomes; coreg-ext on
3 genomes) OVERWROTE results/x-tblastn-{set}.json and results/x-ledger-{set}.json, wiping
the 5-H-input-genome results from the first invocation. Caught before any ext2/coreg-ext
per-gene claim was reported (an intermediate local table showing zeros for H-input genomes
was this artifact, not biology, and was never reported). Fix: merge-on-write in x_map.py
(existing keys preserved, new keys updated). Repair: full coreg+ext2 rerun on the 5 H-input
genomes chained after the FPI run (/tmp/xround2c.sh, ends R2CDONE); the frozen pipeline is
deterministic (fixed seed only affects shuffled set), so regenerated ledgers must reproduce
the already-reported coreg detection rates (12/12 both Td assemblies, 12/12 Trubra,
12/12 Aaurita, 11/12 Clytia) - they will be re-verified against those numbers before
anything downstream uses them.
