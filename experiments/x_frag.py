#!/usr/bin/env python3
"""In silico Fragmentation Penalty Index (judge supplementary R4 demand #4).
Fragment chromosome-level T. rubra into a mock assembly matching T. dohrnii Oviedo's
scaffold length distribution, rebuild the BLAST DB, rerun the frozen bc mapping, and
measure how many panel genes 'disappear' purely from fragmentation."""
import json, os, random, subprocess, sys

G = "/home/sandbox/jellyfish-expansion/genomes"
BLAST = "/home/sandbox/jellyfish-expansion/blast/bin"
OUT = "/home/sandbox/jellyfish-expansion/repo/results/x-frag.json"
MOCK = f"{G}/TrubraMock.fna"
SEED = 27

def lengths(path):
    lens, n = [], 0
    for line in open(path):
        if line.startswith(">"):
            if n: lens.append(n)
            n = 0
        else:
            n += len(line.strip())
    if n: lens.append(n)
    return lens

def main():
    rnd = random.Random(SEED)
    ovi = lengths(f"{G}/TdohrniiOviedo.fna")
    print(f"oviedo scaffolds: {len(ovi)}, median {sorted(ovi)[len(ovi)//2]}", flush=True)
    # fragment Trubra
    nout, total = 0, 0
    with open(MOCK, "w") as out:
        seq, hdr = [], None
        def flush_scaf(seq):
            nonlocal nout, total
            s = "".join(seq)
            i = 0
            while i < len(s):
                L = min(rnd.choice(ovi), len(s) - i)
                nout += 1
                chunk = s[i:i+L]
                out.write(f">mock_{nout}\n" + "\n".join(chunk[j:j+60] for j in range(0, len(chunk), 60)) + "\n")
                i += L
                total += L
        for line in open(f"{G}/Trubra.fna"):
            if line.startswith(">"):
                if seq: flush_scaf(seq)
                seq = []
            else:
                seq.append(line.strip())
        if seq: flush_scaf(seq)
    print(f"mock: {nout} scaffolds, {total} bp", flush=True)
    subprocess.run([f"{BLAST}/makeblastdb", "-in", MOCK, "-dbtype", "nucl",
                    "-out", f"{G}/db/TrubraMock"], check=True, capture_output=True)
    print("DBDONE TrubraMock", flush=True)
    # mapping run is invoked by the queue script afterwards
    r = subprocess.run([sys.executable, "experiments/x_map.py", "bc", "TrubraMock"],
                       capture_output=True, text=True, cwd="/home/sandbox/jellyfish-expansion/repo")
    print(r.stdout[-400:], flush=True)
    intact = json.load(open("/home/sandbox/jellyfish-expansion/repo/results/x-ledger-bc.json"))["Trubra"]
    mock = json.load(open("/home/sandbox/jellyfish-expansion/repo/results/x-ledger-bc.json"))["TrubraMock"]
    intact_genes = {g for g, v in intact.items() if v["n_strong"] >= 1}
    mock_genes = {g for g, v in mock.items() if v["n_strong"] >= 1}
    lost = sorted(intact_genes - mock_genes)
    gained = sorted(mock_genes - intact_genes)
    res = {"mock_scaffolds": nout, "mock_bp": total, "seed": SEED,
           "intact_genes": len(intact_genes), "mock_genes": len(mock_genes),
           "lost_to_fragmentation": lost, "gained": gained,
           "fragmentation_penalty_index": round(len(lost) / max(1, len(intact_genes)), 4)}
    json.dump(res, open(OUT, "w"), indent=1)
    print("FPI:", json.dumps(res, indent=1)[:500], flush=True)
    print("FRAGDONE", flush=True)

if __name__ == "__main__":
    main()
