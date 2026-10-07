# Source-separated robustness test: provenance gate failed
October 7, 2026. No candidate outcome scoring performed.

The proposed frozen source-separated scoring test was stopped before computing its 47-label outcomes. Source verification found that nonhuman queries for original gained labels were not all the claimed exact genes. Primary NCBI FASTA rereads confirmed:
- TP53-labelled XP_066910575.1 is TP53-binding protein 1-like, not TP53.
- PTEN-labelled XP_066911570.1 is tensin-3-like; XP_065655551.1 is tensin-1. Other PTEN-labelled headers include tensin-2/uncharacterized protein.
- TFEB-labelled XP_048589259.1 is microphthalmia-associated transcription factor. Other TFEB sources are MITF/TFEC-family, not verified TFEB orthologs.

The historical 35/47 vs 27/47 remains a query-label count under the executed procedure. It is NOT eight verified correct target genes recovered. The human identity correction did not resolve these nonhuman query assignments. Earlier statements that all cnidarian queries were intact are not sufficient evidence and are superseded by this audit. No corrected target-recovery count is available; do not subtract labels ad hoc or convert this to a new result.

The locked gate treats unresolved identity for an original winner as blocking the robustness claim; no denominator trimming, changed threshold, or success-bar relaxation. No conservative counts or significance test ran. The full multi-species candidate ledger needs a label/protein-family provenance audit before gene-specific interpretation. Human-only mapping and other independent checks need their own source-specific reconciliation; this audit does not certify or invalidate them wholesale. Submitted manuscript has not been changed.

Live accession files, headers, hashes and exact source URLs are preserved in results/x-20261007-query-provenance/verified-records.json.
