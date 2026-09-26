# Pivot ladder for the 26b expansion (user rule 4, 2026-09-26 16:11 IST)
User rule: "A NEGATIVE RESULT IS NEVER THE END: a failed gate/hypothesis triggers a
pivot and the project keeps pushing until there is a useful finding. Honest
negatives stay documented, but they no longer count as project results."

Compatibility with the locked preregistration (main @ 08d8be0): panels,
thresholds, and H1-H6 do NOT change. Pivots are ADDITIONAL post-hoc analyses,
always labeled exploratory, never used to re-tune the pre-registered tests.
The ladder (descending in order until a useful finding lands):
P1. If H3 copy contrasts are null -> domain-level analysis of mapped loci
    (annotated-domain content of the best locus per gene, e.g. kinase, RecQ,
    OB-fold) as the contrast unit instead of whole-gene copies.
P2. If H4/H5 are null -> divergence analysis: pident/qcov distributions of
    mapped loci, T. dohrnii vs comparators, per gene class (maintenance vs
    regulatory), looking for concentrated divergence in rejuvenation-relevant
    genes.
P3. If mapping coverage is thin in Oviedo assembly -> assembly-aware
    reanalysis with fragmentation correction (per-contig normalization),
    separating instrument effects from biology.
P4. Reversal-transcriptome arm: reanalyze the public T. dohrnii life-cycle-
    reversal RNA-seq (Matsumoto 2019 / Pascual-Torner 2022 SRA accessions)
    against the mapped panel loci: do panel genes change expression during
    rejuvenation? This is the strongest orthogonal evidence class available
    publicly.
P5. Cross-panel synthesis: build the maintenance-genome atlas figure/tables
    from whatever mapped, and mine it for the single most defensible novel
    observation (a nomination with locus-level evidence).

Judge rounds (user rule 2): minimum 10 documented weakness-focused judge
rounds on this expansion, logged in docs/X-JUDGE-ROUNDS.md, each round:
weakness found -> fix applied -> evidence of fix.
