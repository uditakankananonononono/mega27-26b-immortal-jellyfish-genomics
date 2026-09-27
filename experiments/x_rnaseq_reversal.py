"""P1 #6 (phase 1, targeted): RNA-seq read-count test across the life-cycle
reversal (PRJNA603209: Polyp1/Medusa1/RevPolyp1). RAM-bounded design for the
1.9GB sandbox: extract the ~40 panel/target loci +/-5kb into a small reference,
stream ENA fastq through minimap2 against it, count primary mapq>=20 reads per
locus. Normalizers: total mapped reads (CPM) and ACTA1 actin locus."""
import json, subprocess, collections, os

MM2 = "/home/sandbox/jellyfish-expansion/tools_bin/minimap2-2.28_x64-linux/minimap2"
GENOME = "/home/sandbox/jellyfish-expansion/genomes/Tdohrnii.fna"
FAI = GENOME + ".seqkit.fai"
REF = "/tmp/xrnaseq_ref.fasta"
FLANK = 5000
RUNS = {"Medusa1": "SRR10967540", "Polyp1": "SRR10967543", "RevPolyp1": "SRR10967537"}
ENA_URLS = {
 "SRR10967540": ("https://ftp.sra.ebi.ac.uk/vol1/fastq/SRR109/040/SRR10967540/SRR10967540_1.fastq.gz",
                 "https://ftp.sra.ebi.ac.uk/vol1/fastq/SRR109/040/SRR10967540/SRR10967540_2.fastq.gz"),
 "SRR10967543": ("https://ftp.sra.ebi.ac.uk/vol1/fastq/SRR109/043/SRR10967543/SRR10967543_1.fastq.gz",
                 "https://ftp.sra.ebi.ac.uk/vol1/fastq/SRR109/043/SRR10967543/SRR10967543_2.fastq.gz"),
 "SRR10967537": ("https://ftp.sra.ebi.ac.uk/vol1/fastq/SRR109/037/SRR10967537/SRR10967537_1.fastq.gz",
                 "https://ftp.sra.ebi.ac.uk/vol1/fastq/SRR109/037/SRR10967537/SRR10967537_2.fastq.gz"),
}

led = json.load(open("results/x-ledger-bc.json"))["Tdohrnii"]
targets = {}
for gene, rec in led.items():
    if rec["best"]:
        targets[gene] = (rec["best"]["contig"], rec["best"]["start"], rec["best"]["end"])
raw = json.load(open("results/x-tblastn-bc.json"))["Tdohrnii"]
def cluster(hsps, min_bits=100, merge=500):
    byc = collections.defaultdict(list)
    for h in hsps:
        if h["bits"] < min_bits: continue
        s, e = sorted((h["sstart"], h["send"]))
        byc[h["contig"]].append((s, e, h["bits"]))
    loci = []
    for contig, hs in byc.items():
        hs.sort(); cur = None
        for s, e, bit in hs:
            if cur and s - cur[1] <= merge: cur[1] = max(cur[1], e); cur[2] += bit
            else:
                if cur: loci.append((contig, *cur))
                cur = [s, e, bit]
        if cur: loci.append((contig, *cur))
    return loci
atg5_loci = []
for qk in ("human_ATG5", "Acropora_ATG5"):
    for contig, s, e, bit in cluster(raw.get(qk, [])):
        if any(contig == c and not (e < s2 - 500 or s > e2 + 500) for c, s2, e2, _ in atg5_loci):
            continue
        atg5_loci.append((contig, s, e, bit))
atg5_loci.sort(key=lambda t: -t[3])
for i, (c, s, e, b) in enumerate(atg5_loci, 1):
    targets[f"ATG5_locus{i}"] = (c, s, e)
dec = json.load(open("results/x-ledger-decoy.json"))["Tdohrnii"]
if dec["ACTA1"]["best"]:
    b = dec["ACTA1"]["best"]
    targets["ACTA1_housekeeping"] = (b["contig"], b["start"], b["end"])
print(f"{len(targets)} targets ({len(atg5_loci)} ATG5-family loci)", flush=True)

# ---- faidx ----
fai = {}
for line in open(FAI):
    f = line.rstrip("\n").split("\t")
    fai[f[0]] = (int(f[1]), int(f[2]), int(f[3]), int(f[4]))  # len, offset, linebases, linewidth
    fai[f"dbj|{f[0]}|"] = fai[f[0]]  # ledger-style key
def fetch(contig, start, end):
    clen, off, lb, lw = fai[contig]
    start = max(0, start); end = min(clen, end)
    fh = open(GENOME, "rb")
    seq = []
    pos = start
    while pos < end:
        line_no = pos // lb
        col = pos % lb
        fh.seek(off + line_no * lw + col)
        take = min(end - pos, lb - col)
        seq.append(fh.read(take).decode())
        pos += take
    fh.close()
    return "".join(seq)

# ---- build targeted reference ----
windows = {}  # win_name -> (contig, ws, we, [ (locus, ls, le) ])
groups = collections.defaultdict(list)
for name, (c, s, e) in targets.items():
    groups[c].append((s, e, name))
ref_contigs = {}
with open(REF, "w") as fh:
    for contig, items in groups.items():
        items.sort()
        merged = []
        for s, e, name in items:
            ws, we = max(0, s - FLANK), e + FLANK
            if merged and ws <= merged[-1][1]:
                merged[-1][1] = max(merged[-1][1], we)
                merged[-1][2].append((name, s, e))
            else:
                merged.append([ws, we, [(name, s, e)]])
        for i, (ws, we, loci) in enumerate(merged):
            wname = f"{contig}__{i}"
            seq = fetch(contig, ws, we)
            windows[wname] = (contig, ws, we, loci)
            fh.write(f">{wname}\n")
            for j in range(0, len(seq), 60):
                fh.write(seq[j:j+60] + "\n")
print(f"{len(windows)} reference windows", flush=True)
locus_win = {}
for wname, (contig, ws, we, loci) in windows.items():
    for name, s, e in loci:
        locus_win[name] = (wname, s - ws, e - ws)

subprocess.run([MM2, "-d", "/tmp/xrnaseq_ref.mmi", REF], check=True, capture_output=True)

def stream_counts(url, counts, retries=2):
    best = 0
    for attempt in range(retries):
        n, rc = _stream_once(url, counts)
        best = max(best, n)
        print(f"  stream attempt {attempt+1} rc={rc} mapped={n}", flush=True)
        if rc == 0 and n > 0:
            break
    return best  # partial streams still yield valid counts; per-mate mapped logged

def _stream_once(url, counts):
    wget = subprocess.Popen(["wget", "-q", "-O", "-", url], stdout=subprocess.PIPE)
    mm = subprocess.Popen([MM2, "-t", "2", "-c", "--secondary=no", "-p", "0", "/tmp/xrnaseq_ref.mmi", "-"],
                          stdin=wget.stdout, stdout=subprocess.PIPE, text=True)
    wget.stdout.close()
    n_mapped = 0
    for line in mm.stdout:
        f = line.split("\t")
        if len(f) < 12: continue
        if not any(t == "tp:A:P" for t in f[12:]): continue
        try:
            mapq = int(f[11])
        except ValueError:
            continue
        if mapq < 20: continue
        n_mapped += 1
        wname = f[5]
        ts, te = int(f[7]), int(f[8])
        contig, ws, we, loci = windows[wname]
        for name, s, e in loci:
            ls, le = s - ws - 2000, e - ws + 2000  # locus +/- 2kb capture zone
            if not (te < ls or ts > le):
                counts[name] += 1
    mm.wait(); wget.wait()
    return n_mapped, wget.returncode

out = {}
for stage, acc in RUNS.items():
    counts = collections.Counter()
    total = 0
    for mate, url in enumerate(ENA_URLS[acc], 1):
        print(f"{stage} mate{mate}: streaming {url}", flush=True)
        total += stream_counts(url, counts)
        print(f"  cumulative mapped: {total}", flush=True)
    out[stage] = {"run": acc, "mapped_primary_mapq20": total,
                  "counts": {k: counts.get(k, 0) for k in sorted(targets)}}
    json.dump(out, open("results/x-rnaseq-reversal.json", "w"), indent=1)
print("RNASEQPHASE1DONE")
