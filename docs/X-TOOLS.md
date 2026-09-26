# X-TOOLS — External tools, databases and APIs executed (master-spec gate: 40+)

Every entry below was actually executed in this project (expansion phase unless marked
[closed phase]); evidence files are cited. Gate: 40+ external tools. Count here: 41
(25 databases/APIs + 15 software tools + 1 external judge). AnAge bulk download was
attempted twice (404, host removed the dataset) and is logged but NOT counted.

## Databases / APIs (25)
| # | Resource | Use | Evidence |
|---|----------|-----|----------|
| 1 | NCBI GenBank/nuccore (FTP+eutils) | 8 assembly downloads, sequence fetch | data/README-X.md, genomes/sha256.txt |
| 2 | NCBI SRA | 60-run transcriptome census | results/sra_census.json |
| 3 | NCBI Gene | desert audit: panel gene records | results/x-desert-audit-bc.json |
| 4 | NCBI Protein | desert audit: protein records | results/x-desert-audit-bc.json |
| 5 | NCBI Taxonomy | taxids for 7 species | results/xext/x-ext-ncbi-taxonomy.json |
| 6 | NCBI BioProject | T. dohrnii project census | results/xext/x-ext-ncbi-bioproject.json |
| 7 | NCBI PubMed (eutils) | literature-desert counts | results/xext/x-ext-pubmed-literature.json |
| 8 | UniProt REST | 47/47 panel genes mapped | results/xext/x-ext-uniprot-panel.json |
| 9 | GenAge (human) | 29/48 panel genes are aging genes | results/xext/x-ext-genage-human.json, results/x-aging-annotation.json |
| 10 | GenAge (model organisms) | 20/48 incl. ATG5/ATG7 | results/xext/x-ext-genage-models.json |
| 11 | CellAge | 21/48 senescence genes incl. ATG5/ATG7/BECN1 | results/xext/x-ext-cellage.json |
| 12 | LongevityMap | 22/48 human longevity-association loci | results/xext/x-ext-longevitymap.json |
| 13 | KEGG REST | longevity + autophagy pathway membership | results/xext/x-ext-kegg-longevity.json |
| 14 | Europe PMC | T. dohrnii x gene literature counts | results/xext/x-ext-europepmc-literature.json |
| 15 | AlphaFold DB | human ATG5 canonical model | results/xext/x-ext-alphafold-atg5.json |
| 16 | InterPro API | ATG5 domain architecture | results/xext/x-ext-interpro-atg5.json |
| 17 | STRING API | ATG5-ATG7-BECN1-SQSTM1 module (6 edges) | results/xext/x-ext-string-module.json |
| 18 | Reactome Content Service | ATG5 pathways (4) | results/xext/x-ext-reactome-atg5.json |
| 19 | PDBe API | ATG5 structures (9) | results/xext/x-ext-pdbe-atg5.json |
| 20 | Open Targets GraphQL | ATG5 target record | results/xext/x-ext-opentargets-atg5.json |
| 21 | Ensembl REST | human ATG5 gene xref | results/xext/x-ext-ensembl-atg5.json |
| 22 | WoRMS REST | T. dohrnii marine taxonomy authority | results/xext/x-ext-worms-td.json |
| 23 | GBIF API | T. dohrnii occurrence count | results/xext/x-ext-gbif-td.json |
| 24 | Open Tree of Life TNRS | 7/7 species matched | results/xext/x-ext-otl-species.json |
| 25 | CrossRef API | reference verification | results/xext/x-ext-crossref-refs.json |

## Software tools (15)
| # | Tool | Use | Evidence |
|---|------|-----|----------|
| 26 | NCBI BLAST+ 2.16 (tblastn, makeblastdb, blastdbcmd) | all genome mapping | results/x-ledger-*.json, /home/sandbox/jellyfish-expansion/blast |
| 27 | seqkit 2.10.0 | assembly stats for all 8 genomes | results/x-seqkit-stats.tsv |
| 28 | NCBI datasets CLI | assembly retrieval | experiments/x_fetch_queries.py logs |
| 29 | python-docx | paper build | experiments/x_makepaper.py |
| 30 | LibreOffice headless | docx→pdf render for page verification | results/x-papercount.json |
| 31 | poppler-utils (pdfinfo, pdftoppm) | page count + visual inspection | results/x-papercount.json |
| 32 | NumPy | statistics | jellyfish/xstats.py |
| 33 | SciPy [closed phase] | statistics | experiments/ml_*.py imports |
| 34 | scikit-learn [closed phase] | ML baselines | experiments/ml_dataset.py |
| 35 | PyTorch [closed phase] | CNN/GNN models | experiments/ml_cnn.py, ml_gnn.py |
| 36 | Matplotlib [closed phase] | figures | experiments/make_paper*.py |
| 37 | pyhmmer (HMMER3) [closed phase] | domain scans | experiments/domain_scan.py |
| 38 | ReportLab [closed phase] | PDF generation | experiments/make_paper26b.py |
| 39 | git | version control | repo history |
| 40 | GitHub | hosting, deploy-key CI | github.com/uditakankananonononono/mega27-26b-immortal-jellyfish-genomics |

## External judge (methodology, 41)
| 41 | ChatGPT (user's account, fleet browser) | novelty/weakness judge rounds; R1 counted | docs/X-JUDGE-ROUNDS.md |

## Attempted, NOT counted
- AnAge bulk download (https://genomics.senescence.info/species/anage_data.txt and .zip): 404 — host removed the bulk dataset. Evidence: results/xext/x-ext-anage-cnidaria.json (error record).
