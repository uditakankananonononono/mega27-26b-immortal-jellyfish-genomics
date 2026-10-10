# TD-1 within-line descriptive TPM reproduction v1
Wound+fasting confounded; 0h post-cut; c/s anatomy unverified. No causal aging/neurology or independent-validation inference.

Complete outputs cover the fixed 23,314 HC genes and 34 source TPM columns. The group table has 233,140 rows (10 groups per gene). Terminal paired differences have 69,942 rows (three s-minus-c pairs per gene). Original 33h labels 1/2/4 and 51h c/s suffixes are preserved. Earlier time labels are not matched longitudinally. No ranking, target shortlist, ratio, pseudocount, count model, p-value, FDR, enrichment or outcome interpretation was performed.

All emitted rows were read back and compared with frozen source cells, with independently sorted median arithmetic. Binary64 values use repr serialization; source precision is bounded by that representation. No renormalization, imputation or gene/sample removal. This is numerical reproduction of the published normalized table, not validation of source measurements or original Salmon computation.

Inputs: public S1-S9 workbook, SHA256 4d66ba83b3ec03c8dffdf92c1823001cb6bef4c06cd64fadf559ecf4b4429f5b; ordered gene-ID hash 0c18805043209c4dc6fc860af93c03eace910dd2f3d6b024ad1fb08d40f6b908. S10 and raw reads were not downloaded.

Source: https://ftp.ebi.ac.uk/pub/databases/biostudies/S-EPMC/754/S-EPMC9835754/Files/dsac047_suppl_supplementary_table_s1-s9.xlsx
Methods: https://www.ebi.ac.uk/europepmc/webservices/rest/PMC9835754/fullTextXML
Run metadata: https://www.ebi.ac.uk/ena/portal/api/filereport?accession=PRJDB11116&result=read_run&fields=run_accession,sample_accession,experiment_title,library_name,library_strategy&format=tsv

execution-audit.json records output hashes and row counts. This package contains no result-signing clearance or biological approval claim. The old blind arm remains closed.
