# Arm C: RNA replicate identity audit and resource status

The ENA PRJNA603209 read-run report, retrieved 2026-09-28, lists nine distinct
experiment/run accessions, each with paired FASTQ files, totaling 35,894,929,318
compressed bytes. Three experiment titles per stage end in Polyp1/2/3,
Medusa1/2/3 or RevPolyp1/2/3 "individual". The public study description at
https://seqout.org/p/SRP245133 says "biological triplicates". Yet ENA attaches
all three polyp experiments to **SAMN13924705**, all medusa experiments to
**SAMN13924706**, and all reverted-polyp experiments to **SAMN13924707**.
Each BioSample itself describes biological triplicates in a stage-level text
field, but the record does not bind each run to an independently collected
individual or distinct extraction. Thus the run titles support but do not
verify biological independence, and the sample accession structure is
ambiguous. The nine-run manifest records the exact titles, run/sample links,
FASTQ URLs, byte sizes and MD5. This is not evidence that the runs are technical
replicates; it is a reason not to assert independence from metadata alone.

Kyushu's provider publishes an HC GFF3 with 23,314 gene predictions and
matching protein sequences on the main genome:
https://mogt.agr.kyushu-u.ac.jp/turritopsis/download.html . It contains
models overlapping both main-assembly ATG5 loci, but prediction on the same
assembly is not independent structure or expression validation. A complete
paired-read, gene-model-aware differential-expression analysis at the locked
n>=3 independent-biological-sample gate has **not** run. The nine compressed
paired libraries are ~35.9 GB, versus ~5.5 GB free here while preserving the
prior pilot reads; an available disk alone would not resolve replicate identity.
A separate 2019 cyst/polyp/medusa study (PRJNA563171) has mismatched
collection locality, platform/library prep and pooling and explicitly says its
assemblies cannot detect transcript-level differential expression; it cannot
be quietly combined as biological replicates for PRJNA603209.

Status: source/model discovery landed; no inferential DE, no ATG5 upregulation
claim. To pass: independently verified per-library biological sample provenance,
adequate scratch/compute, complete paired reads, full-genome gene-level count
matrix with unique/multimapping rules and preregistered QC, then locked design
and BH/FC gates. If provenance cannot be established, remain descriptive.

Primary records: https://www.ebi.ac.uk/ena/portal/api/filereport?accession=PRJNA603209&result=read_run ;
https://www.ebi.ac.uk/ena/browser/api/xml/SRX7633170 ;
https://www.ebi.ac.uk/ena/browser/api/xml/SAMN13924705 ;
https://pmc.ncbi.nlm.nih.gov/articles/PMC6893190/ .
