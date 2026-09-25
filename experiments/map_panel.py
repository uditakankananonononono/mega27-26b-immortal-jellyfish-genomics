"""tBLASTn the panel proteins against the jellyfish genomes; parse to JSON.

Inputs: data/panel/*.faa, BLAST dbs in ../data/genomes/db/
Output: results/tblastn_hits.json  (per genome: gene -> list of HSPs with
contig, coords, evalue, bitscore, query coverage)
"""
import json, os, subprocess, glob, sys
B = "/tmp/ncbi-blast-2.17.0+/bin/tblastn"
DBS = {"Tdohrnii": "../data/genomes/db/Tdohrnii", "Aaurita": "../data/genomes/db/Aaurita"}
OUTFMT = "6 qseqid sseqid pident length evalue bitscore qstart qend sstart send qlen"

def run(genome, db, faa, sym, species):
    cmd = [B, "-query", faa, "-db", db, "-evalue", "1e-5",
           "-max_target_seqs", "20", "-outfmt", OUTFMT, "-num_threads", "4"]
    out = subprocess.run(cmd, capture_output=True, text=True, timeout=3600).stdout
    hits = []
    for line in out.strip().splitlines():
        f = line.split("\t")
        qcov = (int(f[7]) - int(f[6]) + 1) / int(f[10])
        hits.append({"qseqid": f[0], "contig": f[1], "pident": float(f[2]),
                     "alen": int(f[3]), "evalue": float(f[4]), "bits": float(f[5]),
                     "qstart": int(f[6]), "qend": int(f[7]),
                     "sstart": int(f[8]), "send": int(f[9]), "qcov": round(qcov, 3)})
    return hits

def main():
    res = {}
    faas = sorted(glob.glob("data/panel/*.faa"))
    for genome, db in DBS.items():
        res[genome] = {}
        for faa in faas:
            species, sym = os.path.basename(faa)[:-4].split("_", 1)
            try:
                res[genome][f"{species}_{sym}"] = run(genome, db, faa, sym, species)
            except Exception as e:
                res[genome][f"{species}_{sym}"] = {"error": str(e)}
            print(genome, species, sym, len(res[genome][f"{species}_{sym}"]), flush=True)
    json.dump(res, open("results/tblastn_hits.json", "w"), indent=1)

if __name__ == "__main__":
    main()
