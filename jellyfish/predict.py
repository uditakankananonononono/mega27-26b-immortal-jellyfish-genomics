"""HSP-stitch gene prediction: reconstruct a candidate protein from tBLASTn HSPs.

For one gene-locus: take HSPs on the dominant strand, order by query position,
extract each HSP's subject nucleotide span from the locus FASTA, translate the
correct frame, and concatenate non-overlapping query segments. The result is a
candidate protein good enough for Pfam domain verification - NOT a final gene
model (no splice-site model); that limitation is stated in the paper.
"""
CODON = {
    'TTT':'F','TTC':'F','TTA':'L','TTG':'L','CTT':'L','CTC':'L','CTA':'L','CTG':'L',
    'ATT':'I','ATC':'I','ATA':'I','ATG':'M','GTT':'V','GTC':'V','GTA':'V','GTG':'V',
    'TCT':'S','TCC':'S','TCA':'S','TCG':'S','CCT':'P','CCC':'P','CCA':'P','CCG':'P',
    'ACT':'T','ACC':'T','ACA':'T','ACG':'T','GCT':'A','GCC':'A','GCA':'A','GCG':'A',
    'TAT':'Y','TAC':'Y','TAA':'*','TAG':'*','CAT':'H','CAC':'H','CAA':'Q','CAG':'Q',
    'AAT':'N','AAC':'N','AAA':'K','AAG':'K','GAT':'D','GAC':'D','GAA':'E','GAG':'E',
    'TGT':'C','TGC':'C','TGA':'*','TGG':'W','CGT':'R','CGC':'R','CGA':'R','CGG':'R',
    'AGT':'S','AGC':'S','AGA':'R','AGG':'R','GGT':'G','GGC':'G','GGA':'G','GGG':'G'}

def translate(nt):
    nt = nt.upper().replace('U', 'T')
    aa = []
    for i in range(0, len(nt) - 2, 3):
        aa.append(CODON.get(nt[i:i+3], 'X'))
    return "".join(aa)

def revcomp(s):
    return s.translate(str.maketrans("ACGT", "TGCA"))[::-1]

def six_frame_translate(nt):
    rc = revcomp(nt)
    return [translate(nt[i:]) for i in range(3)] + [translate(rc[i:]) for i in range(3)]

def stitch(hsps, locus_seq, locus_start):
    """hsps: HSP dicts for one locus (same gene, same genome); locus_seq: the
    extracted region string; locus_start: 1-based genomic start of that region.
    Returns stitched protein + per-HSP segments with genomic coords."""
    if not hsps:
        return None
    plus = sum(1 for h in hsps if h["send"] >= h["sstart"]) >= len(hsps) / 2
    # order by query start, keep best HSP per query region (drop contained overlaps)
    hs = sorted(hsps, key=lambda h: h["qstart"])
    kept = []
    q_end = 0
    for h in hs:
        if h["qend"] <= q_end:
            continue
        kept.append(h)
        q_end = h["qend"]
    aas, segments = [], []
    for h in kept:
        lo = min(h["sstart"], h["send"]) - locus_start
        hi = max(h["sstart"], h["send"]) - locus_start + 1
        nt = locus_seq[lo:hi]
        if not plus:
            nt = revcomp(nt)
        best = None
        for frame in range(3):
            aa = translate(nt[frame:])
            core = aa.rstrip('*')          # a single terminal stop is normal
            score = core.count('X') * -2 - core.count('*') * 5 + len(core.replace('*', ''))
            if best is None or score > best[0]:
                best = (score, core)
        aas.append(best[1].replace('*', 'X'))
        segments.append({"qstart": h["qstart"], "qend": h["qend"],
                         "s_lo": min(h["sstart"], h["send"]),
                         "s_hi": max(h["sstart"], h["send"]),
                         "strand": "+" if plus else "-", "aa_len": len(best[1])})
    return {"protein": "".join(aas), "n_segments": len(kept),
            "strand": "+" if plus else "-", "segments": segments}
