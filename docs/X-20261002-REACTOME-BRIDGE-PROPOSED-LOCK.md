# Proposed lock: human pathway-bridge retention by the jellyfish candidate map
October 2, 2026. Initial proposed plan, before analysis. Budget and symbol-mapping amendments are recorded in the recovery note.

Hypothesis: the frozen 20/24 aging and 16/24 neurology detected-label sets retain more shared curated human pathway membership than equally sized detection sets conditional on each panel's annotation degree. This tests annotation-level prioritization of the existing candidate atlas, not jellyfish pathway function, orthology, rejuvenation or disease protection.

Data availability: Reactome's official current index links NCBI2Reactome_All_Levels.txt and ReactomePathways.txt. Direct reads returned HTTP 200, with human rows containing Entrez ID, stable pathway ID, URL, pathway name, evidence code and species. HGNC's public REST symbol lookup returns approved symbol and Entrez ID (AKT1 verified). Existing x-stats.json supplies frozen panel lists and detections; only corrected final result labels are used, not superseded identity manifests. No numeric pathway overlap outcomes opened. Snapshot complete small mapping files and HGNC responses, record release/date, URL, bytes and SHA256 before analysis. Budget: <=100MB downloads, <=512MB memory, <=10 CPU-minutes. No keys or paid service.

Scope/comparator: both original panels of 24; remove APOE from BOTH panels before assessing bridges to prevent the one deliberately shared label from creating a trivial bridge. Resolve all remaining approved symbols unambiguously through HGNC. Human TAS rows only. Deduplicate gene-pathway memberships. Use leaf pathways only, defined by the official pathway-relation hierarchy; ancestors excluded to avoid generic top-level sharing. Restrict to pathways with at least two distinct panel genes overall. Freeze eligibility from annotation metadata before attaching detection status.

Primary statistic: number of eligible leaf pathways with at least one detected aging-panel gene AND at least one detected neurology-panel gene, divided by the number of eligible leaf pathways with at least one member from each FULL panel. Denominator must be >0.

Null: independently permute detected status within each panel while preserving detected totals and exact annotation-degree strata (0, 1, 2-4, >=5 eligible pathways). 10,000 seeded permutations, seed 261002. Report observed fraction, null mean, difference and one-sided empirical p=(1+#null>=observed)/(10001). Single primary test alpha .05. No secondary significance hunting, no changed bins after results. Enumerate possible allocations per stratum first: if fewer than 100 distinct paired allocations, exact enumeration where feasible; otherwise mark underpowered/no inferential claim rather than relax matching. Report unmapped genes and coverage explicitly.

Falsifier: p>=.05, observed fraction <= null mean, absent eligible bridges, unresolved symbol mapping, or insufficient null allocations means the proposed enrichment is not supported or not testable. Every result, including a negative, is retained. The source annotation is human and the panels were preselected for aging/neurology: even a positive cannot establish a newly discovered biological link or validate jellyfish mechanisms.

Plan review was required before computation. Freeze complete snapshots and exact mapping coverage; any data-format or null-eligibility failure requires renewed plan review without substituting an easier test.

Sources:
https://reactome.org/download-data
https://reactome.org/download/current/
https://reactome.org/download/current/NCBI2Reactome_All_Levels.txt
https://reactome.org/download/current/ReactomePathways.txt
https://rest.genenames.org/fetch/symbol/AKT1