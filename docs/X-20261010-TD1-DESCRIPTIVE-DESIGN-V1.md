# TD-1 regeneration descriptive reproduction design v1
October 10, 2026. Review draft. Outcome analysis has not started.

## Decision requested
Review this descriptive protocol before execution. It measures reproducible summaries of the published TPM matrix, not differential-expression significance or a new discovery. It cannot validate the closed Panama reversal experiment or the closed sequence-detection arm.

## Question and claim boundary
What descriptive within-TD-1-line expression summaries can be reproduced from the published complete HC-gene TPM table across cut-zooid regeneration stages, while retaining replicate labels and the terminal tissue split?

Allowed conclusion: a specified pattern of normalized RNA abundance in this published within-line dataset. Forbidden conclusions: rejuvenation efficacy, causal aging/neurology mechanism, independent-colony validation, medusa reversal, wound-specific versus regeneration-specific effects, or count-based differential expression. This protocol is retrospective reproduction of published data, not a prospective preregistered discovery test.

## Frozen inputs
- Primary S1-S9 workbook, 9,506,843 bytes, SHA256 4d66ba83b3ec03c8dffdf92c1823001cb6bef4c06cd64fadf559ecf4b4429f5b.
- S9 A5:A23318 is the fixed universe of 23,314 unique HC gene identifiers in source order. Ordered newline-terminated ID-list SHA256: 0c18805043209c4dc6fc860af93c03eace910dd2f3d6b024ad1fb08d40f6b908.
- S9 G:AN contains 34 sample TPM columns. No annotation-based filtering, target list, alignment, extra genes, universe substitutions or highest-hit selection.
- S2 is the frozen run/sample crosswalk, 34 unique DRR accessions reconciled to the 34 live RNA-Seq runs. The shared BioSample isolate is TD-1. WGS runs are excluded by library strategy, not expression values.
- S10 is not needed for this design and remains undownloaded. S9 already supplies the full approved universe and sample abundance schema.

## Structural audit already completed
23,314 data rows; 23,314 unique nonblank gene IDs; 34 unique TPM headers; all headers match the S2 sample-label set; 792,676 expected TPM cells. All cells are present, numeric, finite and nonnegative; none are formulas, missing, error or string-typed. Only cell validity was tested: no distribution, zero prevalence, ranking, contrast or biological outcome was computed. This audit does not establish measurement accuracy or original normalization fidelity.

## Sample structure
| Sampling group | Original labels | Number of libraries | Treatment in this protocol |
| --- | --- | ---: | --- |
| 0h | 0h-1/2/3/4 | 4 | Post-cut reference, not unwounded control |
| 3h | 3h-1/2/3/4 | 4 | Separate sampled zooids; no longitudinal donor assumption |
| 6h | 6h-1/2/3/4 | 4 | Same |
| 9h | 9h-1/2/3/4 | 4 | Same |
| 16h | 16h-1/2/3 | 3 | Same |
| 20h | 20h-1/2/3 | 3 | Same |
| 24h | 24h-1/2/3 | 3 | Same |
| 33h | 33h-1/2/4 | 3 | Preserve 4; do not invent 3 |
| 51h c | 51h-1c/2c/3c | 3 | Terminal tissue fraction, matched suffix index |
| 51h s | 51h-1s/2s/3s | 3 | Terminal tissue fraction, matched suffix index |

The primary Methods says stolon and dumpling were divided at 51h. Preserve the source c/s labels until their anatomical mapping is explicitly verified. Treat matching c/s indices as paired fractions from three divided individuals, not six independent donors. If later evidence contradicts the suffix pairing, stop before paired summaries and amend the design. Do not assume that suffix 1 at different earlier times means the same individual: extraction is destructive and no longitudinal chain is supplied.

## Descriptive computation, only after review
1. Read the frozen matrix without renormalizing TPM, filling values, imputing or dropping any gene/sample. Zero is a reported value, never missing.
2. Produce a complete gene-by-group summary table for the eight earlier time groups and separate 51h c and s groups. For every gene/group, report source sample labels, library count, median TPM and minimum/maximum TPM. For an even number of observations, median is the arithmetic mean of the two middle observations. Range is descriptive variability, not a confidence interval.
3. For every gene, retain all three terminal paired differences, TPM(s_i) minus TPM(c_i), with pair index and sample labels. Report their median descriptively. Do not pool c/s libraries as n=6 or pretend fractions are independent donor replicates.
4. Publish only the complete all-gene descriptive table as the primary result. No top-N list, significance threshold, responder classification, expression-driven exclusions, pathway enrichment, human disease translation or newly selected candidate mechanism.
5. If a compact view is needed, show sample counts and a workflow/schema diagram only. Any later expression plot or requested gene subset needs a separately reviewed display selection rule before plotting. Do not select genes after seeing summaries.

No fold-change ratios, pseudocounts, zero-based on/off claims, count models, p-values, FDR, confidence intervals, resampling, causal claims or sample-distance clustering are part of v1. No TPM group-composition comparison is interpreted as absolute RNA quantity. This keeps the result below the inference line and avoids rescuing the prior failed assay.

## Execution gates and stop rules
- Review acceptance must name this version and intended outputs. Design review is not result validation; no analysis starts from this draft alone.
- Before execution, confirm source workbook hash, ordered gene universe hash, original headers and crosswalk. If any differ, stop and report the mismatch; do not silently update input versions.
- Stop if missing/nonfinite/negative values, duplicate IDs/headers, labels absent from the crosswalk or changed source bytes appear. No silent cleanup.
- Stop the terminal paired component if pairing is contradicted or anatomical labels are needed but unverified. Other approved descriptive work can remain separate.
- No downloads of S10, raw reads or new matrices; no alignment, external target discovery, spending, public filing or contact with authors under this unit.
- Preserve source precision in the machine-readable output; any rounded display must be labeled and never feed back into computation.

## Limits that survive a clean execution
All samples are described as TD-1 line and share the TD-1 BioSample. There is no independent-colony holdout. Cutting and prior fasting are part of the experiment; 0h is immediately post-cut. There is no unwounded or matched fasting-only comparator here. Temporal/tissue composition and wound responses cannot be separated from regeneration. TPM is compositional normalized abundance, not raw count data or absolute expression. The experiment and its expression results were already published. Descriptive reproduction does not establish novelty or biological mechanism.

## Planned deliverables after execution is separately approved
- Complete all-gene group-summary TSV and complete terminal paired-difference TSV.
- Frozen crosswalk and input/hash manifest.
- Audit note documenting exclusions (none permitted), original labels, terminal pairing and limitations.
- Readback verification of output row counts, columns, preserved gene/sample identities and selected arithmetic spot checks. No independent biology/result-signing clearance implied.

## Sources
Published methods/supplement identity:
https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9835754/fullTextXML
https://pmc.ncbi.nlm.nih.gov/articles/PMC9835754/

Verified workbook:
https://ftp.ebi.ac.uk/pub/databases/biostudies/S-EPMC/754/S-EPMC9835754/Files/dsac047_suppl_supplementary_table_s1-s9.xlsx

Live RNA/WGS metadata and isolate:
https://www.ebi.ac.uk/ena/portal/api/filereport?accession=PRJDB11116&result=read_run&fields=run_accession,sample_accession,experiment_title,library_name,library_strategy&format=tsv
https://www.ebi.ac.uk/ena/browser/api/xml/SAMD00275467

Public supplement inventory:
https://www.ebi.ac.uk/biostudies/api/v1/studies/S-EPMC9835754
https://www.ebi.ac.uk/biostudies/api/v1/studies/S-EPMC9835754/info
