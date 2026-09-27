"""P1 #12 (HMMER arm): phmmer concordance on the flagship assembly, RAM-bounded.
Reuses the diamond arm's 6-frame ORF cache (/tmp/xconc_orfs_Tdohrnii.faa,
286,785 ORFs >=75aa with coords in headers), digitizes in chunks, runs
pyhmmer.phmmer per query per chunk (E<=1e-5), clusters to loci (500bp merge),
compares with x-ledger-bc.json Tdohrnii."""
import json, collections
from pyhmmer import easel, hmmer

ORF_FAA = "/tmp/xconc_orfs_Tdohrnii.faa"
led = json.load(open("results/x-ledger-bc.json"))["Tdohrnii"]
genes = sorted(led)
abc = easel.Alphabet.amino()

def bare(c):
    p = c.split("|")
    return p[1] if len(p) >= 3 and p[0] in ("dbj", "gb", "emb", "ref") else c.rstrip("|")
def load_chunks(path, chunk=100000):
    seqs, coords = [], []
    name, buf = None, []
    def flush():
        if name is None: return
        parts = name.split("|")
        gs, ge = int(parts[-2]), int(parts[-1])
        contig = "|".join(parts[1:-2])
        coords.append((contig, gs, ge))
        seqs.append(easel.TextSequence(name=name.encode(), sequence="".join(buf)).digitize(abc))
    for line in open(path):
        if line.startswith(">"):
            flush()
            name = line[1:].split()[0]; buf = []
        else:
            buf.append(line.strip())
    flush()
    for i in range(0, len(seqs), chunk):
        yield seqs[i:i+chunk], coords[i:i+chunk]

hits = collections.defaultdict(list)  # gene -> [(contig, s, e, score)]
queries = []
qgenes = []
for line_block in open("/tmp/xconc_panelB.faa").read().split(">")[1:]:
    lines = line_block.strip().split("\n")
    key = lines[0].split()[0]
    gene = key.split("_", 1)[1] if "_" in key else key
    if gene not in genes: continue
    q = "".join(lines[1:])
    queries.append(easel.TextSequence(name=key.encode(), sequence=q).digitize(abc))
    qgenes.append(gene)

ci = 0
for seqs, coords in load_chunks(ORF_FAA):
    ci += 1
    print(f"chunk {ci}: {len(seqs)} ORFs", flush=True)
    # direct approach: iterate hits with coordinate alignment
    for qseq, gene in zip(queries, qgenes):
        for top in hmmer.phmmer(qseq, seqs, cpus=1, E=1e-5):
            for hit in top:
                nm = hit.name if isinstance(hit.name, str) else hit.name.decode()
                parts = nm.split("|")
                gs, ge = int(parts[-2]), int(parts[-1])
                contig = "|".join(parts[1:-2])
                hits[gene].append((bare(contig), gs, ge, float(hit.score)))
json.dump({g: len(h) for g, h in hits.items()}, open("/tmp/hmmer_hitcnt.json", "w"))
out = {}
for gene in genes:
    byc = collections.defaultdict(list)
    for contig, s, e, bit in hits.get(gene, []):
        byc[contig].append((s, e, bit))
    loci = []
    for contig, hs in byc.items():
        hs.sort(); cur = None
        for s, e, bit in hs:
            if cur and s - cur[1] <= 500: cur[1] = max(cur[1], e); cur[2] += bit
            else:
                if cur: loci.append((contig, *cur))
                cur = [s, e, bit]
        if cur: loci.append((contig, *cur))
    ref = led[gene]
    best_ok = False
    if loci and ref["best"]:
        b = ref["best"]
        for contig, s, e, bit in loci:
            if bare(contig) == bare(b["contig"]) and not (e < b["start"]-500 or s > b["end"]+500):
                best_ok = True; break
    out[gene] = {"phmmer_loci": len(loci), "tblastn_strong": ref["n_strong"],
                 "tblastn_significant": ref["n_strong"] >= 3, "best_locus_overlap": best_ok}
    print(f"{gene}: phmmer_loci={len(loci)} tblastn_strong={ref['n_strong']} best_overlap={best_ok}", flush=True)
json.dump(out, open("results/x-concordance-hmmer.json", "w"), indent=1)
n_sig_h = sum(1 for g in genes if out[g]["phmmer_loci"] >= 3)
n_sig_t = sum(1 for g in genes if out[g]["tblastn_significant"])
n_both = sum(1 for g in genes if out[g]["phmmer_loci"] >= 3 and out[g]["tblastn_significant"])
n_best = sum(1 for g in genes if out[g]["best_locus_overlap"])
print(f"SUMMARY: phmmer>=3 {n_sig_h}/36, tblastn>=3 {n_sig_t}/36, both {n_both}, best-overlap {n_best}/36")
print("HMMERCONCDONE")
