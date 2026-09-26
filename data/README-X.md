# Expansion data provenance (26b)
- Genomes (SHA256 in /home/sandbox workspace, logged here):
  - Tdohrnii GCA_027922465.2 (TUR_r2.0.1) https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/027/922/465/GCA_027922465.2_TUR_r2.0.1/GCA_027922465.2_TUR_r2.0.1_genomic.fna.gz SHA256 2a7580906e1b83534a1005a5b807ce48bc614b2627e0e9dbd574055f3ff33437
  - TdohrniiOviedo GCA_025167195.1 https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/025/167/195/GCA_025167195.1_ASM2516719v1/GCA_025167195.1_ASM2516719v1_genomic.fna.gz SHA256 5ebf13f06313280a5278b7297cc9f0f445f293cb7c111bec55b78846083ba55c
  - Trubra GCA_039566895.2 https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/039/566/895/GCA_039566895.2_ASM3956689v2/GCA_039566895.2_ASM3956689v2_genomic.fna.gz SHA256 0ed32c885d990d43bd913a484da07969beda495fdf7468fd50247dcde60bf91a
  - Aaurita GCA_004194415.1 https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/004/194/415/GCA_004194415.1_ABSv1/GCA_004194415.1_ABSv1_genomic.fna.gz SHA256 8a98fdd3bcd2fe46d2ee6c4287de60cde732733148d7ea649f51bde8aca044eb
  - Clytia GCF_902728285.1 https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/902/728/285/GCF_902728285.1_Clytia_hemisphaerica_genome_assembly/GCF_902728285.1_Clytia_hemisphaerica_genome_assembly_genomic.fna.gz SHA256 0072d105681e78b1818f81d44eec66603ef1ed6d8362a862e630342416986ab4
- GCA_051903475.1 (cited by the closed phase README): FTP assembly dir serves
  only assembly_report/stats/md5, no sequence files -> recorded UNAVAILABLE.
- NCBI BLAST+ 2.17.0 https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+/2.17.0/ncbi-blast-2.17.0+-x64-linux.tar.gz
- Panel B/C query proteins: NCBI eutils esearch/efetch (db=protein), per-symbol
  accessions + lengths in data/xpanel/manifest.json; retrieval deterministic
  (longest RefSeq per species, tiebreak alphabetical), species: Homo sapiens,
  Clytia hemisphaerica, Hydra vulgaris, Acropora millepora, Nematostella vectensis.

## Extension datasets (added 2026-09-27, post-prereg, EXPLORATORY ONLY - not part of frozen H1-H6)
Datasets 6-8 of the expanded collection. SHA256 in ../../genomes/sha256.txt.
- Nvectensis.fna: Nematostella vectensis GCA_932526215.2 (jaNemVect1.2 alternate haplotype), 11,386 contigs, 413MB.
  https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/932/526/215/GCA_932526215.2_jaNemVect1.2_alternate_haplotype/GCA_932526215.2_jaNemVect1.2_alternate_haplotype_genomic.fna.gz
- Mvirulenta.fna: Morbakka virulenta GCA_003991215.1 (MVIv1, box jellyfish), 4,538 contigs, 964MB.
  https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/003/991/215/GCA_003991215.1_MVIv1/GCA_003991215.1_MVIv1_genomic.fna.gz
- Hvulgaris.fna: Hydra vulgaris GCA_059997465.1 (JU_HvJNIG_1.0, non-senescent hydrozoan), 15 contigs (near-chromosome), 934MB.
  https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/059/997/465/GCA_059997465.1_JU_HvJNIG_1.0/GCA_059997465.1_JU_HvJNIG_1.0_genomic.fna.gz
