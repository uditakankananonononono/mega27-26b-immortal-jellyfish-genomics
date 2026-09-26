"""Map expansion panels B/C onto 5 genomes with the closed phase's frozen
tBLASTn pipeline, plus positive (panel A) and shuffled negative controls.

Usage: python3 experiments/x_map.py {bc|actrl|bcshuf} [genome ...]
Outputs: results/x-tblastn-<set>.json, results/x-ledger-<set>.json
"""
import glob, json, os, random, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from jellyfish.loci import cluster_loci

BLAST = "/home/sandbox/jellyfish-expansion/blast/bin/tblastn"
DBDIR = "/home/sandbox/jellyfish-expansion/genomes/db"
GENOMES = ["Tdohrnii", "TdohrniiOviedo", "Trubra", "Aaurita", "Clytia"]
OUTFMT = "6 qseqid sseqid pident length evalue bitscore qstart qend sstart send qlen"
MIN_BITS = 100  # frozen by the closed phase

def read_fasta(path):
    recs, h, s = [], None, []
    for line in open(path):
        line = line.rstrip()
        if line.startswith(">"):
            if h is not None: recs.append((h, "".join(s)))
            h, s = line[1:], []
        elif line:
            s.append(line)
    if h is not None: recs.append((h, "".join(s)))
    return recs

def shuffled_fasta(recs, seed=26):
    rnd = random.Random(seed)
    out = []
    for h, s in recs:
        chars = list(s)
        rnd.shuffle(chars)
        out.append(("SHUF_" + h.split()[0], "".join(chars)))
    return out

def run_tblastn(db, fasta_path):
    cmd = [BLAST, "-query", fasta_path, "-db", db, "-evalue", "1e-5",
           "-max_target_seqs", "20", "-outfmt", OUTFMT, "-num_threads", "2"]
    out = subprocess.run(cmd, capture_output=True, text=True, timeout=5400)
    if out.returncode != 0:
        raise RuntimeError(out.stderr[-500:])
    per_query = {}
    for line in out.stdout.strip().splitlines():
        f = line.split("\t")
        qcov = (int(f[7]) - int(f[6]) + 1) / int(f[10])
        h = {"qseqid": f[0], "contig": f[1], "pident": float(f[2]),
             "alen": int(f[3]), "evalue": float(f[4]), "bits": float(f[5]),
             "qstart": int(f[6]), "qend": int(f[7]),
             "sstart": int(f[8]), "send": int(f[9]), "qcov": round(qcov, 3)}
        per_query.setdefault(f[0], []).append(h)
    return per_query

def gene_of_header(header):
    """Query files are named <Species>_<GENE>.faa; header first token is accession.
    We tag by FILE, so this is handled in main via file->queries map."""
    raise NotImplementedError

def main():
    which = sys.argv[1]
    genomes = sys.argv[2:] or GENOMES
    if which in ("bc", "bcshuf"):
        files = sorted(glob.glob("data/xpanel/*.faa"))
    elif which == "actrl":
        files = sorted(glob.glob("data/panel/*.faa"))
    else:
        raise SystemExit("unknown set")
    # build one combined fasta; map combined header -> (species, gene) from filename
    combo, hmap = [], {}
    for fp in files:
        base = os.path.basename(fp)[:-4]
        species, sym = base.split("_", 1)
        for h, s in read_fasta(fp):
            tag = f"{base}|{h.split()[0]}"
            combo.append((tag, s))
            hmap[tag] = (species, sym)
    if which == "bcshuf":
        combo = shuffled_fasta(combo)
    os.makedirs("/tmp/xmap", exist_ok=True)
    cf = f"/tmp/xmap/{which}.faa"
    with open(cf, "w") as f:
        for h, s in combo:
            f.write(f">{h}\n" + "\n".join(s[i:i+60] for i in range(0, len(s), 60)) + "\n")
    hits_out, ledger = {}, {}
    for genome in genomes:
        print(f"== {genome} {which}: {len(combo)} queries", flush=True)
        per_query = run_tblastn(f"{DBDIR}/{genome}", cf)
        # fold back to per-(species,gene)
        per_key = {}
        for tag, hs in per_query.items():
            base = tag.split("|")[0].replace("SHUF_", "", 1)
            species, sym = hmap.get(tag, (None, base.split("_", 1)[1] if "_" in base else base))
            per_key.setdefault(f"{species}_{sym}", []).extend(hs)
        hits_out[genome] = per_key
        # locus ledger per gene (merged across query species)
        per_gene = {}
        for key, hs in per_key.items():
            _, sym = key.split("_", 1)
            per_gene.setdefault(sym, []).extend(hs)
        ledger[genome] = {}
        for sym, hs in per_gene.items():
            loci = cluster_loci(hs)
            strong = [l for l in loci if l["total_bits"] >= MIN_BITS]
            ledger[genome][sym] = {"n_loci": len(loci), "n_strong": len(strong),
                                   "best": (strong[0] if strong else
                                            (loci[0] if loci else None))}
        json.dump(hits_out, open(f"results/x-tblastn-{which}.json", "w"), indent=1)
        json.dump(ledger, open(f"results/x-ledger-{which}.json", "w"), indent=1)
        print(f"== {genome} {which}: {sum(v['n_strong'] for v in ledger[genome].values())} strong loci over {len(ledger[genome])} genes", flush=True)
    print("MAPDONE", which, flush=True)

if __name__ == "__main__":
    main()
