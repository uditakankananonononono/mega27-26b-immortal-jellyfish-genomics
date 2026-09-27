#!/usr/bin/env python3
"""Reciprocal-best-hit orthology control (judge supplementary R5 demand #1).
For top-10 AEES genes: extract best Td locus, 6-frame translate, blastp back against
Acropora query panel + human RefSeq orthologs. PASS iff top reverse hit = original gene."""
import json, os, subprocess, sys
from Bio.Seq import Seq
from Bio import SeqIO

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
G = "/home/sandbox/jellyfish-expansion/genomes"
BLAST = "/home/sandbox/jellyfish-expansion/blast/bin"
TMP = "/tmp/rbh"
PAD = 300

led = json.load(open(f"{REPO}/results/x-ledger-bc.json"))
top10 = json.load(open(f"{TMP}/top10.json"))

# combined reference DB
os.system(f"cat /tmp/xmap/bc.faa {TMP}/human_refs.faa > {TMP}/refdb.faa")
subprocess.run([f"{BLAST}/makeblastdb", "-in", f"{TMP}/refdb.faa", "-dbtype", "prot",
                "-out", f"{TMP}/refdb"], check=True, capture_output=True)

def extract(assembly, contig, start, end, strand):
    fa = f"{G}/{assembly}.fna"
    bed = f"{TMP}/reg.bed"
    if "|" in contig:
        contig = contig.split("|")[1]
    lo, hi = max(1, min(start, end) - PAD), max(start, end) + PAD
    open(bed, "w").write(f"{contig}\t{lo-1}\t{hi}\n")
    r = subprocess.run(["/tmp/seqkit", "subseq", "--bed", bed, fa], capture_output=True, text=True)
    seq = "".join(l.strip() for l in r.stdout.splitlines() if not l.startswith(">"))
    s = Seq(seq)
    return s.reverse_complement() if strand == "-" else s

def orfs(s, minlen=30):
    out = []
    for fr in range(3):
        t = s[fr:].translate()
        for piece in str(t).split("*"):
            if len(piece) >= minlen:
                out.append(piece)
    return out

res = {}
for asm in ["Tdohrnii", "TdohrniiOviedo"]:
    res[asm] = {}
    for gene in top10:
        rec = led.get(asm, {}).get(gene)
        if not rec or not rec.get("best"):
            res[asm][gene] = {"status": "no_locus"}
            continue
        b = rec["best"]
        s = extract(asm, b["contig"], b["start"], b["end"], b["strand"])
        best = None
        os_ = orfs(s)
        qf = f"{TMP}/q.fasta"
        with open(qf, "w") as fh:
            for i, o in enumerate(os_):
                fh.write(f">orf{i}\n{o}\n")
        r = subprocess.run([f"{BLAST}/blastp", "-query", qf, "-db", f"{TMP}/refdb",
                            "-evalue", "1e-5", "-max_target_seqs", "1", "-num_threads", "1",
                            "-outfmt", "6 qseqid sseqid pident evalue bitscore"],
                           capture_output=True, text=True)
        for line in r.stdout.strip().split("\n"):
            if not line.strip():
                continue
            f0 = line.split("\t")
            if best is None or float(f0[4]) > best["bits"]:
                best = {"subject": f0[1], "pident": float(f0[2]), "bits": float(f0[4])}
        if best is None:
            res[asm][gene] = {"status": "no_reverse_hit"}
        else:
            hit_gene = best["subject"].split("|")[0].split("_", 1)[-1]
            res[asm][gene] = {"status": "PASS" if hit_gene == gene else "FAIL",
                              "top_hit": best["subject"], "pident": best["pident"],
                              "bits": best["bits"], "n_loci": rec["n_loci"]}
npass = sum(1 for a in res.values() for v in a.values() if v.get("status") == "PASS")
ntot = sum(1 for a in res.values() for v in a.values() if v.get("status") in ("PASS", "FAIL"))
out = {"control": "reciprocal_best_hit", "genes": top10, "pass": npass, "total": ntot, "detail": res}
json.dump(out, open(f"{REPO}/results/x-rbh.json", "w"), indent=1)
print(json.dumps({a: {g: v.get("status") for g, v in d.items()} for a, d in res.items()}, indent=1))
print(f"RBH: {npass}/{ntot}")
