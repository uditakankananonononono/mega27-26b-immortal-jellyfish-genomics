# Findings register (2026-09-27, POST-D9 revised) - every claim linked to result files

D9 REVISION NOTE: entries 1-6 were recomputed on 2026-09-27 after the D9 query-integrity
repair (37 mislabeled human query proteins replaced with UniProt-verified orthologs;
docs/X-DEVIATIONS.md D9). Revised values below supersede the pre-D9 numbers. Every revised
number reproduces from results/*.json at the D9-closure commit.

## Verified positives
1. H1 SIGNIFICANT: 20/24 aging/longevity panel genes map to strong loci in T. dohrnii
   (binomial vs shuffled-control rate, p=1.0e-38, BH q=2.0e-38). File: results/x-stats.json (H1_panelB).
   Absent (labeled not-detected, all with verified queries): APOE, CDKN2A, GHR, IGF1.
   Composition changed vs pre-D9 (PRKAA1 gained, GHR removed); count unchanged.
2. H2 SIGNIFICANT: 16/24 neurodegeneration panel genes map (p=1.7e-28, q=1.7e-28).
   Absent: APOE, BDNF, GBA, MAPT, NGF, PRNP, SNCA, TREM2. File: results/x-stats.json (H2_panelC).
   Revised from 18/24: PARK7 + UBQLN2 gained, BDNF/NGF/PRNP/TREM2 removed (artifact detections).
3. Controls PASS. Negative: 0/125 shuffled queries with strong locus in each of 5 genomes
   (FPR 0.0; shuffles are panel-independent, unaffected by D9). Files: results/x-ledger-bcshuf.json,
   results/x-stats.json (H6_*), docs/X-DEVIATIONS.md D5.
4. BENCHMARK BEAT (arm 1): multi-species queries beat human-only on Clytia calibration,
   35/47 (74.5%) vs 27/47 (57.4%) recall, paired re-analysis of identical tBLASTn output
   (revised from 38/47 vs 29/47; beat holds). 8 genes recovered only via non-human queries.
   File: results/x-benchmark-recall.json.
5. BENCHMARK BEAT (arm 2): genome-first beats database-first on T. dohrnii panel genes,
   35/47 vs 0/47 (live NCBI eutils audit 2026-09-27: 0 gene + 0 protein records for all 47
   panel genes; revised from 38/47). Files: results/x-desert-audit-bc.json, results/x-stats.json.
6. Named discovery candidate: ATG5 - AEES 0.860 (rank 2 of panel, behind SOD1 0.862; rank
   stable under frozen + equal weights); ATG5 present in both T. dohrnii assemblies, but see
   entry 22: the second cnidarian-type copy is main-assembly-only and unresolved;
   T. rubra carries exactly one fewer in each query class (453 + 300). The duplication signal
   survived the D9 repair and is corroborated by two independent query classes.
   SOD1 is a new repair-promoted candidate (full-length alignment, 69.5% identity, both assemblies).
   GHR withdrawn: its pre-repair loci belonged to a mislabeled query (IGFALS).
   Files: results/x-aees.json, results/x-ledger-bc.json. RBH 20/20 on the new top-10 (results/x-rbh.json).
   dN/dS post-repair: 7/10 estimable, all omega<1 (ATG5 0.030, ATG7 0.066, SIRT6 0.147,
   GRN 0.350, TARDBP 0.434, VCP 0.437, PSEN1 0.835). File: results/x-dnds.json.

18. Decoy control (P1 #11): 23 verified non-aging decoy genes through the frozen pipeline;
   8-10/23 map per genome (35-43%) vs panel-B 20/24 (83%) in Td, Fisher p=0.0027. Mapped
   decoys are exactly the genes with genuine cnidarian homologs (ACTA1/DMD/MYH7/TTN muscle,
   OPN1LW/RHO opsins, SLC26A5, OR1A1) - the panel's high mapping rate reflects ancient
   conservation, not pipeline laxity. Files: data/xpanel_decoy/, results/x-decoy.json,
   results/x-ledger-decoy.json.
19. ATG5 micro-synteny (P1 #13) - HONEST NEGATIVE-LEANING: ORF-level flanking analysis
   (+/-40kb) finds 1/41 Td flanking ORFs conserved in T. rubra and 0-1/41 in all other
   genomes; no conserved syntenic block surrounds ATG5, so the duplication claim rests on
   concordant copy counting + RBH + purifying selection, not neighborhood conservation.
   File: results/x-synteny.json.

20. Orthogonal-engine concordance (P1 #12): the panel's calls do not depend on BLAST.
   phmmer profile-HMM search on T. dohrnii (286,785 six-frame ORFs >=75aa) reproduces
   all 20/20 tblastn-significant genes with 27/36 best-locus overlap; ATG5 is recovered
   as exactly 3 loci in the main assembly, matching the frozen pipeline's 3 strong loci
   there (confirms sequence presence in that assembly; the duplication-vs-haplotig
   question is entry 22, not settled by engine concordance). DIAMOND blastp against six-frame ORF
   translations of all five genomes confirms direction with lower sensitivity
   (best-locus overlap 16/6/9/3/24 of 36 per genome); the shortfall is the ORF-cutting
   step (domains split across <75aa fragments are invisible to blastp), disclosed as
   method asymmetry. phmmer locus counts run high on multi-domain genes (WRN 120) -
   significance concordance, not raw counts, is the comparable metric. Files:
   results/x-concordance-hmmer.json, results/x-concordance-diamond.json.

21. GFAR formalization (P1 #1/#10): the workflow is now a named, specified method
   (docs/X-ALGORITHM.md): verified inputs, frozen stages, AEES weights, complexity
   (2 cores / 2 GB RAM for ~500 Mb assemblies), six failure modes with mitigations,
   and a framework-level benchmark (arm1 35/47 vs 27/47; arm2 35/47 vs 0/47;
   phmmer 20/20 reproduction of significant calls). Paper section 05e.

22. ATG5 second-copy validation (D9 follow-on) - EXTRA COPY UNRESOLVED:
   Two cnidarian-type loci in the main Td assembly are 97.1% identical over 665bp;
   only one is recovered on the highly fragmented Oviedo assembly. The independently
   sourced PacBio DRR267480 depth test is now complete (852,070 systematically
   thinned odd reads mapped to the full 435.9 Mb genome; results/x-atg5-depth.json,
   experiments/x_atg5_depth.py). The genome-wide median across 8,187 complete
   50kb windows is 9.158x. At mapq>=30, copyA (BQMF02000106.1:66386-66652)
   depth is 7.483x, or 0.817x background; copyB (BQMF02000418.1:205689-205955)
   depth is 12.0x, or 1.310x background; the divergent human-detected paralog
   depth is 22.44x, or 2.450x background. Dedupe 1,368 repeated alignment
   signatures in 883,720 PAF rows; 663,634 alignments meet mapq>=30 and >=500bp.
   Depth varies sharply within 5kb flanks; locus spans are only 267bp. The
   frozen decision rule (both copies ~0.5x for haplotig, both ~1x for real
   duplication) is NOT met uniformly. This is an INCONCLUSIVE test, not
   validation of either scenario. ATG5 remains a candidate under direct
   structural validation; no confirmed extra-copy discovery is claimed.
   A better assembly/phased reads or locus-spanning long-read analysis is needed.

23. Broader but still list-based GenAge arm phase 1 (P1 #16, PARTIAL rather than panel-free): 302/307 verified GenAge proteins mapped
   on Td main (188/231 detected). AEES top is housekeeping machinery as designed
   (UBB/RAD51/HDAC3/HSPA8); panel NOT enriched at top (MW p=0.35) - disclosed
   honestly. Discovery yield: non-panel GenAge genes with high Td evidence -
   RAD51 0.846, HDAC3 0.817 (+HDAC1/2), CHEK2 0.71, SERPINE1 0.727, SOD2 0.68
   (pairs with rank-1 SOD1). Converges on genome-maintenance/chromatin/redox
   modules. Oviedo/Trubra phase 2 complete: 188 strong genes per Td assembly (184 shared); Trubra 192 strong, 177/184 shared Td calls also strong in congener. The seven Td-shared/Trubra-nonstrong calls are NOT species-specific proof. Frozen AEES rerank p=0.356 (still not enriched); RAD51 0.971, HDAC3 0.942, SOD2 0.811 with Oviedo agreement. File: results/x-genage-aees.json and results/x-ledger-genage.json.

24. P1 #6 exploratory RNA-seq subsample - ATG5 EXPRESSION INCONCLUSIVE: complete
   ENA mates for Medusa1/Polyp1/RevPolyp1 verified against source bytes; fixed
   every-100th-pair sample mapped against 40 target labels (37 merged windows).
   Main-assembly cnidarian-type ATG5 copy A/B read-end counts by stage:
   Medusa 5/0, Polyp 9/2, reverted polyp 3/1; all cells below preregistered
   10-read-end threshold. Read-end sums are NOT paired fragments; ACTA1
   dominates this target-enriched reference and gene spans include +/-2kb
   non-exonic capture. No DE, upregulation or functional claim. Source hashes,
   stage counts, all target labels and limitations in results/x-rnaseq-sample1pct.json;
   method in docs/X-RNASEQ-SAMPLING-LOCK.md, experiments/x_rnaseq_chunk.py.

## Deviation D8 (overwrite bug, logged in X-DEVIATIONS.md)
x_map.py overwrote result files on subset reruns, wiping coreg/ext2 5-genome ledgers and (via a
pre-patch frag run) the bc ledgers. bc ledgers restored from git; merge-on-write patch committed;
repair chain rerun reproduced 100% completeness on every genome (verified 2026-09-27, commit
04a5091). All downstream numbers in this register use the repaired ledgers.

## Paper
paper/MEGA27-26b-EXPANSION.docx: 25,352 body words -> 67 rendered body pages (body-only rule:
headings/refs/appendix/diagrams excluded), 12pt Times New Roman, 1.5 spacing. Count methodology:
results/x-papercount.json; rendered PDF inspected visually (pages 2-3, 26).

## 2026-09-27 extension-genome contrast (exploratory) + RBH control
- bcext mapping complete: Nvectensis 284 strong loci/42 genes, Mvirulenta 171/41, Hvulgaris (results/x-ledger-bcext.json).
- ATG5: universal across all 8 genomes. Td main shows 2 cnidarian-type loci, Oviedo and Trubra each 1; the extra main-only copy is unresolved. But Clytia 2, Nvectensis 4 - copy number alone does NOT track immortality (claim narrowed).
- Signal quality tracks non-senescence: Hvulgaris best ATG5 (98.4% pident, qcov 0.79), Td next (0.69); mortals Aaurita (216 bits) and Mvirulenta (201 bits) weakest. n=2 per class - pattern, not statistic.
- Module: ATG7/BECN1 intact everywhere; Hvulgaris ATG7+BECN1 100% pident.
- NEW CONTROL (judge S5): reciprocal-best-hit 20/20 PASS on top-10 AEES genes x both Td assemblies (results/x-rbh.json). Orthology supported for ATG5-matching loci; whether the extra main-assembly sequence is a distinct copy remains unresolved.
- ATG5 validation: extra-copy step 1 NOT PASSED, step 2 PASS, step 3 PASS-with-narrowing, step 4 PacBio raw-read depth INCONCLUSIVE.

## 2026-09-27 provided-verdict amendments (fast items landed)
- P1 archived: judge gate MET 1 of 1 provided (X-JUDGE-ROUNDS.md, wamid ...OEI5RgA=); queue docs/X-AMENDMENTS-P1.md locked pre-execution.
- Item 7 (AEES weight subjectivity): sensitivity analysis (results/x-aees-sensitivity.json). ATG5 rank = 2 under frozen AND equal weights; under 200 random weightings rank ranges 1-24 (mean top-5 overlap 4.21/5). Honest read: frozen top-5 core (SOD1, ATG5, APP, ATG7, PSEN1) is fairly stable; extreme weightings reshuffle - disclosed.
- Item 17 (enrichment framework): Fisher exact tests of aging-DB membership among high-AEES (>=0.75, n=20/44) genes (results/x-enrichment.json). NEGATIVE on all 4 databases (GenAge human OR 1.33 q=0.771; GenAge models OR 2.44 q=0.763; CellAge OR 0.82 q=0.771; LongevityMap OR 0.56 q=0.763). Disclosed confound: the universe is the aging-biased panel itself, so within-panel enrichment is weak by construction; the broader GenAge arm (item 16) compares a larger set but is still aging-list-selected; a genuinely panel-free background enrichment test remains open.
