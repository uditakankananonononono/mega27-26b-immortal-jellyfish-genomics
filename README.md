# mega27-26b-immortal-jellyfish-genomics
Comparative genomics of DNA-repair/telomerase pathways across aging-resistance strategies.
- Verified finding: T. dohrnii and A. aurita have ZERO gene-level records for the 18-gene repair/telomerase panel in NCBI nucleotide/gene/protein (synonyms tried) and near-zero UniProt coverage - only raw genome assemblies exist (e.g. GCA_051903475.1). The literature hypothesis (Pascual-Torner et al. 2022, PNAS: repair-gene expansions) is therefore not directly reproducible from public gene databases - documented as a boundary result.
- Executable arm: human (aging reference, 17/18 genes) vs Hydra vulgaris (non-aging regenerative cnidarian, 16/18) real RefSeq mRNAs: GC/codon/4-mer signature comparison + copy-number signals.
Run: `pip install -e . && pytest && python experiments/fetch_data.py && python experiments/analyze.py`
