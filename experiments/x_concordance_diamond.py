"""P1 #12 (DIAMOND arm): orthogonal-aligner concordance.
Six-frame ORFs >=75aa per genome -> DIAMOND blastp with the 36 verified human
panel proteins (bit>=100, 500bp locus merge, frozen-style) -> compare with
x-ledger-bc.json per genome. Answers: do the frozen tblastn findings depend on
BLAST specifically, or does an independent aligner recover them?"""
import json, os, subprocess, collections

DIAMOND = "/home/sandbox/jellyfish-expansion/tools_bin/diamond"
G = {"Tdohrnii": "/home/sandbox/jellyfish-expansion/genomes/Tdohrnii.fna",
     "TdohrniiOviedo": "/home/sandbox/jellyfish-expansion/genomes/TdohrniiOviedo.fna",
     "Trubra": "/home/sandbox/jellyfish-expansion/genomes/Trubra.fna",
     "Aaurita": "/home/sandbox/jellyfish-expansion/genomes/Aaurita.fna",
     "Clytia": "/home/sandbox/jellyfish-expansion/genomes/Clytia.fna"}
led = json.load(open("results/x-ledger-bc.json"))
genes = sorted(led["Tdohrnii"])
assert len(genes) == 36

bases = "TCAG"
aas = "FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG"
CODON = {}
i = 0
for b1 in bases:
    for b2 in bases:
        for b3 in bases:
            CODON[b1+b2+b3] = aas[i]; i += 1
COMP = str.maketrans("ACGTNacgtn", "TGCANtgcan")

def trl(s):
    return "".join(CODON.get(s[i:i+3], "X") for i in range(0, len(s)-2, 3))

def orfs_to_faa(fa, out_faa, min_aa=75):
    name = None; buf = []
    def emit(seq, nm, fh):
        rc = seq.translate(COMP)[::-1]
        L = len(seq); n = 0
        for strand, s in (("+", seq), ("-", rc)):
            for fr in range(3):
                prot = trl(s[fr:])
                i = 0
                while i < len(prot):
                    if prot[i] == "M":
                        j = prot.find("*", i)
                        if j == -1: j = len(prot)
                        if j - i >= min_aa:
                            ps = fr + 3*i; pe = fr + 3*j
                            gs, ge = (L-pe, L-ps) if strand == "-" else (ps, pe)
                            fh.write(f">o{n}|{nm}|{gs}|{ge}\n{prot[i:j]}\n")
                            n += 1
                        i = j + 1
                    else:
                        i += 1
        return n
    total = 0
    with open(out_faa, "w") as fh:
        for line in open(fa):
            if line.startswith(">"):
                if name: total += emit("".join(buf).upper(), name, fh)
                name = line.split()[0][1:]; buf = []
            else:
                buf.append(line.strip())
        if name: total += emit("".join(buf).upper(), name, fh)
    return total

def run(cmd):
    subprocess.run(cmd, check=True, capture_output=True)

def bare(c):
    p = c.split("|")
    return p[1] if len(p) >= 3 and p[0] in ("dbj", "gb", "emb", "ref") else c.rstrip("|")
res = {}
for gname, fa in G.items():
    orf_faa = f"/tmp/xconc_orfs_{gname}.faa"
    if not os.path.exists(orf_faa):
        n = orfs_to_faa(fa, orf_faa)
        print(f"{gname}: {n} ORFs translated", flush=True)
    else:
        print(f"{gname}: ORF fasta cached", flush=True)
    db = f"/tmp/xconc_db_{gname}"
    if not os.path.exists(db + ".dmnd"):
        run([DIAMOND, "makedb", "--in", orf_faa, "-d", db, "-p", "2"])
    tsv = f"/tmp/xconc_bp_{gname}.tsv"
    run([DIAMOND, "blastp", "-q", "/tmp/xconc_panelB.faa", "-d", db, "-o", tsv,
         "--outfmt", "6", "qseqid", "sseqid", "pident", "length", "qstart", "qend",
         "sstart", "send", "evalue", "bitscore", "-e", "1e-5", "-k", "200", "-p", "2"])
    hits = collections.defaultdict(list)
    for line in open(tsv):
        c = line.split("\t")
        bit = float(c[9])
        if bit < 100: continue
        key = c[0].split("|")[0]
        gene = key.split("_", 1)[1] if "_" in key else key
        parts = c[1].split("|")
        gs, ge = parts[-2], parts[-1]
        contig = "|".join(parts[1:-2])
        hits[gene].append((bare(contig), int(gs), int(ge), bit))
    conc = {}
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
        loci.sort(key=lambda t: -t[3])
        ref = led[gname].get(gene, {"n_strong": 0, "best": None})
        best_ok = False
        if loci and ref["best"]:
            b = ref["best"]
            for contig, s, e, bit in loci:
                if bare(contig) == bare(b["contig"]) and not (e < b["start"]-500 or s > b["end"]+500):
                    best_ok = True; break
        conc[gene] = {"diamond_loci": len(loci), "tblastn_strong": ref["n_strong"],
                      "tblastn_significant": ref["n_strong"] >= 3, "best_locus_overlap": best_ok}
    res[gname] = conc
    n_d = sum(1 for g in genes if conc[g]["diamond_loci"] >= 3)
    n_t = sum(1 for g in genes if conc[g]["tblastn_significant"])
    n_both = sum(1 for g in genes if conc[g]["diamond_loci"] >= 3 and conc[g]["tblastn_significant"])
    n_best = sum(1 for g in genes if conc[g]["best_locus_overlap"])
    print(f"{gname}: diamond>=3loci {n_d}/36, tblastn>=3 {n_t}/36, both {n_both}, best-overlap {n_best}/36", flush=True)
json.dump(res, open("results/x-concordance-diamond.json", "w"), indent=1)
print("DIAMONDCONCDONE")
