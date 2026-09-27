# Findings register (2026-09-27) - every claim linked to result files

## Verified positives
1. H1 SIGNIFICANT: 20/24 aging/longevity panel genes map to strong loci in T. dohrnii
   (binomial vs shuffled-control rate, p=1.0e-38, BH q=2.0e-38). File: results/x-stats.json (H1_panelB).
   Absent (labeled not-detected): APOE, CDKN2A, IGF1, PRKAA1.
2. H2 SIGNIFICANT: 18/24 neurodegeneration panel genes map (p=2.0e-33, q=2.0e-33).
   Absent: APOE, GBA, MAPT, PARK7, SNCA, UBQLN2. File: results/x-stats.json (H2_panelC).
3. Controls PASS. Negative: 0/125 shuffled queries with strong locus in each of 5 genomes
   (FPR 0.0; manually spot-verified 3 shuffled queries -> zero raw HSPs vs Tdohrnii DB).
   Positive: 52/60 closed-phase calls reproduced, 8 mismatches ALL gains (superset queries), 0 losses.
   Files: results/x-ledger-bcshuf.json, results/x-stats.json (H6_*), docs/X-DEVIATIONS.md D5.
4. BENCHMARK BEAT (arm 1): multi-species queries beat human-only on Clytia calibration,
   38/47 (80.9%) vs 29/47 (61.7%) recall, paired re-analysis of identical tBLASTn output.
   File: results/x-benchmark-recall.json. 9 genes recovered only via cnidarian queries.
5. BENCHMARK BEAT (arm 2): genome-first beats database-first on T. dohrnii panel genes,
   38/47 vs 0/47 (live NCBI eutils audit 2026-09-27: 0 gene + 0 protein records for all 47
   panel genes). Files: results/x-desert-audit-bc.json, results/x-stats.json (presence_counts).
6. Named discovery candidate: ATG5 - highest AEES (0.860), both T. dohrnii assemblies,
   2 strong loci, 69% query coverage; autophagy-core gene invisible to the human-only arm.
   Supporting: SIRT1, SIRT6, GRN (strongest single alignment, 8299 bits).
   Files: results/x-aees.json, results/x-ledger-bc.json. Validation plan: paper section 08c.

## Honest negatives (equal prominence)
7. H3 NEGATIVE: no panel-B gene shows T. dohrnii-enriched copy expansion after BH
   (copy-share Fisher per gene; INSR runs opposite, 31 Td vs 67 mortal). File: results/x-stats.json (H3).
8. H4 NEGATIVE: presence matrix does not separate rejuvenating from non-reverting species
   (exact label permutation, 6 assignments, p=0.333; assembly-redundancy caveat). File: results/x-stats.json (H4).
9. H5 near-vacuous by construction (panels share only APOE, undetected); reported, D4.
10. Annotation desert confirmed again for panels B+C (47/47 genes: zero database records) -
    a boundary result about public databases, not about the organism.

## Methodological additions (judge-round novelty, logged)
11. AEES v1 (round R1): assembly-aware evidence scoring; jellyfish/xaees.py, results/x-aees.json.
12. Benchmark arms 1-2 (this register 4-5).

13. FPI fragmentation control (P1 #4): T. rubra shredded to 49,860 mock scaffolds matching the
   74,835-scaffold assembly's profile; 37/39 recoverable genes survive, FOXO3 + NFE2L2 lost,
   FPI = 0.0513. Files: experiments/x_frag.py, results/x-frag.json.
14. Housekeeping completeness + normalization (P1 #15): 12 coreg genes recovered in full in all
   8 genomes (11/11 where the query panel has 11); correction factor 1.0, normalized call rates
   identical to raw. File: results/x-ledger-coreg.json.
15. Rejuvenation panel extension (ext2) - HONEST NEGATIVE: 12 reversal-literature genes map in
   all 8 genomes, mean identity 64.5-71.2%, no separation of non-senescent vs mortal lineages;
   mortal M. virulenta tops the identity band. Sharpens claims to duplication structure +
   module signal quality. File: results/x-ledger-ext2.json.
16. dN/dS exploratory (P1 #3): NG86 pairwise Td vs Trubra, top-10 AEES genes; 6/10 estimable,
   all omega<1 (ATG7 0.066, ATG5 0.124, SIRT6 0.147, GRN 0.350, TARDBP 0.434, PSEN1 0.835);
   APP/GHR/SIRT1/VCP dS-saturated. ATG5 duplication maintained under purifying selection, not
   eroding. Files: experiments/x_dnds.py, results/x-dnds.json.
17. Evidence tiers (P1 #19): 38 panel genes tier 1; top-10 tier 2 (RBH 20/20); 9/10 tier 4
   (external aging DB); TARDBP tier 2 only; tier 3 (expression) empty pending SRA.

## Deviation D8 (overwrite bug, logged in X-DEVIATIONS.md)
x_map.py overwrote result files on subset reruns, wiping coreg/ext2 5-genome ledgers and (via a
pre-patch frag run) the bc ledgers. bc ledgers restored from git; merge-on-write patch committed;
repair chain rerun reproduced 100% completeness on every genome (verified 2026-09-27, commit
04a5091). All downstream numbers in this register use the repaired ledgers.

## Paper
paper/MEGA27-26b-EXPANSION.docx: 23,016 body words -> 61 rendered body pages (body-only rule:
headings/refs/appendix/diagrams excluded), 12pt Times New Roman, 1.5 spacing. Count methodology:
results/x-papercount.json; rendered PDF inspected visually (pages 2-3, 26).

## 2026-09-27 extension-genome contrast (exploratory) + RBH control
- bcext mapping complete: Nvectensis 284 strong loci/42 genes, Mvirulenta 171/41, Hvulgaris (results/x-ledger-bcext.json).
- ATG5: universal across all 8 genomes. Td duplication (2 loci, both assemblies, concordant stats) vs 1 in Trubra. But Clytia 2, Nvectensis 4 - copy number alone does NOT track immortality (claim narrowed).
- Signal quality tracks non-senescence: Hvulgaris best ATG5 (98.4% pident, qcov 0.79), Td next (0.69); mortals Aaurita (216 bits) and Mvirulenta (201 bits) weakest. n=2 per class - pattern, not statistic.
- Module: ATG7/BECN1 intact everywhere; Hvulgaris ATG7+BECN1 100% pident.
- NEW CONTROL (judge S5): reciprocal-best-hit 20/20 PASS on top-10 AEES genes x both Td assemblies (results/x-rbh.json). Orthology confirmed incl. duplicated ATG5 loci.
- ATG5 validation: step1 PASS, step2 PASS, step3 PASS-with-narrowing, step4 (SRA raw reads) OPEN.

## 2026-09-27 provided-verdict amendments (fast items landed)
- P1 archived: judge gate MET 1 of 1 provided (X-JUDGE-ROUNDS.md, wamid ...OEI5RgA=); queue docs/X-AMENDMENTS-P1.md locked pre-execution.
- Item 7 (AEES weight subjectivity): sensitivity analysis (results/x-aees-sensitivity.json). ATG5 rank = 1 under frozen AND equal weights; under 200 random weightings rank ranges 1-27 (mean top-5 overlap 3.71/5). Honest read: frozen top-5 core (ATG5, APP, ATG7, PSEN1, GHR) is robust to reasonable weightings; extreme weightings reshuffle - disclosed.
- Item 17 (enrichment framework): Fisher exact tests of aging-DB membership among high-AEES (>=0.75, n=20/44) genes (results/x-enrichment.json). NEGATIVE on all 4 databases (GenAge human OR 1.33 q=0.771; GenAge models OR 2.44 q=0.763; CellAge OR 0.82 q=0.771; LongevityMap OR 0.56 q=0.763). Disclosed confound: the universe is the aging-biased panel itself, so within-panel enrichment is weak by construction; the unbiased genome-wide arm (item 16) is the non-circular test.
