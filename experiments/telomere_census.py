"""Run the telomere census over all downloaded assemblies -> results/telomere_census.json"""
import json, glob, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from jellyfish.telomere import census

GENOMES = {
    "Tdohrnii_Kazusa_GCA_027922465.2": "../data/genomes/GCA_027922465.2/ncbi_dataset/data/GCA_027922465.2/GCA_027922465.2_TUR_r2.0.1_genomic.fna",
    "Tdohrnii_Oviedo_GCA_025167195.1": "../data/genomes/GCA_025167195.1/ncbi_dataset/data/GCA_025167195.1/GCA_025167195.1_ASM2516719v1_genomic.fna",
    "Aaurita_GCA_004194415.1": "../data/genomes/GCA_004194415.1/ncbi_dataset/data/GCA_004194415.1/GCA_004194415.1_ABSv1_genomic.fna",
    "Clytia_GCF_902728285.1": "../data/genomes/GCF_902728285.1/ncbi_dataset/data/GCF_902728285.1/*_genomic.fna",
    "HydraT2T_GCF_038396675.1": "../data/genomes/GCF_038396675.1/ncbi_dataset/data/GCF_038396675.1/*_genomic.fna",
    "Nematostella_GCA_932526225.2": "../data/genomes/GCA_932526225.2/ncbi_dataset/data/GCA_932526225.2/*_genomic.fna",
}

def resolve(p):
    g = glob.glob(p)
    return g[0] if g else None

out = {}
for label, path in GENOMES.items():
    rp = resolve(path)
    if not rp:
        print("skip (not downloaded):", label); continue
    out[label] = census(rp)
    out[label]["assembly"] = label
    print("done", label, flush=True)
json.dump(out, open("results/telomere_census.json", "w"), indent=1)
