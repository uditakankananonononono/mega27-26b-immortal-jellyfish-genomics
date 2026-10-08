# Consolidated exact-label identity-gate ledger

2026-10-08. Ten cnidarian exact-label scouts, no qualified replacements and no new alignments. Excluded means no qualified candidate in these bounded checks, not biological absence. MAPT is unresolved, not rejected as biologically absent. Benchmark unchanged. Raw evidence remains local and unpushed.

## BDNF: excluded

84-aa fragment named only by ProtNLM; original record is unnamed partial protein; exact BDNF unsupported.

- uniprot: `taxonomy_id:6073 AND (gene_exact:BDNF OR protein_name:"brain-derived neurotrophic factor")`. Returned 1.
  https://rest.uniprot.org/uniprotkb/search?query=taxonomy_id%3A6073+AND+%28gene_exact%3ABDNF+OR+protein_name%3A%22brain-derived+neurotrophic+factor%22%29&format=json&size=10
- ncbi: `Cnidaria[Organism] AND (BDNF[Gene Name] OR "brain-derived neurotrophic factor"[Title])`. Returned 0.
  https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=protein&term=Cnidaria%5BOrganism%5D+AND+%28BDNF%5BGene+Name%5D+OR+%22brain-derived+neurotrophic+factor%22%5BTitle%5D%29&retmode=json&retmax=10

Primary records / domain documentation:
- https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=protein&id=CAH3015145.1&rettype=gp&retmode=text

Raw evidence and SHA-256:
- `results/x-20261008-neurotrophin-gate/BDNF-uniprot.json` : `667e15a819a1f5efd11c2a9972c45d86e3bb4d6d058704501ce778f1b7df3314`
- `results/x-20261008-neurotrophin-gate/BDNF-ncbi.json` : `89685a2d859e51628fbf86be5cdbd52a7ddfd81b6412e3d5b3c0a0f4b395d060`
- `results/x-20261008-neurotrophin-gate/BDNF-genpept-url.txt` : `e616687ba723a9db42cddb07a9101e71d9021c060cf3b650b757c2c7048fbcad`
- `results/x-20261008-neurotrophin-gate/BDNF-genpept.txt` : `4d4e55c9dc800266de92519e9c20232974f025833c51ba41911d3cbf96241320`
- `results/x-20261008-neurotrophin-gate/NGF-genpept-url.txt` : `a83e6b8e81576ced2fd2687f6b61f1de7cc570e8eb3009b4dfb62e35086ada28`
- `results/x-20261008-neurotrophin-gate/NGF-genpept.txt` : `514d0fc9cb1c9ac008b544d4c3941f47c0b00d82d8329501c21f051afe944cf1`
- `results/x-20261008-neurotrophin-gate/NGF-ncbi-all.json` : `a1e4e73f8c521c454c2c9ad2fcad0e28699a04f0df3fc415bd8f2f8925768efe`
- `results/x-20261008-neurotrophin-gate/NGF-ncbi.json` : `d75fbaf25ec49634d2d4fdefc4e7a5729bf9d1627cd58daef74be29d2b3e465c`
- `results/x-20261008-neurotrophin-gate/NGF-uniprot.json` : `6c84e00f994bc142d826c596257b10d7abaaee45bb286668b3b0bbc45e3b10b8`
- `results/x-20261008-neurotrophin-gate/outcome.json` : `faadc7376d93d24d122907757d2c3861f31f8ff82ff749e4f32420962f816a60`

## NGF: excluded

All returned named records are receptors, not NGF ligand.

- uniprot: `taxonomy_id:6073 AND (gene_exact:NGF OR protein_name:"nerve growth factor")`. Returned 5.
  https://rest.uniprot.org/uniprotkb/search?query=taxonomy_id%3A6073+AND+%28gene_exact%3ANGF+OR+protein_name%3A%22nerve+growth+factor%22%29&format=json&size=10
- ncbi: `Cnidaria[Organism] AND (NGF[Gene Name] OR "nerve growth factor"[Title])`. Returned 11.
  https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=protein&term=Cnidaria%5BOrganism%5D+AND+%28NGF%5BGene+Name%5D+OR+%22nerve+growth+factor%22%5BTitle%5D%29&retmode=json&retmax=10

Primary records / domain documentation:
- https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=protein&id=2327130070%2C2327105134%2C2327090807%2C2327082051%2C2327075423%2C2327072689%2C2327033011%2C2113771499%2C999979152%2C1066877549%2C400621323&rettype=gp&retmode=text

Raw evidence and SHA-256:
- `results/x-20261008-neurotrophin-gate/NGF-uniprot.json` : `6c84e00f994bc142d826c596257b10d7abaaee45bb286668b3b0bbc45e3b10b8`
- `results/x-20261008-neurotrophin-gate/NGF-ncbi.json` : `d75fbaf25ec49634d2d4fdefc4e7a5729bf9d1627cd58daef74be29d2b3e465c`
- `results/x-20261008-neurotrophin-gate/BDNF-genpept-url.txt` : `e616687ba723a9db42cddb07a9101e71d9021c060cf3b650b757c2c7048fbcad`
- `results/x-20261008-neurotrophin-gate/BDNF-genpept.txt` : `4d4e55c9dc800266de92519e9c20232974f025833c51ba41911d3cbf96241320`
- `results/x-20261008-neurotrophin-gate/BDNF-ncbi.json` : `89685a2d859e51628fbf86be5cdbd52a7ddfd81b6412e3d5b3c0a0f4b395d060`
- `results/x-20261008-neurotrophin-gate/BDNF-uniprot.json` : `667e15a819a1f5efd11c2a9972c45d86e3bb4d6d058704501ce778f1b7df3314`
- `results/x-20261008-neurotrophin-gate/NGF-genpept-url.txt` : `a83e6b8e81576ced2fd2687f6b61f1de7cc570e8eb3009b4dfb62e35086ada28`
- `results/x-20261008-neurotrophin-gate/NGF-genpept.txt` : `514d0fc9cb1c9ac008b544d4c3941f47c0b00d82d8329501c21f051afe944cf1`
- `results/x-20261008-neurotrophin-gate/NGF-ncbi-all.json` : `a1e4e73f8c521c454c2c9ad2fcad0e28699a04f0df3fc415bd8f2f8925768efe`
- `results/x-20261008-neurotrophin-gate/outcome.json` : `faadc7376d93d24d122907757d2c3861f31f8ff82ff749e4f32420962f816a60`

## MAPT: unresolved

Submitted MAPT naming is similarity-based; one recorded PF00418 repeat is shared-family support and cannot distinguish MAPT/MAP2/MAP4.

- uniprot: `taxonomy_id:6073 AND (gene_exact:MAPT OR protein_name:"microtubule-associated protein tau")`. Returned 0.
  https://rest.uniprot.org/uniprotkb/search?query=taxonomy_id%3A6073+AND+%28gene_exact%3AMAPT+OR+protein_name%3A%22microtubule-associated+protein+tau%22%29&format=json&size=20
- ncbi: `Cnidaria[Organism] AND (MAPT[Gene Name] OR "microtubule-associated protein tau"[Title])`. Returned 1.
  https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=protein&term=Cnidaria%5BOrganism%5D+AND+%28MAPT%5BGene+Name%5D+OR+%22microtubule-associated+protein+tau%22%5BTitle%5D%29&retmode=json&retmax=20

Primary records / domain documentation:
- https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=protein&id=999971173&rettype=gp&retmode=text
- https://rest.uniprot.org/uniprotkb/Q5YCW0.json
- https://rest.uniprot.org/uniprotkb/search?query=reviewed%3Atrue+AND+organism_id%3A9606+AND+gene_exact%3AMAP2&format=json&size=5
- https://rest.uniprot.org/uniprotkb/search?query=reviewed%3Atrue+AND+organism_id%3A9606+AND+gene_exact%3AMAP4&format=json&size=5
- https://prosite.expasy.org/PS51491
- https://prosite.expasy.org/PDOC00201

Raw evidence and SHA-256:
- `results/x-20261008-mapt-snca-gate/MAPT-uniprot.json` : `b0955baffda4f5404dce757230602d6e93cac5b7a87847b0150f23d624e40f56`
- `results/x-20261008-mapt-snca-gate/MAPT-ncbi.json` : `d86ba7c05cee78594d4a2e3a10cc4edf47518b41b6ba0120174502d4f90d648e`
- `results/x-20261008-mapt-snca-gate/MAP2-reviewed.json` : `ea84f4971a4c223bc01d7131ee5bf16c0a68e42d25c7a70c3038a2fb871f3f70`
- `results/x-20261008-mapt-snca-gate/MAP4-reviewed.json` : `31c541a6be085656cd1fd20ff88ea2fcaa910a930a57240f962e238bba85cd92`
- `results/x-20261008-mapt-snca-gate/MAPT-KXJ10347.1.fasta` : `ae4d962a7467764992116c6b42760d92bac38396b8b40d5e25e5194ccea7d240`
- `results/x-20261008-mapt-snca-gate/MAPT-genpept-url.txt` : `a38c23273c418813d09bdbfaf93d6eaf7b00cd783589cb5390c85882607de4bc`
- `results/x-20261008-mapt-snca-gate/MAPT-genpept.txt` : `9fb889e3f35843fb898ed0d46e059b4e7d4e7238212bd2030d7ff212422acd73`
- `results/x-20261008-mapt-snca-gate/Q5YCW0.json` : `d7bd8691bfe208d4b0ea2094f3a485b5fef300403689e024544fb8d011227232`
- `results/x-20261008-mapt-snca-gate/SNCA-ncbi.json` : `69b2c3a05bf0afc61d2bd24cf2f66184447e20520545338aaed6f868c3280d53`
- `results/x-20261008-mapt-snca-gate/SNCA-uniprot.json` : `728be94d81919521b42c3f1f6d8aa0100f2a999e8109657456b1fed7f7fd7d58`
- `results/x-20261008-mapt-snca-gate/outcome.json` : `0110da99dd81a8833e328fc64f24129d0048c7b2aac14ffdc7a07383d4f6cb98`
- `results/x-20261008-mapt-snca-gate/paralog-identity-outcome.json` : `89d4748390d3dbac27ddbb20f5da5fa4116246216a0e3d40d812bcf68f1b9f78`

## SNCA: excluded

No candidate returned by bounded exact gene/product searches in either primary database.

- uniprot: `taxonomy_id:6073 AND (gene_exact:SNCA OR protein_name:"alpha-synuclein")`. Returned 0.
  https://rest.uniprot.org/uniprotkb/search?query=taxonomy_id%3A6073+AND+%28gene_exact%3ASNCA+OR+protein_name%3A%22alpha-synuclein%22%29&format=json&size=20
- ncbi: `Cnidaria[Organism] AND (SNCA[Gene Name] OR "alpha-synuclein"[Title])`. Returned 0.
  https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=protein&term=Cnidaria%5BOrganism%5D+AND+%28SNCA%5BGene+Name%5D+OR+%22alpha-synuclein%22%5BTitle%5D%29&retmode=json&retmax=20

No candidate primary accession record to inspect; search response is the evidence.

Raw evidence and SHA-256:
- `results/x-20261008-mapt-snca-gate/SNCA-uniprot.json` : `728be94d81919521b42c3f1f6d8aa0100f2a999e8109657456b1fed7f7fd7d58`
- `results/x-20261008-mapt-snca-gate/SNCA-ncbi.json` : `69b2c3a05bf0afc61d2bd24cf2f66184447e20520545338aaed6f868c3280d53`
- `results/x-20261008-mapt-snca-gate/MAP2-reviewed.json` : `ea84f4971a4c223bc01d7131ee5bf16c0a68e42d25c7a70c3038a2fb871f3f70`
- `results/x-20261008-mapt-snca-gate/MAP4-reviewed.json` : `31c541a6be085656cd1fd20ff88ea2fcaa910a930a57240f962e238bba85cd92`
- `results/x-20261008-mapt-snca-gate/MAPT-KXJ10347.1.fasta` : `ae4d962a7467764992116c6b42760d92bac38396b8b40d5e25e5194ccea7d240`
- `results/x-20261008-mapt-snca-gate/MAPT-genpept-url.txt` : `a38c23273c418813d09bdbfaf93d6eaf7b00cd783589cb5390c85882607de4bc`
- `results/x-20261008-mapt-snca-gate/MAPT-genpept.txt` : `9fb889e3f35843fb898ed0d46e059b4e7d4e7238212bd2030d7ff212422acd73`
- `results/x-20261008-mapt-snca-gate/MAPT-ncbi.json` : `d86ba7c05cee78594d4a2e3a10cc4edf47518b41b6ba0120174502d4f90d648e`
- `results/x-20261008-mapt-snca-gate/MAPT-uniprot.json` : `b0955baffda4f5404dce757230602d6e93cac5b7a87847b0150f23d624e40f56`
- `results/x-20261008-mapt-snca-gate/Q5YCW0.json` : `d7bd8691bfe208d4b0ea2094f3a485b5fef300403689e024544fb8d011227232`
- `results/x-20261008-mapt-snca-gate/outcome.json` : `0110da99dd81a8833e328fc64f24129d0048c7b2aac14ffdc7a07383d4f6cb98`
- `results/x-20261008-mapt-snca-gate/paralog-identity-outcome.json` : `89d4748390d3dbac27ddbb20f5da5fa4116246216a0e3d40d812bcf68f1b9f78`

## APOE: excluded

ProtNLM-only APOE name; original hypothetical protein with repetitive sequence and SMC_prok_B match, not exact APOE support.

- uniprot: `taxonomy_id:6073 AND (gene_exact:APOE OR protein_name:"apolipoprotein E")`. Returned 1.
  https://rest.uniprot.org/uniprotkb/search?query=taxonomy_id%3A6073+AND+%28gene_exact%3AAPOE+OR+protein_name%3A%22apolipoprotein+E%22%29&format=json&size=20
- ncbi: `Cnidaria[Organism] AND (APOE[Gene Name] OR "apolipoprotein E"[Title])`. Returned 0.
  https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=protein&term=Cnidaria%5BOrganism%5D+AND+%28APOE%5BGene+Name%5D+OR+%22apolipoprotein+E%22%5BTitle%5D%29&retmode=json&retmax=20

Primary records / domain documentation:
- https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=protein&id=KAJ7372127.1&rettype=gp&retmode=text

Raw evidence and SHA-256:
- `results/x-20261008-apoe-prnp-gate/APOE-uniprot.json` : `750920d2279dc28407efca2329f85a8c84674f09ed7394cd9c8d815b2e71d693`
- `results/x-20261008-apoe-prnp-gate/APOE-ncbi.json` : `19d94e60423b29c0db2e3a6cbfebbdb294eb8b90dd7f393aaabb6c2adece333d`
- `results/x-20261008-apoe-prnp-gate/APOE-genpept-url.txt` : `a56200fc9be536b55856d14e9311246f3b43b592e10b18e80ae14ecc0d08f9c8`
- `results/x-20261008-apoe-prnp-gate/APOE-genpept.txt` : `a356faffe3c9f278b758a61a6804be5ed17a9af43a3420d1ccfc5f25fc17f17b`
- `results/x-20261008-apoe-prnp-gate/PRNP-ncbi.json` : `57f25cc391564f17fae2619b55c8a4b1f512db6a4b89a83851260d22cb1e1905`
- `results/x-20261008-apoe-prnp-gate/PRNP-uniprot.json` : `6edae6cd18393cd575544f4576e5f7899ff2fb06ce720d353f13b16872be0f40`
- `results/x-20261008-apoe-prnp-gate/outcome.json` : `ef2df01f5379f7063f4ef8b6c579dc17ff785e721129c98d57b57fa148704699`

## PRNP: excluded

No candidate returned by bounded exact gene/product searches in either primary database.

- uniprot: `taxonomy_id:6073 AND (gene_exact:PRNP OR protein_name:"prion protein")`. Returned 0.
  https://rest.uniprot.org/uniprotkb/search?query=taxonomy_id%3A6073+AND+%28gene_exact%3APRNP+OR+protein_name%3A%22prion+protein%22%29&format=json&size=20
- ncbi: `Cnidaria[Organism] AND (PRNP[Gene Name] OR "prion protein"[Title])`. Returned 0.
  https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=protein&term=Cnidaria%5BOrganism%5D+AND+%28PRNP%5BGene+Name%5D+OR+%22prion+protein%22%5BTitle%5D%29&retmode=json&retmax=20

No candidate primary accession record to inspect; search response is the evidence.

Raw evidence and SHA-256:
- `results/x-20261008-apoe-prnp-gate/PRNP-uniprot.json` : `6edae6cd18393cd575544f4576e5f7899ff2fb06ce720d353f13b16872be0f40`
- `results/x-20261008-apoe-prnp-gate/PRNP-ncbi.json` : `57f25cc391564f17fae2619b55c8a4b1f512db6a4b89a83851260d22cb1e1905`
- `results/x-20261008-apoe-prnp-gate/APOE-genpept-url.txt` : `a56200fc9be536b55856d14e9311246f3b43b592e10b18e80ae14ecc0d08f9c8`
- `results/x-20261008-apoe-prnp-gate/APOE-genpept.txt` : `a356faffe3c9f278b758a61a6804be5ed17a9af43a3420d1ccfc5f25fc17f17b`
- `results/x-20261008-apoe-prnp-gate/APOE-ncbi.json` : `19d94e60423b29c0db2e3a6cbfebbdb294eb8b90dd7f393aaabb6c2adece333d`
- `results/x-20261008-apoe-prnp-gate/APOE-uniprot.json` : `750920d2279dc28407efca2329f85a8c84674f09ed7394cd9c8d815b2e71d693`
- `results/x-20261008-apoe-prnp-gate/outcome.json` : `ef2df01f5379f7063f4ef8b6c579dc17ff785e721129c98d57b57fa148704699`

## CDKN2A: excluded

No candidate returned by bounded exact gene/product searches in either primary database.

- uniprot: `taxonomy_id:6073 AND (gene_exact:CDKN2A OR protein_name:"cyclin-dependent kinase inhibitor 2A")`. Returned 0.
  https://rest.uniprot.org/uniprotkb/search?query=taxonomy_id%3A6073+AND+%28gene_exact%3ACDKN2A+OR+protein_name%3A%22cyclin-dependent+kinase+inhibitor+2A%22%29&format=json&size=20
- ncbi: `Cnidaria[Organism] AND (CDKN2A[Gene Name] OR "cyclin-dependent kinase inhibitor 2A"[Title])`. Returned 0.
  https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=protein&term=Cnidaria%5BOrganism%5D+AND+%28CDKN2A%5BGene+Name%5D+OR+%22cyclin-dependent+kinase+inhibitor+2A%22%5BTitle%5D%29&retmode=json&retmax=20

No candidate primary accession record to inspect; search response is the evidence.

Raw evidence and SHA-256:
- `results/x-20261008-final-quartet-gate/CDKN2A-uniprot.json` : `4afee4827d16d2f46d32fd4fc8a9324f6b504e70e2a07b941f0ce5fb8eb0ec42`
- `results/x-20261008-final-quartet-gate/CDKN2A-ncbi.json` : `c62f08d9a110b3d8eba63308b0a8edeac1f6b5790cb370a42ddde6306d2bf9f7`
- `results/x-20261008-final-quartet-gate/GHR-genpept-url.txt` : `75bebaf4c41e40124b090ffe1d0672a7c63039959fe21e602fc4c67e3c6ba26d`
- `results/x-20261008-final-quartet-gate/GHR-genpept.txt` : `efff8029b2363aae29818ee365360e559e7bd7f0e599d3ffbc7a5160011201a2`
- `results/x-20261008-final-quartet-gate/GHR-ncbi.json` : `893b3e25eeedbd446563627ba702ad396242d783eaa33298f2a01bd85d24e2fa`
- `results/x-20261008-final-quartet-gate/GHR-uniprot.json` : `a7d6847a2a876822a27c79d9f1302608e94c7a4c99354f810438f8d2091b2f4a`
- `results/x-20261008-final-quartet-gate/IGF1-ncbi.json` : `dda1c60745a5f19287e980dd98866f1d34f1d6a3848f450a96e6cf349419610d`
- `results/x-20261008-final-quartet-gate/IGF1-uniprot.json` : `868e3d083ad17734953837e1ad92a8fd6da9465c753a9a7c6aab2492e75e3a2e`
- `results/x-20261008-final-quartet-gate/TREM2-ncbi.json` : `9267934ee1ab623d2df26eb1e9c204923620417aa75b54ae2ef9a1f764e684b1`
- `results/x-20261008-final-quartet-gate/TREM2-uniprot.json` : `3f08974bd519f1a902e8a5b9d9a9e957b4c0fdd8b790c347b3f939185b9d1135`
- `results/x-20261008-final-quartet-gate/outcome.json` : `7a6b567b2dc8d69c95321a030a44981548a75ea2b1e115ba0a648cd34e604753`

## GHR: excluded

ProtNLM-only unnamed partial Porites models and an MBD5 pathway-phrase match; none supports exact GHR.

- uniprot: `taxonomy_id:6073 AND (gene_exact:GHR OR protein_name:"growth hormone receptor")`. Returned 3.
  https://rest.uniprot.org/uniprotkb/search?query=taxonomy_id%3A6073+AND+%28gene_exact%3AGHR+OR+protein_name%3A%22growth+hormone+receptor%22%29&format=json&size=20
- ncbi: `Cnidaria[Organism] AND (GHR[Gene Name] OR "growth hormone receptor"[Title])`. Returned 1.
  https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=protein&term=Cnidaria%5BOrganism%5D+AND+%28GHR%5BGene+Name%5D+OR+%22growth+hormone+receptor%22%5BTitle%5D%29&retmode=json&retmax=20

Primary records / domain documentation:
- https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=protein&id=CAH3192342.1%2CCAH3169576.1%2C2462373518&rettype=gp&retmode=text

Raw evidence and SHA-256:
- `results/x-20261008-final-quartet-gate/GHR-uniprot.json` : `a7d6847a2a876822a27c79d9f1302608e94c7a4c99354f810438f8d2091b2f4a`
- `results/x-20261008-final-quartet-gate/GHR-ncbi.json` : `893b3e25eeedbd446563627ba702ad396242d783eaa33298f2a01bd85d24e2fa`
- `results/x-20261008-final-quartet-gate/CDKN2A-ncbi.json` : `c62f08d9a110b3d8eba63308b0a8edeac1f6b5790cb370a42ddde6306d2bf9f7`
- `results/x-20261008-final-quartet-gate/CDKN2A-uniprot.json` : `4afee4827d16d2f46d32fd4fc8a9324f6b504e70e2a07b941f0ce5fb8eb0ec42`
- `results/x-20261008-final-quartet-gate/GHR-genpept-url.txt` : `75bebaf4c41e40124b090ffe1d0672a7c63039959fe21e602fc4c67e3c6ba26d`
- `results/x-20261008-final-quartet-gate/GHR-genpept.txt` : `efff8029b2363aae29818ee365360e559e7bd7f0e599d3ffbc7a5160011201a2`
- `results/x-20261008-final-quartet-gate/IGF1-ncbi.json` : `dda1c60745a5f19287e980dd98866f1d34f1d6a3848f450a96e6cf349419610d`
- `results/x-20261008-final-quartet-gate/IGF1-uniprot.json` : `868e3d083ad17734953837e1ad92a8fd6da9465c753a9a7c6aab2492e75e3a2e`
- `results/x-20261008-final-quartet-gate/TREM2-ncbi.json` : `9267934ee1ab623d2df26eb1e9c204923620417aa75b54ae2ef9a1f764e684b1`
- `results/x-20261008-final-quartet-gate/TREM2-uniprot.json` : `3f08974bd519f1a902e8a5b9d9a9e957b4c0fdd8b790c347b3f939185b9d1135`
- `results/x-20261008-final-quartet-gate/outcome.json` : `7a6b567b2dc8d69c95321a030a44981548a75ea2b1e115ba0a648cd34e604753`

## IGF1: excluded

Returned UniProt records are IGF1 receptors, not IGF1 ligand; NCBI exact search returned zero.

- uniprot: `taxonomy_id:6073 AND (gene_exact:IGF1 OR protein_name:"insulin-like growth factor 1")`. Returned 5.
  https://rest.uniprot.org/uniprotkb/search?query=taxonomy_id%3A6073+AND+%28gene_exact%3AIGF1+OR+protein_name%3A%22insulin-like+growth+factor+1%22%29&format=json&size=20
- ncbi: `Cnidaria[Organism] AND (IGF1[Gene Name] OR "insulin-like growth factor 1"[Title])`. Returned 0.
  https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=protein&term=Cnidaria%5BOrganism%5D+AND+%28IGF1%5BGene+Name%5D+OR+%22insulin-like+growth+factor+1%22%5BTitle%5D%29&retmode=json&retmax=20

No candidate primary accession record to inspect; search response is the evidence.

Raw evidence and SHA-256:
- `results/x-20261008-final-quartet-gate/IGF1-uniprot.json` : `868e3d083ad17734953837e1ad92a8fd6da9465c753a9a7c6aab2492e75e3a2e`
- `results/x-20261008-final-quartet-gate/IGF1-ncbi.json` : `dda1c60745a5f19287e980dd98866f1d34f1d6a3848f450a96e6cf349419610d`
- `results/x-20261008-final-quartet-gate/CDKN2A-ncbi.json` : `c62f08d9a110b3d8eba63308b0a8edeac1f6b5790cb370a42ddde6306d2bf9f7`
- `results/x-20261008-final-quartet-gate/CDKN2A-uniprot.json` : `4afee4827d16d2f46d32fd4fc8a9324f6b504e70e2a07b941f0ce5fb8eb0ec42`
- `results/x-20261008-final-quartet-gate/GHR-genpept-url.txt` : `75bebaf4c41e40124b090ffe1d0672a7c63039959fe21e602fc4c67e3c6ba26d`
- `results/x-20261008-final-quartet-gate/GHR-genpept.txt` : `efff8029b2363aae29818ee365360e559e7bd7f0e599d3ffbc7a5160011201a2`
- `results/x-20261008-final-quartet-gate/GHR-ncbi.json` : `893b3e25eeedbd446563627ba702ad396242d783eaa33298f2a01bd85d24e2fa`
- `results/x-20261008-final-quartet-gate/GHR-uniprot.json` : `a7d6847a2a876822a27c79d9f1302608e94c7a4c99354f810438f8d2091b2f4a`
- `results/x-20261008-final-quartet-gate/TREM2-ncbi.json` : `9267934ee1ab623d2df26eb1e9c204923620417aa75b54ae2ef9a1f764e684b1`
- `results/x-20261008-final-quartet-gate/TREM2-uniprot.json` : `3f08974bd519f1a902e8a5b9d9a9e957b4c0fdd8b790c347b3f939185b9d1135`
- `results/x-20261008-final-quartet-gate/outcome.json` : `7a6b567b2dc8d69c95321a030a44981548a75ea2b1e115ba0a648cd34e604753`

## TREM2: excluded

No candidate returned by bounded exact gene/product searches in either primary database.

- uniprot: `taxonomy_id:6073 AND (gene_exact:TREM2 OR protein_name:"triggering receptor expressed on myeloid cells 2")`. Returned 0.
  https://rest.uniprot.org/uniprotkb/search?query=taxonomy_id%3A6073+AND+%28gene_exact%3ATREM2+OR+protein_name%3A%22triggering+receptor+expressed+on+myeloid+cells+2%22%29&format=json&size=20
- ncbi: `Cnidaria[Organism] AND (TREM2[Gene Name] OR "triggering receptor expressed on myeloid cells 2"[Title])`. Returned 0.
  https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=protein&term=Cnidaria%5BOrganism%5D+AND+%28TREM2%5BGene+Name%5D+OR+%22triggering+receptor+expressed+on+myeloid+cells+2%22%5BTitle%5D%29&retmode=json&retmax=20

No candidate primary accession record to inspect; search response is the evidence.

Raw evidence and SHA-256:
- `results/x-20261008-final-quartet-gate/TREM2-uniprot.json` : `3f08974bd519f1a902e8a5b9d9a9e957b4c0fdd8b790c347b3f939185b9d1135`
- `results/x-20261008-final-quartet-gate/TREM2-ncbi.json` : `9267934ee1ab623d2df26eb1e9c204923620417aa75b54ae2ef9a1f764e684b1`
- `results/x-20261008-final-quartet-gate/CDKN2A-ncbi.json` : `c62f08d9a110b3d8eba63308b0a8edeac1f6b5790cb370a42ddde6306d2bf9f7`
- `results/x-20261008-final-quartet-gate/CDKN2A-uniprot.json` : `4afee4827d16d2f46d32fd4fc8a9324f6b504e70e2a07b941f0ce5fb8eb0ec42`
- `results/x-20261008-final-quartet-gate/GHR-genpept-url.txt` : `75bebaf4c41e40124b090ffe1d0672a7c63039959fe21e602fc4c67e3c6ba26d`
- `results/x-20261008-final-quartet-gate/GHR-genpept.txt` : `efff8029b2363aae29818ee365360e559e7bd7f0e599d3ffbc7a5160011201a2`
- `results/x-20261008-final-quartet-gate/GHR-ncbi.json` : `893b3e25eeedbd446563627ba702ad396242d783eaa33298f2a01bd85d24e2fa`
- `results/x-20261008-final-quartet-gate/GHR-uniprot.json` : `a7d6847a2a876822a27c79d9f1302608e94c7a4c99354f810438f8d2091b2f4a`
- `results/x-20261008-final-quartet-gate/IGF1-ncbi.json` : `dda1c60745a5f19287e980dd98866f1d34f1d6a3848f450a96e6cf349419610d`
- `results/x-20261008-final-quartet-gate/IGF1-uniprot.json` : `868e3d083ad17734953837e1ad92a8fd6da9465c753a9a7c6aab2492e75e3a2e`
- `results/x-20261008-final-quartet-gate/outcome.json` : `7a6b567b2dc8d69c95321a030a44981548a75ea2b1e115ba0a648cd34e604753`

