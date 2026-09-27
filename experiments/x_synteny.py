"""P1 #13: ORF-level micro-synteny around ATG5 loci across genomes.
No annotation exists (desert), so: extract +/-40kb around each genome's best
ATG5 locus, 6-frame translate, find ORFs >= 100aa outside the ATG5 span,
pairwise blastp against the Td flanking ORFs, count conserved neighbors."""
import json, os, subprocess, sys
sys.path.insert(0, ".")
from Bio.Seq import Seq

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
G = "/home/sandbox/jellyfish-expansion/genomes"
BLAST = "/home/sandbox/jellyfish-expansion/blast/bin"
TMP = "/tmp/synteny"; FLANK = 40000; MINORF = 300  # nt
os.makedirs(TMP, exist_ok=True)

def contigs(asm):
    # return a lazy fetcher: stream the fasta, capture only the wanted contig
    class Fetcher:
        def get(self, name):
            if "|" in name:
                parts = [p for p in name.split("|") if p]
                name = parts[1] if len(parts) > 1 else parts[0]
            grab, buf = False, []
            with open(f"{G}/{asm}.fna") as f:
                for ln in f:
                    if ln.startswith(">"):
                        if grab:
                            return "".join(buf)
                        grab = ln[1:].split()[0] == name
                    elif grab:
                        buf.append(ln.strip())
            return "".join(buf) if grab else None
    return Fetcher()

def orfs(seq, exclude):
    out = []
    for frame in range(3):
        p = str(Seq(seq[frame:]).translate())
        pos = frame
        for piece in p.split("*"):
            aa = len(piece)
            if aa * 3 >= MINORF:
                s, e = pos, pos + aa * 3
                if not (s < exclude[1] and e > exclude[0]):
                    out.append((s, e, piece))
            pos += (aa + 1) * 3
    rc = str(Seq(seq).reverse_complement())
    for frame in range(3):
        p = str(Seq(rc[frame:]).translate())
        pos = frame
        for piece in p.split("*"):
            aa = len(piece)
            if aa * 3 >= MINORF:
                s, e = pos, pos + aa * 3
                gs, ge = len(seq) - e, len(seq) - s
                if not (gs < exclude[1] and ge > exclude[0]):
                    out.append((gs, ge, piece))
            pos += (aa + 1) * 3
    return out

led = {}
for f in ["results/x-ledger-bc.json", "results/x-ledger-bcext.json"]:
    for g, genes in json.load(open(f)).items():
        led[g] = genes

res = {}
td_orfs = None
for asm in ["Tdohrnii", "Trubra", "Aaurita", "Clytia", "TdohrniiOviedo", "Hvulgaris", "Nvectensis", "Mvirulenta"]:
    b = led.get(asm, {}).get("ATG5", {}).get("best")
    if not b:
        res[asm] = {"status": "no_locus"}; continue
    cs = contigs(asm)
    c = cs.get(b["contig"])
    if c is None:
        res[asm] = {"status": "contig_missing"}; continue
    lo, hi = sorted((b["start"], b["end"]))
    s0 = max(0, lo - FLANK); e0 = min(len(c), hi + FLANK)
    win = c[s0:e0]
    excl = (lo - s0, hi - s0)
    o = orfs(win, excl)
    with open(f"{TMP}/{asm}.faa", "w") as f:
        for i, (s, e, p) in enumerate(o):
            f.write(f">{asm}_orf{i}_{s}_{e}\n{p}\n")
    res[asm] = {"status": "ok", "n_orfs": len(o), "window": e0 - s0}
    if asm == "Tdohrnii":
        td_orfs = f"{TMP}/{asm}.faa"
    print(asm, len(o), "flanking ORFs", flush=True)

# blastp Td vs each other genome
if td_orfs:
    for asm in res:
        if asm in ("Tdohrnii",) or res[asm].get("status") != "ok":
            continue
        subprocess.run([f"{BLAST}/makeblastdb", "-in", f"{TMP}/{asm}.faa", "-dbtype", "prot",
                        "-out", f"{TMP}/{asm}"], capture_output=True)
        r = subprocess.run([f"{BLAST}/blastp", "-query", td_orfs, "-db", f"{TMP}/{asm}",
                            "-evalue", "1e-5", "-max_target_seqs", "1", "-outfmt",
                            "6 qseqid sseqid pident length evalue bitscore"],
                           capture_output=True, text=True)
        hits = {l.split("\t")[0] for l in r.stdout.splitlines() if l.strip()}
        res[asm]["conserved_neighbor_orfs"] = len(hits)
        res[asm]["td_orfs_total"] = res["Tdohrnii"]["n_orfs"]
        print(asm, "conserved:", len(hits), "/", res["Tdohrnii"]["n_orfs"], flush=True)
json.dump(res, open("results/x-synteny.json", "w"), indent=1)
print("SYNTENYDONE")
