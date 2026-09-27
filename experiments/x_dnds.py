#!/usr/bin/env python3
"""Exploratory pairwise dN/dS (P1 item 3; S2-S5 convergent demand).
For the top-10 AEES genes: extract best Td and Trubra loci, choose translation frame by
blastp vs the Acropora query, mafft-align the two proteins, thread codons, NG86 (Biopython
codonalign). Partial-gene pairwise estimate - exploratory, disclosed as such."""
import json, os, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio import SeqIO
from Bio.codonalign import build as codon_build
from Bio.codonalign.codonseq import cal_dn_ds
from Bio.Align import MultipleSeqAlignment

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
G = "/home/sandbox/jellyfish-expansion/genomes"
BLAST = "/home/sandbox/jellyfish-expansion/blast/bin"
MAFFT = "/home/sandbox/jellyfish-expansion/mafft/mafft.bat"
TMP = "/tmp/dnds"
os.makedirs(TMP, exist_ok=True)
PAD = 300

raw = json.load(open(f"{REPO}/results/x-tblastn-bc.json"))
top10 = json.load(open("/tmp/rbh/top10.json"))

def read_query(gene):
    import glob as _g
    cands = sorted(_g.glob(f"{REPO}/data/xpanel/*_{gene}.faa"))
    cands.sort(key=lambda p: 0 if "Acropora" in p else (1 if "Clytia" in p or "Hydra" in p else 2))
    for fp in cands:
        for r in SeqIO.parse(fp, "fasta"):
            return str(r.seq)
    return None

def extract(asm, b):
    contig = b["contig"].split("|")[1] if "|" in b["contig"] else b["contig"]
    lo, hi = max(1, min(b["start"], b["end"]) - PAD), max(b["start"], b["end"]) + PAD
    open(f"{TMP}/reg.bed", "w").write(f"{contig}\t{lo-1}\t{hi}\n")
    r = subprocess.run(["/tmp/seqkit", "subseq", "--bed", f"{TMP}/reg.bed", f"{G}/{asm}.fna"],
                       capture_output=True, text=True)
    seq = "".join(l.strip() for l in r.stdout.splitlines() if not l.startswith(">"))
    s = Seq(seq)
    return s.reverse_complement() if b["strand"] == "-" else s

def best_orf(s, qprot):
    open(f"{TMP}/q.faa", "w").write(f">q\n{qprot}\n")
    subprocess.run([f"{BLAST}/makeblastdb", "-in", f"{TMP}/q.faa", "-dbtype", "prot",
                    "-out", f"{TMP}/qdb"], capture_output=True)
    best = None
    for fr in range(3):
        nuc = s[fr:]
        nuc = nuc[:len(nuc) - len(nuc) % 3]
        prot = str(nuc.translate())
        open(f"{TMP}/t.faa", "w").write(f">t\n{prot}\n")
        r = subprocess.run([f"{BLAST}/blastp", "-query", f"{TMP}/t.faa", "-db", f"{TMP}/qdb",
                            "-evalue", "1e-3", "-max_target_seqs", "1", "-num_threads", "1",
                            "-outfmt", "6 bitscore"], capture_output=True, text=True)
        vals = [float(l.split("\t")[0]) for l in r.stdout.strip().splitlines() if l.strip()]
        bits = max(vals) if vals else 0.0
        if best is None or bits > best[0]:
            best = (bits, nuc, prot)
    return best[1], best[2]

def pair_dnds(gene):
    q = read_query(gene)
    if q is None:
        return {"status": "no_query"}
    out = {}
    recs = {}
    for asm in ["Tdohrnii", "Trubra"]:
        hits = []
        for key, hs in raw.get(asm, {}).items():
            if key.endswith("_" + gene):
                hits.extend(hs)
        if not hits:
            return {"status": f"no_locus_{asm}"}
        h = max(hits, key=lambda x: x["bits"])
        b = {"contig": h["contig"], "start": h["sstart"], "end": h["send"],
             "strand": "+" if h["send"] >= h["sstart"] else "-"}
        s = extract(asm, b)
        nuc, prot = best_orf(s, q)
        # trim to longest stop-free ORF segment
        pieces = prot.split("*")
        prot = max(pieces, key=len) if pieces else ""
        recs[asm] = (nuc, prot)
    fa = f"{TMP}/pair.faa"
    with open(fa, "w") as f:
        f.write(f">Td\n{recs['Tdohrnii'][1]}\n>Tr\n{recs['Trubra'][1]}\n")
    r = subprocess.run([MAFFT, "--auto", fa], capture_output=True, text=True)
    aln = {}
    h, s = None, []
    for line in r.stdout.splitlines():
        if line.startswith(">"):
            if h: aln[h] = "".join(s)
            h, s = line[1:], []
        else:
            s.append(line.strip())
    if h: aln[h] = "".join(s)
    if "Td" not in aln or "Tr" not in aln:
        return {"status": "mafft_failed", "err": r.stderr[-200:]}
    prots = [SeqRecord(Seq(aln["Td"]), id="Td"), SeqRecord(Seq(aln["Tr"]), id="Tr")]
    nucls = [SeqRecord(recs["Tdohrnii"][0], id="Td"), SeqRecord(recs["Trubra"][0], id="Tr")]
    try:
        ca = codon_build(MultipleSeqAlignment(prots), nucls, max_score=10000)
        dN, dS = cal_dn_ds(ca[0].seq, ca[1].seq, method="NG86")
        return {"status": "ok", "dN": round(float(dN), 4), "dS": round(float(dS), 4),
                "omega": round(float(dN) / float(dS), 3) if dS > 0 else None,
                "n_codons": ca.get_alignment_length() // 3}
    except Exception as e:
        return {"status": f"calc_error: {str(e)[:120]}"}

res = {}
for g in top10:
    res[g] = pair_dnds(g)
    print(g, res[g].get("status"), res[g].get("omega"), flush=True)
json.dump({"method": "NG86 pairwise, partial-gene (exploratory)", "pairs": "Tdohrnii vs Trubra",
           "results": res}, open(f"{REPO}/results/x-dnds.json", "w"), indent=1)
print("DNDSDONE")
